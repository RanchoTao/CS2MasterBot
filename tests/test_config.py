from cs2masterbot.config import ConfigError, validate_config


def test_standard_config_rejects_hidden_enemy_ground_truth() -> None:
    config = {
        "observation": {
            "team_information_only": True,
            "include_hidden_enemy_ground_truth": True,
        },
        "evaluation": {"enforce_information_mask": True},
        "latency": {
            "reaction_delay_ms": 200,
            "perception_hz": 30,
            "aim_action_hz": 20,
            "tactical_action_hz": 2,
        },
    }

    try:
        validate_config(config)
    except ConfigError as exc:
        assert "Hidden enemy ground truth" in str(exc)
    else:
        raise AssertionError("Privileged inputs should invalidate the config")
