"""Tests for event-driven architecture example (TIP-008 + TIP-007)."""

from event_bus import InMemoryEventBus
from events import (
    Event,
    TrialCompleted,
    TuningCompleted,
    TuningFailed,
    TuningStarted,
)


def _make_collector(name: str, results: list, value: int = 0) -> None:
    """Named handler factory — avoids E731 lambda assignment warnings."""
    def handler(event: Event) -> None:
        results.append(value)
    handler.__name__ = name
    return handler  # type: ignore[return-value]


class TestEventBusTypedDispatch:
    """Handlers receive only events of their subscribed type."""

    def test_handler_receives_subscribed_event(self):
        bus = InMemoryEventBus()
        received: list[TuningStarted] = []
        bus.subscribe(TuningStarted, lambda e: received.append(e))
        event = TuningStarted(strategy_name="rsi")
        bus.publish(event)
        assert len(received) == 1
        assert received[0].strategy_name == "rsi"
        assert received[0].trace_id == event.trace_id

    def test_handler_ignores_unsubscribed_types(self):
        bus = InMemoryEventBus()
        tuning_events: list[TuningStarted] = []
        bus.subscribe(TuningStarted, lambda e: tuning_events.append(e))
        bus.publish(TrialCompleted(strategy_name="rsi", trial_id="t1", metric_value=0.95))
        assert len(tuning_events) == 0

    def test_multiple_event_types_independent(self):
        bus = InMemoryEventBus()
        started: list[TuningStarted] = []
        completed: list[TrialCompleted] = []
        bus.subscribe(TuningStarted, lambda e: started.append(e))
        bus.subscribe(TrialCompleted, lambda e: completed.append(e))
        bus.publish(TuningStarted(strategy_name="rsi"))
        bus.publish(TrialCompleted(strategy_name="rsi", trial_id="t1", metric_value=0.95))
        assert len(started) == 1
        assert len(completed) == 1


class TestEventBusMultipleHandlers:
    """Multiple handlers can subscribe to the same event type."""

    def test_multiple_handlers_all_receive(self):
        bus = InMemoryEventBus()
        results: list[int] = []
        bus.subscribe(TuningStarted, lambda _: results.append(1))
        bus.subscribe(TuningStarted, lambda _: results.append(2))
        bus.publish(TuningStarted(strategy_name="rsi"))
        assert results == [1, 2]


class TestEventBusUnsubscribe:
    """Handlers can be removed after subscription."""

    def test_unsubscribe_removes_handler(self):
        bus = InMemoryEventBus()
        results: list[int] = []

        def handler(event: Event) -> None:
            results.append(1)

        bus.subscribe(TuningStarted, handler)
        bus.unsubscribe(TuningStarted, handler)
        bus.publish(TuningStarted(strategy_name="rsi"))
        assert results == []

    def test_unsubscribe_unknown_handler_is_noop(self):
        bus = InMemoryEventBus()
        # Should not raise even if handler was never registered.
        bus.unsubscribe(TuningStarted, lambda e: None)


class TestEventBusErrorIsolation:
    """A handler exception must not break other handlers (M3)."""

    def test_failing_handler_does_not_stop_others(self):
        bus = InMemoryEventBus()
        results: list[str] = []

        def bad_handler(event: Event) -> None:
            raise RuntimeError("boom")

        def good_handler(event: Event) -> None:
            results.append("ok")

        bus.subscribe(TuningStarted, bad_handler)
        bus.subscribe(TuningStarted, good_handler)
        # Should not raise; good_handler must still receive the event.
        bus.publish(TuningStarted(strategy_name="rsi"))
        assert results == ["ok"]


class TestEventBusChoreography:
    """Multiple actors communicate only through events (TIP-008)."""

    def test_choreography_flow(self):
        bus = InMemoryEventBus()
        published_events: list = []
        bus.subscribe(TuningStarted, lambda e: published_events.append(e))
        bus.subscribe(TrialCompleted, lambda e: published_events.append(e))
        bus.subscribe(TuningCompleted, lambda e: published_events.append(e))
        bus.subscribe(TuningFailed, lambda e: published_events.append(e))

        bus.publish(TuningStarted(strategy_name="rsi"))
        assert len(published_events) == 1

        bus.publish(TrialCompleted(strategy_name="rsi", trial_id="t1", metric_value=0.95))
        assert len(published_events) == 2

        assert isinstance(published_events[0], TuningStarted)
        assert isinstance(published_events[1], TrialCompleted)
