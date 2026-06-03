"""Event types for event-driven architecture (TIP-008 + TIP-007).

All events are ADTOs (TIP-007), inheriting from Event which is itself an ADTO.
This combines TIP-007 audit trail with TIP-008 choreography — every event
payload crossing an actor boundary is typed and auditable.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from adto import ADTO
from pydantic import Field


class Event(ADTO):
    """Base event: all events have trace_id and timestamp.

    Inherits ADTO's audit trail — every mutation is recorded. In practice
    events are constructed once and published; the audit captures the
    initial state for traceability.
    """

    trace_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TuningStarted(Event):
    """Emitted when tuning begins."""

    strategy_name: str


class TrialCompleted(Event):
    """Emitted when a single trial finishes."""

    strategy_name: str
    trial_id: str
    metric_value: float


class TuningCompleted(Event):
    """Emitted when all trials are done."""

    strategy_name: str
    total_trials: int
    best_metric: float


class TuningFailed(Event):
    """Emitted when tuning fails."""

    strategy_name: str
    reason: str
