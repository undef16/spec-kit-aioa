"""ADTO — Auditable Data Transfer Object (TIP-007).

ADTO satisfies three requirements:
1. Immutability — the object's state cannot be modified after construction
   in any way that bypasses the audit trail. Runtime attribute assignment is
   restricted to declared model fields; non-field names raise AttributeError.
2. Auditability — mutation history can be retrieved via mutation_history().
3. Provenance — caller class/method and timestamp are captured for each change.

This is the Python reference implementation matching the pseudocode
specification in docs/AIOA.md.

Disabling audit
---------------
Audit trail can be disabled at construction time for performance-critical code:

    event = TuningStarted("rsi", adto_trace_enabled=False)

When disabled, __setattr__ still validates and rejects non-field names, but
no history is recorded. Use with caution — the audit trail is part of the
ADTO contract.
"""

from __future__ import annotations

import copy
import inspect
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)

# Private attribute names (used with object.__setattr__ / object.__getattribute__)
_ADTO_HISTORY = "_adto_history"
_ADTO_TRACE_ENABLED = "_adto_trace_enabled"


@dataclass(frozen=True)
class PropertyChange:
    """A single property change in an ADTO audit trail (immutable)."""

    property_name: str
    new_value: Any


@dataclass(frozen=True)
class TraceEntry:
    """A trace entry recording a batch of changes from one caller (immutable)."""

    timestamp: datetime
    caller_class: str
    caller_method: str
    changes: tuple[PropertyChange, ...]
    snapshot: Any


class ADTO(BaseModel):
    """Base class for Auditable Data Transfer Objects.

    Inherits from pydantic.BaseModel — all subclasses get validation,
    serialization (model_dump, model_dump_json), and schema generation.

    Property changes are tracked automatically via __setattr__ override.
    Call mutation_history() to retrieve the audit trail (a deep copy).

    Usage:
        class User(ADTO):
            name: str

        user = User(name="alice")     # initial set tracked
        user.name = "bob"             # automatically recorded
        print(user.mutation_history())
    """

    model_config = ConfigDict(extra="forbid")

    def __init__(self, **kwargs: Any) -> None:
        # Pop adto_trace_enabled from kwargs (pydantic must not receive it).
        trace_enabled = kwargs.pop("adto_trace_enabled", True)

        # Extract only model field kwargs to pass to pydantic (extra="forbid"
        # would reject any other key).
        field_kwargs = {k: v for k, v in kwargs.items() if k in type(self).model_fields}
        super().__init__(**field_kwargs)

        # Initialize audit attributes AFTER super().__init__() because pydantic
        # v2's BaseModel.__init__ may rebuild __dict__ internally, which would
        # drop attributes set via object.__setattr__ beforehand.
        object.__setattr__(self, _ADTO_HISTORY, [])
        object.__setattr__(self, _ADTO_TRACE_ENABLED, trace_enabled)

        # Defensive: if pydantic ever bypasses our __setattr__ (some versions
        # use object.__setattr__ internally), explicitly record the initial
        # values so the audit trail is never empty for a constructed ADTO.
        if trace_enabled:
            self._on_property_changed(field_kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        """Intercept public attribute sets for change tracking.

        Non-field names (not starting with '_') are rejected — ADTOs are
        typed and cannot grow ad-hoc attributes. The internal audit
        attributes (_adto_history, _adto_trace_enabled) and pydantic-private
        attributes (starting with '__' or '_pydantic_') are allowed through.
        """
        cls = type(self)
        if not name.startswith("_") and name not in cls.model_fields:
            raise AttributeError(
                f"{cls.__name__} has no field '{name}'. "
                f"ADTOs are typed; only declared model fields can be set."
            )

        super().__setattr__(name, value)

        if not object.__getattribute__(self, _ADTO_TRACE_ENABLED):
            return

        if name in cls.model_fields:
            self._on_property_changed(name, value)

    def _on_property_changed(self, changes: dict[str, Any]) -> None:
        """Record property changes in the audit trail.

        Detects caller class/method from the stack trace. Falls back to a
        warning (not silent "unknown") if the frame cannot be analyzed.
        """
        caller_class, caller_method = self._detect_caller()

        property_changes = tuple(
            PropertyChange(property_name=name, new_value=copy.deepcopy(value))
            for name, value in changes.items()
        )

        history: list[TraceEntry] = object.__getattribute__(self, _ADTO_HISTORY)
        last: Optional[TraceEntry] = history[-1] if history else None

        if (last is not None
                and last.caller_class == caller_class
                and last.caller_method == caller_method):
            # Same caller — build a new TraceEntry with the merged changes
            # (TraceEntry is frozen, so we cannot mutate in place).
            existing = {change.property_name: change for change in last.changes}
            for property_change in property_changes:
                existing[property_change.property_name] = property_change
            new_entry = TraceEntry(
                timestamp=last.timestamp,
                caller_class=last.caller_class,
                caller_method=last.caller_method,
                changes=tuple(existing.values()),
                snapshot=copy.deepcopy(self),
            )
            history[-1] = new_entry
        else:
            entry = TraceEntry(
                timestamp=datetime.now(timezone.utc),
                caller_class=caller_class,
                caller_method=caller_method,
                changes=property_changes,
                snapshot=copy.deepcopy(self),
            )
            history.append(entry)

    def _detect_caller(self) -> tuple[str, str]:
        """Walk the call stack to identify the caller of __setattr__.

        Returns (caller_class, caller_method). Assumes a valid call chain:
        _detect_caller <- _on_property_changed <- __setattr__/__init__

        Falls back to ("<undetected>", "<unknown>") when stack frames are
        unavailable (e.g. non-CPython implementations).
        """
        frame = inspect.currentframe()
        if frame is None:
            logger.warning("Cannot detect caller: no current frame available")
            return "<undetected>", "<unknown>"

        caller_frame = frame.f_back
        if caller_frame is None:
            logger.warning("Cannot detect caller: no caller frame available")
            return "<undetected>", "<unknown>"

        caller_frame = caller_frame.f_back
        if caller_frame is None:
            logger.warning("Cannot detect caller: no grandparent frame available")
            return "<undetected>", "<unknown>"

        caller_method = caller_frame.f_code.co_name
        caller_class = "<undetected>"
        if "self" in caller_frame.f_locals:
            self_obj = caller_frame.f_locals["self"]
            cls = getattr(self_obj, "__class__", None)
            if cls is not None:
                caller_class = cls.__name__
        return caller_class, caller_method

    def mutation_history(self) -> list[TraceEntry]:
        """Retrieve the ordered history of all recorded changes.

        Returns a deep copy — the caller can safely mutate the result
        without affecting the internal audit state.
        """
        return copy.deepcopy(object.__getattribute__(self, _ADTO_HISTORY))
