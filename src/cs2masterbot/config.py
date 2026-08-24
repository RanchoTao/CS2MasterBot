"""Configuration loading and safety checks for research experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    """Raised when an experiment config violates project invariants."""


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config and validate the core information-bound constraints."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}

    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    observation = config.get("observation", {})
    evaluation = config.get("evaluation", {})
    latency = config.get("latency", {})

    if observation.get("team_information_only", True) and observation.get(
        "include_hidden_enemy_ground_truth", False
    ):
        raise ConfigError(
            "Hidden enemy ground truth cannot be a policy input in a team-information-bounded run."
        )

    if evaluation.get("enforce_information_mask", True) and not observation.get(
        "team_information_only", True
    ):
        raise ConfigError(
            "Standard evaluation requires observation.team_information_only=true."
        )

    reaction_delay_ms = int(latency.get("reaction_delay_ms", 0))
    if reaction_delay_ms < 0:
        raise ConfigError("reaction_delay_ms must be non-negative.")

    for key in ("perception_hz", "aim_action_hz", "tactical_action_hz"):
        value = float(latency.get(key, 0))
        if value <= 0:
            raise ConfigError(f"latency.{key} must be positive.")
