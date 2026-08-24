# CS2MasterBot Research Plan

## 1. Research question

Can a Counter-Strike 2 agent become competitive under a strict **human-information-bound** interface, without reading privileged game memory, while keeping reaction speed and action bandwidth explicitly constrained?

The project should separate two questions:

1. Can mechanics be learned cheaply from dense replay / POV data?
2. Can team tactics be learned from long-horizon, partially observed replay sequences?

The initial goal is not a full 5v5 autonomous team. The goal is to validate the smallest useful components on one consumer GPU.

## 2. Working hypotheses

### H1 — Replay-first learning is enough for useful mechanics priors
A compact imitation model trained on dense combat windows should learn useful aim, fire timing, and movement priors without expensive online RL from scratch.

### H2 — Radar-like observations are sufficient for a meaningful tactical baseline
A low-dimensional team-observable state should predict future region occupancy and high-level decisions better than frequency and velocity baselines.

### H3 — Streaming memory matters
A model with bounded temporal memory should outperform a memoryless policy on rotations, retakes, saves, and opponent-location belief.

### H4 — Opponent modeling improves held-out tactical prediction
Historical team/player tendencies should improve prediction only if evaluation is split strictly by future matches and no test-match information leaks into training.

### H5 — Offline pretraining can reduce later interactive training cost
If aim and tactical priors are learned offline, local/private RL or self-play should be used only for residual adaptation rather than learning the game from zero.

## 3. Data strategy

### Initial sources
- Public professional demos.
- High-skill matchmaking/platform demos where collection and use are permitted.
- Self-recorded POV/deathmatch sessions for dense mechanics data.

### Canonical processing rule
Raw demo state may contain omniscient ground truth. The dataset builder must derive two separate views:

- `observable_state`: information available to the player/team at that moment.
- `privileged_label`: hidden ground truth used only for supervision or evaluation.

A policy input must never contain `privileged_label` fields.

### Split policy
At minimum, split by full match rather than random ticks. Stronger evaluations should additionally hold out:
- teams,
- players,
- tournaments/time periods,
- maps,
- tactical patterns where feasible.

## 4. MVP sequence

### Milestone 0 — Parse and inspect
Deliverables:
- 10+ demos from one map,
- canonical player/event schema,
- trajectory visualization,
- visibility/information masking tests.

Go/no-go criterion: manually inspected rounds match the source replay and hidden enemy information does not appear in policy inputs.

### Milestone 1 — Tactical prediction baseline
Tasks:
- predict each player's next map region,
- predict rotate/hold/regroup-like high-level labels,
- compare against last-position, velocity, and empirical-frequency baselines.

Go/no-go criterion: learned model beats trivial baselines on held-out matches.

### Milestone 2 — Mechanics imitation baseline
Tasks:
- extract short combat windows,
- learn view delta / fire timing / movement actions,
- evaluate offline first,
- later evaluate in a controlled deathmatch environment.

Go/no-go criterion: stable closed-loop behavior without privileged inputs and within the latency budget.

### Milestone 3 — Streaming belief state
Tasks:
- incremental observations only,
- bounded memory,
- enemy-location belief distribution,
- event compression / memory ablation.

Go/no-go criterion: memory improves tactical prediction and belief calibration on held-out rounds.

### Milestone 4 — Controlled interactive agent
Tasks:
- connect tactical and mechanics policies,
- enforce 200 ms reaction delay by default,
- cap observation and action rates,
- test only in local/private research environments.

### Milestone 5 — Multi-agent coordination
Tasks:
- shared team belief state,
- five role-conditioned policies or one parameter-shared policy,
- explicit coordination objectives,
- opponent-specific adaptation without test leakage.

## 5. Baselines

Always keep cheap baselines. They are required to know whether a neural model is actually learning something meaningful.

Suggested baselines:
- last observed position,
- constant velocity extrapolation,
- region transition matrix,
- empirical action prior by map/side/economy,
- small MLP/LSTM,
- small Transformer.

Do not begin with a large VLM unless the lower-dimensional baselines fail for reasons that require richer visual information.

## 6. Evaluation

### Mechanics
- target detection / tracking quality where applicable,
- view-delta error,
- fire timing error,
- time-to-damage,
- hit/headshot rates in controlled evaluation,
- performance variance across long sessions.

### Tactical modeling
- next-region accuracy,
- trajectory distance error,
- action classification F1,
- enemy-location belief calibration,
- round-outcome value prediction if added,
- held-out team/map generalization.

### System constraints
Every interactive result should report:
- observation source,
- observation frequency,
- action frequency,
- enforced reaction delay,
- hardware,
- model size,
- inference latency,
- whether any privileged state was available.

## 7. Compute strategy

The project should be designed so that a useful paper-quality prototype is possible on one consumer GPU:

1. parse demos on CPU,
2. cache compact tensors instead of raw rendered video when possible,
3. train small baselines first,
4. use mixed precision,
5. sample combat windows rather than repeatedly decoding entire matches,
6. use offline imitation before online RL,
7. scale only after an experiment shows a measurable bottleneck.

## 8. Publication-quality standard

A convincing result is not "the bot got many kills." It should demonstrate a controlled claim such as:

- bounded-memory tactical prediction improves over strong baselines,
- human-information masking still permits useful opponent belief estimation,
- offline replay pretraining reduces interactive sample requirements,
- coordinated agents outperform independent agents under the same information/action constraints.

The strongest long-term benchmark would compare AI and human teams under explicitly matched information and reaction constraints.
