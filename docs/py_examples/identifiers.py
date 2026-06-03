"""Domain identifier examples: typed wrappers for primitive IDs (TIP-002).

A domain identifier is a concept, not a primitive. Its type must be distinct
from the primitive it wraps, so the type system can prevent accidental
interchange of IDs from different concepts.

This module uses frozen dataclasses with slots=True as wrapper types
instead of plain strings. UserId, OrderId, and TrialId are distinct types
even though all three wrap strings.

Boundary-crossing responses (create_user, create_order, create_trial)
return ADTOs (TIP-007), not raw dicts.
"""

from __future__ import annotations

from dataclasses import dataclass

from adto import ADTO


@dataclass(frozen=True, slots=True)
class UserId:
    """Domain identifier for users. Distinct type from OrderId, TrialId."""

    value: str


@dataclass(frozen=True, slots=True)
class OrderId:
    """Domain identifier for orders. Distinct type from UserId, TrialId."""

    value: str


@dataclass(frozen=True, slots=True)
class TrialId:
    """Domain identifier for tuning trials. Distinct type from UserId, OrderId."""

    value: str


class UserResponse(ADTO):
    """Typed, auditable response for create_user (TIP-007)."""

    user_id: str
    name: str


class OrderResponse(ADTO):
    """Typed, auditable response for create_order (TIP-007)."""

    user_id: str
    order_id: str
    amount: float


class TrialResult(ADTO):
    """Typed, auditable response for create_trial (TIP-007)."""

    trial_id: str
    metric: float


def create_user(user_id: UserId, name: str) -> UserResponse:
    """Create a user with a typed ID. Returns a typed ADTO."""
    return UserResponse(user_id=user_id.value, name=name)


def create_order(user_id: UserId, order_id: OrderId, amount: float) -> OrderResponse:
    """Create an order. Only accepts typed IDs. Returns a typed ADTO."""
    return OrderResponse(
        user_id=user_id.value,
        order_id=order_id.value,
        amount=amount,
    )


def create_trial(trial_id: TrialId, metric: float) -> TrialResult:
    """Record a trial outcome. Returns a typed ADTO."""
    return TrialResult(trial_id=trial_id.value, metric=metric)
