from dataclasses import asdict
from pathlib import Path

import pytest

from cs2masterbot.config import load_config
from cs2masterbot.runtime.contracts import RuntimeLimits

FIELDS = ("reaction_delay_ms", "perception_hz", "aim_action_hz", "tactical_action_hz")
RATE_FIELDS = FIELDS[1:]


def test_defaults_remain_valid() -> None:
    limits = RuntimeLimits()
    assert asdict(limits) == {
        "reaction_delay_ms": 200,
        "perception_hz": 30.0,
        "aim_action_hz": 20.0,
        "tactical_action_hz": 2.0,
    }
    assert limits.validate() is None


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_limits_are_rejected(field: str, value: float) -> None:
    with pytest.raises(ValueError):
        RuntimeLimits(**{field: value}).validate()


@pytest.mark.parametrize("field", RATE_FIELDS)
@pytest.mark.parametrize("value", [0, -0.0, -0.01, -1])
def test_zero_and_negative_rates_are_rejected(field: str, value: float) -> None:
    with pytest.raises(ValueError, match="all runtime rates must be positive"):
        RuntimeLimits(**{field: value}).validate()


@pytest.mark.parametrize("value", [-1, -0.001, -(10**1000)])
def test_negative_delay_is_rejected(value: float) -> None:
    with pytest.raises(ValueError, match="reaction_delay_ms must be non-negative"):
        RuntimeLimits(reaction_delay_ms=value).validate()


@pytest.mark.parametrize("value", [0, 0.0, 0.5, 1, 199, 200, 10**1000])
def test_finite_nonnegative_delay_is_valid(value: float) -> None:
    assert RuntimeLimits(reaction_delay_ms=value).validate() is None


@pytest.mark.parametrize("field", RATE_FIELDS)
@pytest.mark.parametrize("value", [0.1, 1, 1.7e308, 5e-324, 10**1000])
def test_finite_positive_rates_are_valid(field: str, value: float) -> None:
    assert RuntimeLimits(**{field: value}).validate() is None


def test_nan_cannot_mask_a_negative_rate() -> None:
    with pytest.raises(ValueError):
        RuntimeLimits(perception_hz=float("nan"), aim_action_hz=-1).validate()


def test_repository_latency_config_satisfies_runtime_contract() -> None:
    config_path = Path(__file__).resolve().parents[1] / "configs" / "base.yaml"
    config = load_config(config_path)
    limits = RuntimeLimits(**config["latency"])
    assert limits.validate() is None
    assert limits == RuntimeLimits()
