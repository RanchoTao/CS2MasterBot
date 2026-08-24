"""Interfaces for short-horizon mechanics / aim policies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


@dataclass(frozen=True)
class AimInput:
    """A compact mechanics input window.

    `frames` is expected to have shape [T, H, W, C] when visual training is used.
    Auxiliary features are deliberately small so visual mechanics can be studied
    independently from tactical state.
    """

    frames: np.ndarray
    velocity_xyz: tuple[float, float, float]
    weapon_id: str
    previous_fire: bool


@dataclass(frozen=True)
class AimAction:
    delta_yaw: float
    delta_pitch: float
    fire: bool
    move_forward: float = 0.0
    move_right: float = 0.0
    crouch: bool = False


class AimPolicy(Protocol):
    """Runtime-agnostic interface implemented by mechanics models."""

    def predict(self, observation: AimInput) -> AimAction:
        ...
