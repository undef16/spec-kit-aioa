"""PipelineBuilder — wires actors to an event bus (TIP-005).

Subscribes ``@handler``-decorated methods of each actor to the event bus.
The caller is responsible for creating all actor instances; this builder
only handles wiring.

Usage:
    builder = PipelineBuilder()
    result = builder.build(actors=[actor_a, actor_b], bus=bus)
"""

from __future__ import annotations

import inspect
import logging
import types as pytypes
import typing
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

class EventBus(Protocol):
    """Protocol for event bus — only subscribe and publish needed."""

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None: ...
    def publish(self, event: Any) -> None: ...

logger = logging.getLogger(__name__)


class HandlerValidationError(TypeError):
    """Raised when @handler metadata doesn't match method signature."""
    pass



class PipelineBuilder:
    """Builder that wires already-created actors to an event bus.

    The ``build()`` method:
    1. Iterates the provided actor instances.
    2. Wires ``@handler``-decorated methods to the event bus.
    3. Returns a ``PipelineResult`` with the wired actors.

    This class has no knowledge of specific actors — the caller is
    responsible for creating them.
    """

    def build(
        self,
        actors: list[object],
        bus: EventBus,
    ) -> None:
        """Wire *actors* to *bus* and return the result.

        Args:
            actors: List of actor instances to wire, in execution order.
            bus: Event bus (any object satisfying the ``EventBus`` protocol).

        Returns:
            PipelineResult with the wired actors.
        """
        for actor in actors:
            self.wire_actor(actor, type(actor), bus)


    # ------------------------------------------------------------------
    # Wiring
    # ------------------------------------------------------------------

    @staticmethod
    def wire_actor(actor: object, actor_cls: type, bus: EventBus) -> None:
        """Inspect ``@handler`` methods on *actor_cls* and subscribe to *bus*.

        Static so tests can wire actors without creating a factory instance.

        Args:
            actor: Instance to wire.
            actor_cls: Class used for introspection.
            bus: Event bus (any object satisfying the ``EventBus`` protocol).
        """
        for method_name in dir(actor_cls):
            method = getattr(actor_cls, method_name)
            if not hasattr(method, "_handler_input"):
                continue

            # Validate handler metadata against the method signature
            PipelineBuilder._validate_handler(actor_cls, method_name, method)

            event_type = method._handler_input
            output_type = getattr(method, "_handler_output", None)
            bound_method = getattr(actor, method_name)

            if output_type:
                bus.subscribe(
                    event_type,
                    PipelineBuilder._make_publisher(bound_method, bus),
                )
            else:
                bus.subscribe(event_type, bound_method)

    # ------------------------------------------------------------------
    # Handler validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_handler(actor_cls: type, method_name: str, method: Callable[..., Any]) -> None:
        """Validate ``@handler`` metadata against the method's signature.

        Checks that the first parameter (after ``self``) is annotated with the
        declared ``input_type`` and that the return annotation matches the
        declared ``output_type`` (or ``output_type | None`` for optional
        publishing).

        Raises:
            HandlerValidationError: On any mismatch.
        """
        if not callable(method):
            raise HandlerValidationError(
                f"@{actor_cls.__name__}.{method_name}: "
                f"@handler applied to non-callable '{method_name}'"
            )

        # Resolve type hints — handles ``from __future__ import annotations``
        # which stores annotations as strings at runtime.
        try:
            hints = typing.get_type_hints(method)
        except Exception:
            hints = {}

        try:
            sig = inspect.signature(method)
        except (ValueError, TypeError):
            return  # Can't introspect (C extension, builtin, etc.)

        params = list(sig.parameters.values())
        expected_input = method._handler_input
        expected_output = method._handler_output

        # --- Input type validation ---
        # First parameter after ``self`` must be annotated as ``input_type``
        if len(params) < 2:
            raise HandlerValidationError(
                f"{actor_cls.__name__}.{method_name}: "
                f"@handler({expected_input.__name__}, ...) declares input type "
                f"'{expected_input.__name__}' but method has no event parameter"
            )

        event_param = params[1]
        if event_param.name in hints:
            actual_input = hints[event_param.name]
            if actual_input != expected_input:
                raise HandlerValidationError(
                    f"{actor_cls.__name__}.{method_name}: "
                    f"@handler input type mismatch. "
                    f"Declared: '{expected_input.__name__}', "
                    f"Parameter '{event_param.name}' annotated as: "
                    f"'{getattr(actual_input, '__name__', actual_input)}'"
                )

        # --- Output type validation ---
        # Return annotation must be ``output_type`` or ``output_type | None``
        if expected_output is not None and "return" in hints:
            actual_return = hints["return"]
            if actual_return != expected_output:
                # Build set of union types (typing.Union + types.UnionType for 3.10+)
                _union_types = {typing.Union}
                if hasattr(pytypes, "UnionType"):
                    _union_types.add(pytypes.UnionType)  # type: ignore[attr-defined]

                origin = typing.get_origin(actual_return)
                if origin in _union_types:
                    args = typing.get_args(actual_return)
                    if not (expected_output in args and type(None) in args):
                        raise HandlerValidationError(
                            f"{actor_cls.__name__}.{method_name}: "
                            f"@handler output type mismatch. "
                            f"Declared: '{expected_output.__name__}', "
                            f"Return annotation resolves to '{actual_return}'"
                        )
                else:
                    raise HandlerValidationError(
                        f"{actor_cls.__name__}.{method_name}: "
                        f"@handler output type mismatch. "
                        f"Declared: '{expected_output.__name__}', "
                        f"Return annotation: "
                        f"'{getattr(actual_return, '__name__', actual_return)}'"
                    )

    # ------------------------------------------------------------------
    # Publisher wrapper
    # ------------------------------------------------------------------

    @staticmethod
    def _make_publisher(
        handler_fn: Callable[[Any], Any | None],
        bus: EventBus,
    ) -> Callable[[Any], None]:
        """Wrap *handler_fn* so its return value is auto-published to *bus*.

        Handlers that return ``None`` skip publishing. If the return value
        is a list, each item is published individually.

        Exceptions from the handler are logged with full context and re-raised.
        """

        def wrapper(event: Any) -> None:
            try:
                result = handler_fn(event)
            except Exception:
                logger.exception(
                    "Handler %s failed on %s",
                    handler_fn.__qualname__,
                    type(event).__name__,
                )
                raise
            if result is not None:
                if isinstance(result, list):
                    for item in result:
                        bus.publish(item)
                else:
                    bus.publish(result)

        return wrapper


