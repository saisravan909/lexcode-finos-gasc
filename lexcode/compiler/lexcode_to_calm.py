#!/usr/bin/env python3
"""Compile a LexCode policy into CALM control requirements."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


CONTROL_REQUIREMENT_URL = "https://calm.finos.org/release/1.3/meta/control-requirement.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def compile_policy(policy: dict[str, Any], architecture: dict[str, Any]) -> dict[str, Any]:
    if not policy.get("policy_id") or not policy.get("version"):
        raise ValueError("Policy must define policy_id and version")
    rules = policy.get("rules")
    if not isinstance(rules, list) or not rules:
        raise ValueError("Policy must contain at least one rule")

    compiled = copy.deepcopy(architecture)
    compiled["$schema"] = "https://calm.finos.org/release/1.3/meta/calm.json"
    requirements = []
    for rule in rules:
        requirements.append(
            {
                "requirement-url": CONTROL_REQUIREMENT_URL,
                "config": {
                    "control-id": rule["id"],
                    "name": rule["title"],
                    "description": rule["description"],
                    "policy-id": policy["policy_id"],
                    "policy-version": policy["version"],
                    "evaluation": {
                        "scope": rule["scope"],
                        "field": rule["field"],
                        "operator": rule["operator"],
                        "expected": rule["expected"],
                    },
                    "ccc-mappings": rule.get("ccc_mappings", []),
                    "aigf-reference": rule.get("aigf_reference"),
                },
            }
        )
    compiled["controls"] = {
        "lexcode-policy-controls": {
            "description": (
                f"Generated from {policy['policy_id']} version {policy['version']}. "
                "Policy checks are internal controls and do not assert legal compliance."
            ),
            "requirements": requirements,
        }
    }
    return compiled


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    parser.add_argument("architecture", type=Path, help="Base CALM architecture JSON")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    policy = load_json(args.policy)
    architecture = load_json(args.architecture)
    result = compile_policy(policy, architecture)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        f"[LexCode] Compiled {len(policy['rules'])} internal policy controls "
        f"into {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
