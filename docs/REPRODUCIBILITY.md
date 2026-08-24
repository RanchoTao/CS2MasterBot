# Reproducibility Contract

Every released CS2MasterBot result should be reproducible from a small, versioned bundle of artifacts rather than from undocumented local state.

## Required release artifacts

For each named checkpoint or reported experiment, publish:

1. **Config** — exact YAML used for preprocessing, model construction, training, and evaluation.
2. **Checkpoint** — model weights with a stable version/name.
3. **Dataset manifest** — demo identifiers, hashes where practical, source metadata, and split assignment.
4. **Preprocessing version** — commit SHA and schema version used to build training samples.
5. **Evaluation protocol** — metrics, latency/action limits, information mask, and test split definition.
6. **Environment metadata** — Python, CUDA, framework versions, GPU model, and relevant driver/runtime information.
7. **Result file** — machine-readable metrics plus a short human-readable summary.

## Checkpoint naming

Suggested convention:

```text
<component>-<map_or_scope>-<architecture>-v<major>.<minor>
```

Examples:

```text
radar-mirage-smalltx-v0.1
aim-dm-smalltx-v0.1
```

## Model card metadata

Each checkpoint should document at least:

```yaml
name: radar-mirage-smalltx-v0.1
commit: <git-sha>
config: configs/experiments/radar-mirage-v0.1.yaml
schema_version: 1
dataset_manifest: manifests/radar-mirage-v0.1.jsonl
trained_on:
  maps: [de_mirage]
  split: train
constraints:
  team_information_only: true
  reaction_delay_ms: 200
metrics:
  next_region_accuracy: null
  trajectory_error: null
license: TBD
```

## Data manifests

Do not commit large raw demo collections into Git. A manifest should make the dataset auditable without bloating the repository.

Recommended fields:

```json
{
  "match_id": "...",
  "source": "...",
  "map": "de_mirage",
  "date": "YYYY-MM-DD",
  "demo_sha256": "...",
  "split": "train",
  "schema_version": 1
}
```

If a data source cannot legally or practically be redistributed, publish the acquisition/selection procedure and the manifest metadata that can be shared.

## Determinism

Where feasible, record:
- random seed,
- deterministic framework settings,
- data-order seed,
- model initialization seed.

Exact bitwise reproduction across different GPUs is not guaranteed; metric-level reproduction within documented tolerance is the target.

## Information-bound audit

Every evaluation config must state whether the policy could access:
- hidden enemy position,
- hidden enemy orientation,
- server memory/state unavailable to a human,
- future replay information,
- information from other agents beyond the defined team-sharing channel.

A standard benchmark result is valid only when all privileged policy inputs are disabled.

## Release workflow

Target release flow:

```bash
git clone https://github.com/RanchoTao/CS2MasterBot
cd CS2MasterBot
pip install -e '.[train]'

# acquire/preprocess data according to the published manifest
python scripts/prepare_demos.py --config configs/base.yaml

# later: train/evaluate entry points will follow the same config contract
```

Large checkpoints should be distributed through a model/checkpoint hosting service or GitHub Releases rather than committed directly to the repository.
