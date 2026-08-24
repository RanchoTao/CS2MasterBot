"""Evaluation records and checks for comparable CS2MasterBot experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class BenchmarkConstraints:
    observation_source: str
    reaction_delay_ms: int
    perception_hz: float
    aim_action_hz: float
    tactical_action_hz: float
    team_information_only: bool
    privileged_policy_inputs: bool = False

    def validate_standard(self) -> None:
        if not self.team_information_only:
            raise ValueError("Standard benchmark requires team-information-bounded observations.")
        if self.privileged_policy_inputs:
            raise ValueError("Privileged policy inputs invalidate the standard benchmark.")
        if self.reaction_delay_ms < 0:
            raise ValueError("reaction_delay_ms must be non-negative.")


@dataclass(frozen=True)
class BenchmarkResult:
    experiment_name: str
    checkpoint: str
    commit: str
    hardware: str
    constraints: BenchmarkConstraints
    metrics: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        self.constraints.validate_standard()
        return asdict(self)
