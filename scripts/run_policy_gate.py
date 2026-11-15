#!/usr/bin/env python3
"""Evaluate an architecture against the local LexCode policy source."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lexcode.policy import evaluate_policy  # noqa: E402


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=ROOT / "lexcode/dsl/sample_internal_policy.json")
    parser.add_argument("--architecture", type=Path, required=True)
    args = parser.parse_args()

    result = evaluate_policy(read_json(args.policy), read_json(args.architecture))
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
