#!/usr/bin/env python3
"""Prepare replay data into the canonical CS2MasterBot dataset format.

This is intentionally a thin scaffold. A concrete parser adapter (for example,
Awpy/demoparser2 or another maintained CS2 demo parser) should be implemented
behind the same output schema without exposing privileged state to policy inputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from cs2masterbot.config import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare CS2 demos for CS2MasterBot")
    parser.add_argument("--config", default="configs/base.yaml")
    parser.add_argument("--input", default=None, help="Directory containing local .dem files")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    data_config = config["data"]

    raw_dir = Path(args.input or data_config["raw_dir"])
    processed_dir = Path(data_config["processed_dir"])
    manifest = Path(data_config["manifest"])

    print(f"Raw demos:       {raw_dir}")
    print(f"Processed data:  {processed_dir}")
    print(f"Manifest:        {manifest}")
    print(
        "Information bound:",
        "team-only" if config["observation"]["team_information_only"] else "unbounded",
    )

    if args.dry_run:
        return

    processed_dir.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)

    demos = sorted(raw_dir.glob("*.dem")) if raw_dir.exists() else []
    if not demos:
        raise SystemExit(
            f"No .dem files found in {raw_dir}. Add local research demos and rerun."
        )

    raise SystemExit(
        "Demo discovery works, but parser conversion is intentionally not implemented yet. "
        "Next step: add a parser adapter that emits observable_state and privileged_target separately."
    )


if __name__ == "__main__":
    main()
