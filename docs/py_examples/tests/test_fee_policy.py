"""Tests for policy mechanism example (TIP-006 + TIP-007)."""

import pytest

from fee_policy import (
    FeeCalculator,
    FeeQuote,
    FlatFee,
    PercentageFee,
    TieredFee,
)


class TestFlatFee:
    def test_fixed_fee(self):
        fee = FlatFee(10.0)
        assert fee.calculate(100.0) == 10.0
        assert fee.calculate(1000.0) == 10.0

    def test_zero_fee(self):
        fee = FlatFee(0.0)
        assert fee.calculate(100.0) == 0.0

    def test_negative_fee_raises_error(self):
        with pytest.raises(ValueError, match="Fee must be non-negative"):
            FlatFee(-1.0)


class TestPercentageFee:
    def test_percentage_of_amount(self):
        fee = PercentageFee(0.01)
        assert fee.calculate(100.0) == 1.0
        assert fee.calculate(1000.0) == 10.0

    def test_zero_percent(self):
        fee = PercentageFee(0.0)
        assert fee.calculate(100.0) == 0.0

    def test_full_percent(self):
        fee = PercentageFee(1.0)
        assert fee.calculate(100.0) == 100.0

    def test_invalid_rate_raises_error(self):
        with pytest.raises(ValueError, match="Rate must be between 0 and 1"):
            PercentageFee(1.5)


class TestTieredFee:
    def test_first_tier_low_amount(self):
        fee = TieredFee([(100, 0.05), (1000, 0.02)])
        assert fee.calculate(50.0) == 2.5

    def test_second_tier_mid_amount(self):
        fee = TieredFee([(100, 0.05), (1000, 0.02)])
        assert fee.calculate(500.0) == 10.0

    def test_beyond_all_tiers(self):
        fee = TieredFee([(100, 0.05), (1000, 0.02)])
        assert fee.calculate(2000.0) == 40.0

    def test_single_tier(self):
        fee = TieredFee([(1000, 0.01)])
        assert fee.calculate(500.0) == 5.0
        assert fee.calculate(2000.0) == 20.0

    def test_empty_tiers_raises_error(self):
        with pytest.raises(ValueError, match="At least one tier is required"):
            TieredFee([])

    def test_negative_threshold_raises_error(self):
        with pytest.raises(ValueError, match="Tier threshold must be non-negative"):
            TieredFee([(-1.0, 0.05)])

    def test_rate_above_one_raises_error(self):
        with pytest.raises(ValueError, match="Tier rate must be in"):
            TieredFee([(100, 1.5)])

    def test_negative_rate_raises_error(self):
        with pytest.raises(ValueError, match="Tier rate must be in"):
            TieredFee([(100, -0.1)])


class TestFeeCalculator:
    """Business logic returns typed ADTO (TIP-007) and is policy-agnostic (TIP-006)."""

    def test_flat_fee_policy(self):
        calc = FeeCalculator(FlatFee(10.0))
        result = calc.calculate_total(100.0)
        assert isinstance(result, FeeQuote)
        assert result.original_amount == 100.0
        assert result.fee == 10.0
        assert result.total == 110.0
        assert result.policy_type == "FlatFee"

    def test_percentage_fee_policy(self):
        calc = FeeCalculator(PercentageFee(0.1))
        result = calc.calculate_total(100.0)
        assert isinstance(result, FeeQuote)
        assert result.fee == 10.0
        assert result.total == 110.0
        assert result.policy_type == "PercentageFee"

    def test_tiered_fee_policy(self):
        calc = FeeCalculator(TieredFee([(100, 0.05), (1000, 0.02)]))
        result = calc.calculate_total(500.0)
        assert isinstance(result, FeeQuote)
        assert result.fee == 10.0
        assert result.total == 510.0
        assert result.policy_type == "TieredFee"

    def test_policy_swappable_at_runtime(self):
        calc = FeeCalculator(FlatFee(10.0))
        assert calc.calculate_total(100.0).policy_type == "FlatFee"

        calc.policy = PercentageFee(0.1)
        result = calc.calculate_total(100.0)
        assert result.policy_type == "PercentageFee"
        assert result.fee == 10.0

    def test_policy_setter_rejects_non_policy(self):
        calc = FeeCalculator(FlatFee(10.0))
        with pytest.raises(TypeError, match="policy must be a FeePolicy"):
            calc.policy = "not a policy"  # type: ignore[assignment]
