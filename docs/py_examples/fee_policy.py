"""Policy mechanism example: strategy pattern separating policy from business logic (TIP-006).

TIP-006 (Declarative Straight-Line Code) requires that execution mechanics
(retry, fallback, timeouts, fee calculation policies) are extracted into
separate abstractions. Business code stays linear and declarative.

This module demonstrates the Strategy pattern: different fee calculation
strategies (FlatFee, PercentageFee, TieredFee) are interchangeable policies
injected into a FeeCalculator. The calculator's business logic never changes
when a new fee policy is added.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from adto import ADTO


class FeePolicy(ABC):
    """Abstract policy for fee calculation.

    New fee policies are added by subclassing FeePolicy, not by
    modifying business code (open/closed principle).
    """

    @abstractmethod
    def calculate(self, amount: float) -> float:
        """Calculate fee for a given transaction amount."""
        ...


class FlatFee(FeePolicy):
    """A fixed fee regardless of transaction amount."""

    def __init__(self, fee: float) -> None:
        if fee < 0:
            raise ValueError(f"Fee must be non-negative, got {fee}")
        self._fee = fee

    def calculate(self, amount: float) -> float:
        return self._fee


class PercentageFee(FeePolicy):
    """A percentage of the transaction amount."""

    def __init__(self, rate: float) -> None:
        if not 0 <= rate <= 1:
            raise ValueError(f"Rate must be between 0 and 1, got {rate}")
        self._rate = rate

    def calculate(self, amount: float) -> float:
        return amount * self._rate


class TieredFee(FeePolicy):
    """A tiered fee: different rates for different amount thresholds.

    Example:
        TieredFee([(100, 0.05), (1000, 0.02)])
        - amount <= 100  \u2192 5%
        - amount <= 1000 \u2192 2%
        - amount > 1000  \u2192 2% (last tier's rate)
    """

    def __init__(self, tiers: list[tuple[float, float]]) -> None:
        if not tiers:
            raise ValueError("At least one tier is required")
        # Validate all thresholds and rates up front \u2014 Parse, Don't Validate.
        for threshold, rate in tiers:
            if threshold < 0:
                raise ValueError(f"Tier threshold must be non-negative, got {threshold}")
            if not 0 <= rate <= 1:
                raise ValueError(f"Tier rate must be in [0, 1], got {rate}")
        self._tiers = sorted(tiers, key=lambda t: t[0])

    def calculate(self, amount: float) -> float:
        for threshold, rate in self._tiers:
            if amount <= threshold:
                return amount * rate
        # Amount exceeds all thresholds \u2014 use the last tier's rate.
        return amount * self._tiers[-1][1]


class FeeQuote(ADTO):
    """Typed, auditable fee calculation result (TIP-007).

    Boundary-crossing data must be a typed ADTO, not a raw dict.
    """

    original_amount: float
    fee: float
    total: float
    policy_type: str


class FeeCalculator:
    """Business logic that delegates fee calculation to a policy.

    The calculator's business code stays linear and declarative.
    Policies can be swapped at runtime without changing the calculator.
    """

    def __init__(self, policy: FeePolicy) -> None:
        self._policy = policy

    @property
    def policy(self) -> FeePolicy:
        """Currently active fee policy."""
        return self._policy

    @policy.setter
    def policy(self, policy: FeePolicy) -> None:
        """Swap the fee policy at runtime.

        Raises TypeError if the new policy is not a FeePolicy subclass \u2014
        type validation at the boundary (Parse, Don't Validate).
        """
        if not isinstance(policy, FeePolicy):
            raise TypeError(
                f"policy must be a FeePolicy instance, got {type(policy).__name__}"
            )
        self._policy = policy

    def calculate_total(self, amount: float) -> FeeQuote:
        """Calculate fee and total amount using the current policy.

        Business logic is one line: the policy handles the variation.
        Returns a typed ADTO (TIP-007), not a raw dict.
        """
        fee = self._policy.calculate(amount)
        return FeeQuote(
            original_amount=amount,
            fee=fee,
            total=amount + fee,
            policy_type=type(self._policy).__name__,
        )
