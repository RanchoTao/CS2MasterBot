# CS2MasterBot

CS2MasterBot is a research-oriented project for building a **human-information-bounded Counter-Strike 2 agent** from replay data, visual observations, and lightweight online interaction.

The long-term goal is not to create a memory-reading or anti-cheat-bypassing bot. The research question is stricter:

> How strong can an AI team become if it only receives information a human player/team could legitimately obtain, while its reaction and action bandwidth are explicitly bounded?

The project starts from a single-GPU, offline-first setup and scales only when the core hypotheses are validated.

## Core principles

1. **No game-memory reads or hidden-state access at inference time.**
2. **No anti-cheat bypass work.** Live evaluation should be restricted to private/local research environments.
3. **Human-information-bounded observations.** Enemy information must be masked unless it would be observable to the team.
4. **Explicit reaction constraints.** Experiments should report latency, observation rate, and action rate.
5. **Replay-first learning.** Use high-skill and professional demos for imitation/pretraining before expensive reinforcement learning.
6. **Modular before end-to-end.** Separate mechanics, tactical state estimation, team policy, and runtime control.
7. **Reproducibility first.** Public configs, deterministic evaluation protocols, checkpoint metadata, and dataset manifests are first-class artifacts.

## Initial research decomposition

### A. Aim / mechanics policy

Goal: learn stable short-horizon combat behavior from visual or replay-derived supervision.

Inputs may include:
- recent first-person frames,
- player motion state available from recorded training data,
- weapon state,
- short action history.

Outputs may include:
- view delta,
- fire/no-fire,
- movement/action decisions.

The first benchmark should be a constrained deathmatch setting because it provides dense combat samples and simple feedback.

### B. Radar / tactical policy

Goal: model high-level team behavior using a much lower-dimensional observation space.

Inputs may include:
- teammates' positions and orientations,
- legally observed enemy information,
- last-known enemy positions,
- round timer / score / economy features,
- recent events and compact memory.

Outputs may include:
- region-level movement,
- rotate / hold / regroup decisions,
- formation changes,
- opponent location beliefs,
- high-level team commands.

Professional demos are especially valuable here because they contain strong priors for spacing, timing, rotations, retakes, saves, and opponent-specific tendencies.

## Architecture

```text
                Offline Demos / Recorded POV
                         |
                         v
                +-------------------+
                | Demo / POV Parser |
                +-------------------+
                         |
                         v
                +-------------------+
                | Canonical Dataset |
                | + visibility mask |
                +-------------------+
                   |             |
                   |             |
                   v             v
          +---------------+   +----------------+
          | Aim / Combat  |   | Radar / Team   |
          | Policy        |   | Policy         |
          +---------------+   +----------------+
                   |             |
                   +------v------+
                          |
                  +---------------+
                  | Runtime Agent |
                  | latency limits|
                  +---------------+
                          |
                          v
                  Private evaluation
```

The tactical model should never receive omniscient demo state as an input feature. Ground-truth hidden positions may be retained only as labels or evaluation targets.

## Repository layout

```text
configs/                  Experiment configuration
scripts/                  Data preparation / training entry points
src/cs2masterbot/
  data/                    Demo schema and dataset interfaces
  models/                  Aim and radar policy interfaces
  runtime/                 Observation/action contracts
  eval/                    Reproducible evaluation protocol

docs/
  RESEARCH_PLAN.md         Research roadmap and hypotheses
  REPRODUCIBILITY.md       Checkpoint/config/dataset release contract
```

## MVP roadmap

### Phase 0 — Data pipeline
- Parse a small batch of demos from one map.
- Export tick/event/player trajectories into a canonical schema.
- Build a **team-observable mask** so hidden enemy state cannot leak into policy inputs.
- Visualize trajectories and verify data quality manually.

### Phase 1 — Offline baselines
- Train a next-region / next-action tactical baseline from radar-like state.
- Train a short-horizon aim/action imitation baseline from dense combat samples.
- Establish train/validation/test splits by match and player/team identity.

### Phase 2 — Streaming inference
- Consume observations incrementally rather than loading the full round.
- Maintain a compact belief/memory state.
- Enforce configurable reaction delay and action rate.

### Phase 3 — Private interactive evaluation
- Connect policies to a controlled local/private environment.
- Compare against fixed bots and human baselines.
- Add limited RL/self-play only where offline imitation stops improving.

### Phase 4 — Multi-agent team
- Five coordinated agents with shared bounded information.
- Opponent modeling from historical demos.
- Generalization tests across maps, teams, patches, and unseen tactical patterns.

## Evaluation priorities

A strong result should report more than win rate:

- reaction latency and action frequency,
- combat accuracy / time-to-damage,
- positional prediction accuracy,
- calibration of enemy-location belief,
- round win rate under fixed constraints,
- performance variance across long sessions,
- generalization to held-out matches / teams / maps,
- ablations for memory, opponent modeling, and coordination.

## Reproducibility target

The intended release format is similar to modern model repositories:

```bash
# example target workflow (not implemented yet)
git clone https://github.com/RanchoTao/CS2MasterBot
cd CS2MasterBot
pip install -e .

# download released checkpoint(s) separately
# python scripts/prepare_demos.py --config configs/base.yaml
# python scripts/evaluate.py --config configs/base.yaml --checkpoint <path>
```

A released result should be reproducible from:

- a versioned config,
- checkpoint weights,
- preprocessing version,
- dataset manifest / split definition,
- evaluation protocol,
- hardware/software metadata.

See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Status

**Very early research scaffold.** The immediate objective is to validate the demo-to-dataset pipeline and define a leakage-free observation space before spending significant compute on training.

## Scope note

CS2MasterBot is intended for AI research, offline replay analysis, and controlled private evaluation. The repository should not contain anti-cheat bypasses, memory-reading cheats, or instructions for deploying an unfair agent into public matchmaking.
