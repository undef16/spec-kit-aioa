"""Tests for domain identifier examples (TIP-002 + TIP-007)."""

import pytest

from identifiers import (
    OrderId,
    TrialId,
    TrialResult,
    UserId,
    create_order,
    create_trial,
    create_user,
)


class TestDomainIdentifiers:
    """Domain identifiers are distinct typed wrappers, not bare primitives."""

    def test_create_user_with_typed_id(self):
        result = create_user(UserId("alice"), "Alice")
        assert isinstance(result.user_id, str)
        assert result.user_id == "alice"
        assert result.name == "Alice"

    def test_create_order_with_typed_ids(self):
        result = create_order(UserId("alice"), OrderId("ord-1"), 100.0)
        assert result.user_id == "alice"
        assert result.order_id == "ord-1"
        assert result.amount == 100.0

    def test_user_id_and_order_id_are_distinct_types(self):
        """UserId and OrderId are not interchangeable despite same structure."""
        assert UserId.__name__ != OrderId.__name__
        assert type(UserId("a")) is not type(OrderId("b"))

    @pytest.mark.parametrize("id_cls", [UserId, OrderId, TrialId])
    def test_id_is_immutable(self, id_cls):
        obj = id_cls("test")
        with pytest.raises(AttributeError):
            obj.value = "changed"  # type: ignore[attr-defined]

    def test_trial_id_is_separate_type(self):
        """TrialId is distinct from both UserId and OrderId."""
        assert TrialId.__name__ not in (UserId.__name__, OrderId.__name__)


class TestTypedResponses:
    """Boundary-crossing responses are typed ADTOs (TIP-007)."""

    def test_user_response_has_mutation_history(self):
        result = create_user(UserId("alice"), "Alice")
        history = result.mutation_history()
        # Initial fields are audited.
        assert len(history) >= 1

    def test_order_response_has_mutation_history(self):
        result = create_order(UserId("alice"), OrderId("ord-1"), 100.0)
        history = result.mutation_history()
        assert len(history) >= 1

    def test_trial_result_has_mutation_history(self):
        result = create_trial(TrialId("t-001"), 0.95)
        assert result.trial_id == "t-001"
        assert result.metric == 0.95
        assert len(result.mutation_history()) >= 1


