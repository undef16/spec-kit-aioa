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
import pprint
import sys
from typing import Callable

from events import Event

logger = logging.getLogger(__name__)

Handler = Callable[[Event], None]


class InMemoryEventBus:
    """Simple publish/subscribe event bus with typed dispatch.

    Usage:
        bus = InMemoryEventBus()
        bus.subscribe(FilterRequested, lambda e: print(e.config))
        bus.publish(FilterRequested(config=config))

    Notes:
        - Handler exceptions are caught and logged — remaining handlers still fire.
        - unsubscribe uses identity comparison (pass the same object you registered).
        - Not thread-safe; wrap with locks if sharing across threads.
    """

    def __init__(self, debug_trace: bool = False) -> None:
        self._handlers: dict[type, list[Handler]] = {}
        self._debug_trace = debug_trace

    @staticmethod
    def _truncate_long_lists(obj: object, max_visible: int = 3) -> object:
        """Recursively truncate lists longer than 2*max_visible, keeping
        the first *max_visible* and last *max_visible* elements with a
        placeholder in between.
        """
        if isinstance(obj, dict):
            return {k: InMemoryEventBus._truncate_long_lists(v, max_visible) for k, v in obj.items()}
        if isinstance(obj, list):
            if len(obj) > 2 * max_visible:
                head = [InMemoryEventBus._truncate_long_lists(x, max_visible) for x in obj[:max_visible]]
                tail = [InMemoryEventBus._truncate_long_lists(x, max_visible) for x in obj[-max_visible:]]
                hidden = len(obj) - 2 * max_visible
                return head + [f"... ({hidden} items hidden)"] + tail
            return [InMemoryEventBus._truncate_long_lists(x, max_visible) for x in obj]
        return obj

    def _trace(self, action: str, **kwargs: object) -> None:
        """Print formatted trace info to stderr when debug_trace is enabled."""
        if not self._debug_trace:
            return
        print("═══ EVENT BUS TRACE ═══", file=sys.stderr)
        print(f"Action: {action}", file=sys.stderr)
        if action == "PUBLISH":
            event_type = kwargs.get("event_type", "?")
            event = kwargs.get("event")
            handler_count = kwargs.get("handler_count", 0)
            print(f"  Event type: {event_type}", file=sys.stderr)
            print("  Event data:", file=sys.stderr)
            if event is not None and hasattr(event, "model_dump"):
                data = self._truncate_long_lists(event.model_dump())
                print(pprint.pformat(data, indent=4), file=sys.stderr)
            print(f"  Handlers to receive: {handler_count}", file=sys.stderr)
        elif action in ("SUBSCRIBE", "UNSUBSCRIBE"):
            event_type = kwargs.get("event_type", "?")
            handler = kwargs.get("handler", "?")
            print(f"  Event type: {event_type}", file=sys.stderr)
            print(f"  Handler: {handler!r}", file=sys.stderr)
        print("═══ END TRACE ═══", file=sys.stderr)

    def subscribe(self, event_type: type, handler: Handler) -> None:
        """Register a handler for a specific event type."""
        self._trace("SUBSCRIBE", event_type=event_type, handler=handler)
        self._handlers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: type, handler: Handler) -> None:
        """Remove a previously registered handler (identity comparison)."""
        self._trace("UNSUBSCRIBE", event_type=event_type, handler=handler)
        handlers = self._handlers.get(event_type)
        if handlers is None:
            return
        self._handlers[event_type] = [h for h in handlers if h is not handler]

    def publish(self, event: Event) -> None:
        """Dispatch an event to all handlers registered for its type.

        Handler exceptions are caught and logged; remaining handlers
        still receive the event.
        """
        handlers = list(self._handlers.get(type(event), []))
        self._trace(
            "PUBLISH",
            event_type=type(event).__name__,
            event=event,
            handler_count=len(handlers),
        )
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                logger.exception(
                    "Handler %r raised while processing %r; continuing.",
                    handler,
                    event,
                )
