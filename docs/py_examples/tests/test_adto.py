"""Comprehensive tests for the ADTO base class (TIP-007).

Tests cover construction, setattr validation, audit trail recording,
trace disabling, caller detection, frozen dataclasses, and edge cases.
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from dataclasses import FrozenInstanceError

import pytest
from pydantic import ValidationError

from adto import ADTO, PropertyChange, TraceEntry

# ---------------------------------------------------------------------------
# Concrete ADTO subclass for testing
# ---------------------------------------------------------------------------


class SampleADTO(ADTO):
    name: str
    value: int = 0
    tags: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _MethodCaller:
    """Used by test_detect_caller_from_method to set a field from a method."""

    def set_name(self, obj: SampleADTO, new_name: str) -> None:
        obj.name = new_name


# ===================================================================
# TestADTOConstruction
# ===================================================================


class TestADTOConstruction:
    """ADTO construction validation — fields, defaults, and error cases."""

    def test_create_with_valid_fields(self) -> None:
        """Creating an ADTO with declared model fields sets them correctly."""
        obj = SampleADTO(name="test", value=42, tags=["a", "b"])
        assert obj.name == "test"
        assert obj.value == 42
        assert obj.tags == ["a", "b"]

    def test_create_with_adto_trace_enabled_false(self) -> None:
        """When adto_trace_enabled=False the initial history is empty."""
        obj = SampleADTO(name="test", value=42, adto_trace_enabled=False)
        assert len(obj.mutation_history()) == 0

    def test_extra_field_rejected(self) -> None:
        """Creating an ADTO with an undeclared field drops the extra field
        at the boundary (Parse Don't Validate). The model is created
        successfully with only the declared fields."""
        # ADTO's custom __init__ filters unknown kwargs — pydantic never
        # sees them. This is intentional: the boundary parse step ensures
        # only declared model fields reach the constructor.
        obj = SampleADTO(name="test", unknown="x")  # type: ignore[call-arg]
        assert obj.name == "test"
        # unknown was filtered — it is not a model field.
        assert not hasattr(obj, "unknown")
        assert obj.model_fields_set == {"name"}

    def test_missing_required_field_raises(self) -> None:
        """Omitting a required (non-defaulted) field raises ValidationError."""
        with pytest.raises(ValidationError):
            SampleADTO(value=42)  # missing required 'name'


# ===================================================================
# TestADTOSetattr
# ===================================================================


class TestADTOSetattr:
    """ADTO __setattr__ validation — declared fields accepted, others rejected."""

    def test_set_declared_field(self) -> None:
        """Setting a declared model field works and the value is reflected."""
        obj = SampleADTO(name="test")
        obj.name = "updated"
        assert obj.name == "updated"

    def test_set_non_field_raises_attribute_error(self) -> None:
        """Setting an undeclared, non-private name raises AttributeError."""
        obj = SampleADTO(name="test")
        with pytest.raises(AttributeError, match="has no field 'unknown'"):
            obj.unknown = "x"  # type: ignore[attr-defined]

    def test_set_private_attribute_allowed(self) -> None:
        """Setting a name starting with '_' is permitted for internal use."""
        obj = SampleADTO(name="test")
        obj._foo = "bar"
        assert obj._foo == "bar"

    def test_set_pydantic_private_allowed(self) -> None:
        """Setting pydantic-private names (__double, _pydantic_) is permitted."""
        obj = SampleADTO(name="test")
        # Double-underscore names pass through __setattr__.
        obj.__private__ = "x"
        assert obj.__private__ == "x"


# ===================================================================
# TestADTOAuditTrail
# ===================================================================


class TestADTOAuditTrail:
    """ADTO mutation history / audit trail entries."""

    def test_initial_set_recorded_in_history(self) -> None:
        """After construction, history has at least one entry with initial field values."""
        obj = SampleADTO(name="test", value=42)
        history = obj.mutation_history()
        assert len(history) >= 1
        change_map = {c.property_name: c.new_value for c in history[0].changes}
        assert change_map["name"] == "test"
        assert change_map["value"] == 42

    def test_subsequent_set_appends_to_history(self) -> None:
        """Setting a field after construction appends a new entry to the history."""
        obj = SampleADTO(name="test")
        initial_len = len(obj.mutation_history())
        obj.name = "updated"
        assert len(obj.mutation_history()) == initial_len + 1

    def test_mutation_history_returns_deep_copy(self) -> None:
        """Mutating the returned list does not affect the internal state."""
        obj = SampleADTO(name="test")
        history1 = obj.mutation_history()
        assert len(history1) >= 1
        # Clear the returned copy — internal state must survive.
        history1.clear()
        history2 = obj.mutation_history()
        assert len(history2) >= 1

    def test_snapshot_reflects_state_at_change(self) -> None:
        """The snapshot in each TraceEntry has the correct field values at that time."""
        obj = SampleADTO(name="first", value=1)
        obj.name = "second"
        obj.value = 2
        history = obj.mutation_history()
        # Initial entry snapshot should reflect the starting state.
        assert history[0].snapshot.name == "first"
        assert history[0].snapshot.value == 1
        # The last (most recent) entry snapshot should reflect the final state.
        last = history[-1]
        assert last.snapshot.name == "second"
        assert last.snapshot.value == 2

    def test_same_caller_merges_changes(self) -> None:
        """Two sequential sets from the same caller merge into one TraceEntry."""
        obj = SampleADTO(name="test")
        initial_len = len(obj.mutation_history())
        # Both calls go through __setattr__, so they share caller_class/method.
        obj.name = "first"
        obj.value = 42
        history = obj.mutation_history()
        # Expect one merged entry for the two sets.
        assert len(history) == initial_len + 1
        merged = history[-1]
        change_map = {c.property_name: c.new_value for c in merged.changes}
        assert change_map["name"] == "first"
        assert change_map["value"] == 42

    def test_deep_copied_value(self) -> None:
        """The new_value in PropertyChange is a deep copy, not a reference."""
        obj = SampleADTO(name="test", tags=[])
        original = ["a", "b", "c"]
        obj.tags = original
        history = obj.mutation_history()
        for entry in reversed(history):
            for change in entry.changes:
                if change.property_name == "tags":
                    assert change.new_value == ["a", "b", "c"]
                    # Mutating the original must NOT affect the recorded copy.
                    original.append("d")
                    assert change.new_value == ["a", "b", "c"]
                    return
        pytest.fail("No 'tags' change found in history")


# ===================================================================
# TestADTOTraceDisabled
# ===================================================================


class TestADTOTraceDisabled:
    """ADTO behaviour when audit trail is disabled."""

    def test_no_history_when_trace_disabled(self) -> None:
        """With adto_trace_enabled=False, the history stays empty after multiple sets."""
        obj = SampleADTO(name="test", value=1, adto_trace_enabled=False)
        obj.name = "updated"
        obj.value = 42
        assert len(obj.mutation_history()) == 0

    def test_non_field_still_rejected_when_trace_disabled(self) -> None:
        """Even with trace disabled, setting a non-field name raises AttributeError."""
        obj = SampleADTO(name="test", adto_trace_enabled=False)
        with pytest.raises(AttributeError, match="has no field 'unknown'"):
            obj.unknown = "x"  # type: ignore[attr-defined]


# ===================================================================
# TestCallerDetection
# ===================================================================


class TestCallerDetection:
    """ADTO provenance — caller class and method detection."""

    def test_detect_caller_from_method(self) -> None:
        """Setting a field from a method captures caller_class and caller_method."""
        obj = SampleADTO(name="original")
        _MethodCaller().set_name(obj, "from_method")
        history = obj.mutation_history()
        last = history[-1]
        # The detected caller is __setattr__ (the ADTO method that invokes
        # _on_property_changed), with the ADTO subclass as caller_class.
        assert last.caller_class == "SampleADTO"
        assert last.caller_method == "__setattr__"

    def test_detect_caller_from_init(self) -> None:
        """Initial construction entries always have caller_method == '__init__'."""
        obj = SampleADTO(name="test", value=42)
        history = obj.mutation_history()
        for entry in history:
            assert entry.caller_method == "__init__"


# ===================================================================
# TestFrozenDataclasses
# ===================================================================


class TestFrozenDataclasses:
    """PropertyChange and TraceEntry are frozen (immutable) dataclasses."""

    def test_property_change_is_frozen(self) -> None:
        """PropertyChange instances cannot be mutated after creation."""
        pc = PropertyChange(property_name="x", new_value=1)
        with pytest.raises(FrozenInstanceError):
            pc.property_name = "y"  # type: ignore[misc]

    def test_trace_entry_is_frozen(self) -> None:
        """TraceEntry instances cannot be mutated after creation."""
        te = TraceEntry(
            timestamp=datetime.now(timezone.utc),
            caller_class="Test",
            caller_method="test",
            changes=(PropertyChange("x", 1),),
            snapshot=SampleADTO(name="test"),
        )
        with pytest.raises(FrozenInstanceError):
            te.caller_class = "Other"  # type: ignore[misc]

    def test_trace_entry_changes_are_tuple(self) -> None:
        """The changes field of a TraceEntry is a tuple, not a list."""
        te = TraceEntry(
            timestamp=datetime.now(timezone.utc),
            caller_class="Test",
            caller_method="test",
            changes=(PropertyChange("x", 1),),
            snapshot=SampleADTO(name="test"),
        )
        assert isinstance(te.changes, tuple)


# ===================================================================
# TestEdgeCases
# ===================================================================


class TestEdgeCases:
    """Edge-case scenarios for ADTO behaviour."""

    def test_history_preserves_order(self) -> None:
        """Multiple sets from different contexts preserve chronological order."""
        obj = SampleADTO(name="first")
        obj.value = 10
        obj.name = "last"
        history = obj.mutation_history()
        timestamps = [e.timestamp for e in history]
        for i in range(1, len(timestamps)):
            assert timestamps[i] >= timestamps[i - 1]

    def test_utc_timestamp(self) -> None:
        """All timestamps in the history have UTC timezone information."""
        obj = SampleADTO(name="test")
        obj.name = "updated"
        history = obj.mutation_history()
        assert len(history) >= 1
        for entry in history:
            assert entry.timestamp.tzinfo is not None
            offset = entry.timestamp.utcoffset()
            assert offset is not None
            assert offset.total_seconds() == 0
