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
    """

    def __init__(self) -> None:
        # Plain dict (not defaultdict) so that `len(bus._handlers)` reflects
        # only types that have been subscribed to.
        self._handlers: dict[type, list[Handler]] = {}

    def subscribe(self, event_type: type, handler: Handler) -> None:
        """Register a handler for a specific event type.

        Args:
            event_type: The concrete event class to listen for. Must be a
                subclass of Event (or a duck-typed equivalent).
            handler: Callable invoked with the event when published.
        """
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
        for handler in list(self._handlers.get(type(event), [])):
            try:
                handler(event)
            except Exception:
                logger.exception(
                    "Handler %r raised while processing %r; continuing.",
                    handler,
                    event,
                )
