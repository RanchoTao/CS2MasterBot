"""Interfaces for radar-like tactical and team policies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from cs2masterbot.data.schema import TeamObservation


TeamCommand = Literal[
    "hold",
    "regroup",
    "rotate_a",
    "rotate_b",
    "execute_a",
    "execute_b",
    "retake",
    "save",
]


@dataclass(frozen=True)
class PlayerDirective:
    player_id: str
    target_region: str
    urgency: float


@dataclass(frozen=True)
class RadarDecision:
    command: TeamCommand
    player_directives: tuple[PlayerDirective, ...]
    confidence: float


class RadarPolicy(Protocol):
    """High-level policy that consumes only team-observable state."""

    def predict(self, observation: TeamObservation) -> RadarDecision:
        observation.assert_information_bound()
        ...
