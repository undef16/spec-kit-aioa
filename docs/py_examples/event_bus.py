"""In-memory event bus for typed event dispatch (TIP-008).

Cross-actor communication goes through the event bus. Actors never call
each other's methods directly. The event bus technology is an implementation
decision — by default, use InMemoryEventBus (zero infrastructure).

Handler error isolation: if a handler raises, the exception is logged
and the remaining handlers still receive the event. A broken subscriber
must not break the publisher or other subscribers.
"""

from __future__ import annotations

import logging
import sys
from typing import Callable

from events import Event

logger = logging.getLogger(__name__)

# Public type alias for handlers — at module scope so users can write
# `bus.subscribe(MyEvent, handler)` and tools like IDEs resolve the
# signature correctly.
Handler = Callable[[Event], None]


class InMemoryEventBus:
    """Simple publish/subscribe event bus with typed dispatch.

    Usage:
        bus = InMemoryEventBus()
        bus.subscribe(TuningStarted, lambda e: print(e.strategy_name))
        bus.publish(TuningStarted(strategy_name="rsi"))

    Notes:
        - `subscribe` and `unsubscribe` are O(n) over the handler list.
        - `unsubscribe` uses identity comparison (handler is a function or
          bound method — pass the same object you registered).
        - `publish` isolates handler exceptions; one bad handler does not
          prevent the others from receiving the event.
        - This bus is not thread-safe; wrap with locks if sharing across
          threads.
        - Pass debug_trace=True to print event flow to stderr.
        - Subscribe, unsubscribe, and publish actions are traced when
          debug_trace is enabled.
        - The trace is designed for development debugging, not production
          logging.
    """

    def __init__(self, debug_trace: bool = False) -> None:
        # Plain dict (not defaultdict) so that `len(bus._handlers)` reflects
        # only types that have been subscribed to.
        self._handlers: dict[type, list[Handler]] = {}
        self._debug_trace = debug_trace

    @staticmethod
    def _truncate_long_lists(obj: object, max_visible: int = 3) -> object:
        """Truncate long lists in trace output for readability."""
        if isinstance(obj, list) and len(obj) > max_visible:
            return obj[:max_visible] + [f"... ({len(obj) - max_visible} more)"]
        return obj

    def _trace(self, action: str, **kwargs: object) -> None:
        """Print formatted trace info to stderr when debug_trace is enabled."""
        if not self._debug_trace:
            return
        parts = [f"[EventBus] {action}"]
        for key, value in kwargs.items():
            parts.append(f"{key}={self._truncate_long_lists(value)}")
        print(" | ".join(parts), file=sys.stderr)

    def subscribe(self, event_type: type, handler: Handler) -> None:
        """Register a handler for a specific event type.

        Args:
            event_type: The concrete event class to listen for. Must be a
                subclass of Event (or a duck-typed equivalent).
            handler: Callable invoked with the event when published.
        """
        self._trace("SUBSCRIBE", event_type=event_type.__name__, handler=handler)
        self._handlers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: type, handler: Handler) -> None:
        """Remove a previously registered handler.

        Uses identity comparison (the `is` operator). Pass the exact same
        handler object that was given to `subscribe`.

        Args:
            event_type: The event class the handler was registered for.
            handler: The handler object to remove. A no-op if the handler
                was not registered.
        """
        self._trace("UNSUBSCRIBE", event_type=event_type.__name__, handler=handler)
        handlers = self._handlers.get(event_type)
        if handlers is None:
            return
        self._handlers[event_type] = [h for h in handlers if h is not handler]

    def publish(self, event: Event) -> None:
        """Dispatch an event to all handlers registered for its type.

        Handler exceptions are caught and logged; remaining handlers
        still receive the event. This implements the "fire and forget"
        contract of an event bus — a subscriber failure must not
        propagate to the publisher.
        """
        handlers = list(self._handlers.get(type(event), []))
        self._trace("PUBLISH", event=type(event).__name__, handlers=len(handlers))
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                logger.exception(
                    "Handler %r raised while processing %r; continuing.",
                    handler,
                    event,
                )
