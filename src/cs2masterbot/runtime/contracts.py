"""Runtime contracts shared by offline replay and controlled interactive evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from cs2masterbot.data.schema import TeamObservation
from cs2masterbot.models.aim import AimAction
from cs2masterbot.models.radar import RadarDecision


@dataclass(frozen=True)
class RuntimeLimits:
    reaction_delay_ms: int = 200
    perception_hz: float = 30.0
    aim_action_hz: float = 20.0
    tactical_action_hz: float = 2.0

    def validate(self) -> None:
        if self.reaction_delay_ms < 0:
            raise ValueError("reaction_delay_ms must be non-negative")
        if min(self.perception_hz, self.aim_action_hz, self.tactical_action_hz) <= 0:
            raise ValueError("all runtime rates must be positive")


class TeamObservationSource(Protocol):
    def read(self) -> TeamObservation:
        ...


class AimActionSink(Protocol):
    def apply(self, action: AimAction) -> None:
        ...


class TacticalDecisionSink(Protocol):
    def apply(self, decision: RadarDecision) -> None:
        ...