# ── Example actors ──────────────────────────────────────────────────────────

from pydantic import BaseModel


class OrderPlaced(BaseModel):
    order_id: str
    total: float


class PaymentRequested(BaseModel):
    order_id: str
    amount: float


class PaymentCompleted(BaseModel):
    order_id: str
    amount: float


class CheckoutActor:
    @handler(OrderPlaced, PaymentRequested)
    def process_order(self, event: OrderPlaced) -> PaymentRequested:
        return PaymentRequested(order_id=event.order_id, amount=event.total)


class PaymentActor:
    @handler(PaymentRequested, PaymentCompleted)
    def process_payment(self, event: PaymentRequested) -> PaymentCompleted:
        return PaymentCompleted(order_id=event.order_id, amount=event.amount)


class NotificationActor:
    @handler(PaymentCompleted)
    def notify(self, event: PaymentCompleted) -> None:
        print(f"Order {event.order_id} paid {event.amount}")


if __name__ == "__main__":
    from event_bus import InMemoryEventBus

    logging.basicConfig(level=logging.INFO)
    bus = InMemoryEventBus(debug_trace=True)
    actors = [CheckoutActor(), PaymentActor(), NotificationActor()]
    PipelineBuilder().build(actors, bus)
    bus.publish(OrderPlaced(order_id="ORD-001", total=49.99))
