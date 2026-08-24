"""Canonical observation schema for offline and streaming CS2 research."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


Team = Literal["T", "CT"]


@dataclass(frozen=True)
class Vec3:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class PlayerObservation:
    player_id: str
    team: Team
    position: Vec3 | None
    yaw: float | None
    pitch: float | None
    alive: bool
    observed: bool
    last_observed_ms: int | None = None


@dataclass(frozen=True)
class PublicRoundState:
    tick: int
    round_time_s: float
    score_t: int
    score_ct: int
    bomb_planted: bool = False
    bombsite: str | None = None


@dataclass(frozen=True)
class TeamObservation:
    """Policy-facing state containing only information available to one team."""

    observing_team: Team
    round_state: PublicRoundState
    teammates: tuple[PlayerObservation, ...] = field(default_factory=tuple)
    enemies: tuple[PlayerObservation, ...] = field(default_factory=tuple)

    def assert_information_bound(self) -> None:
        """Reject hidden enemy coordinates/orientation accidentally leaked from demos."""
        for enemy in self.enemies:
            if enemy.team == self.observing_team:
                raise ValueError("Enemy list contains a player from the observing team.")
            if not enemy.observed and any(
                value is not None
                for value in (enemy.position, enemy.yaw, enemy.pitch)
            ):
                raise ValueError(
                    "Privileged enemy state leaked into an unobserved policy input."
                )

        for teammate in self.teammates:
            if teammate.team != self.observing_team:
                raise ValueError("Teammate list contains a player from the opposing team.")


@dataclass(frozen=True)
class PrivilegedTarget:
    """Training/evaluation-only target that must never be fed into the policy."""

    player_id: str
    position: Vec3
    yaw: float
    pitch: float


@dataclass(frozen=True)
class ReplaySample:
    observation: TeamObservation
    privileged_targets: tuple[PrivilegedTarget, ...] = field(default_factory=tuple)

    def validate(self) -> None:
        self.observation.assert_information_bound()
