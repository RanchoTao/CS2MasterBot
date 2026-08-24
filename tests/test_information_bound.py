from cs2masterbot.data.schema import (
    PlayerObservation,
    PublicRoundState,
    TeamObservation,
    Vec3,
)


def _round() -> PublicRoundState:
    return PublicRoundState(
        tick=128,
        round_time_s=75.0,
        score_t=3,
        score_ct=4,
    )


def test_hidden_enemy_without_coordinates_is_valid() -> None:
    obs = TeamObservation(
        observing_team="T",
        round_state=_round(),
        enemies=(
            PlayerObservation(
                player_id="enemy-1",
                team="CT",
                position=None,
                yaw=None,
                pitch=None,
                alive=True,
                observed=False,
            ),
        ),
    )
    obs.assert_information_bound()


def test_hidden_enemy_coordinates_are_rejected() -> None:
    obs = TeamObservation(
        observing_team="T",
        round_state=_round(),
        enemies=(
            PlayerObservation(
                player_id="enemy-1",
                team="CT",
                position=Vec3(100.0, 200.0, 0.0),
                yaw=90.0,
                pitch=0.0,
                alive=True,
                observed=False,
            ),
        ),
    )

    try:
        obs.assert_information_bound()
    except ValueError as exc:
        assert "Privileged enemy state leaked" in str(exc)
    else:
        raise AssertionError("Hidden enemy coordinates should be rejected")
