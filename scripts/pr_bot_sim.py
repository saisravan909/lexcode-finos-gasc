#!/usr/bin/env python3
"""Write a local preview of a policy failure comment. This never calls GitHub."""

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
    parser.add_argument("--architecture", type=Path, default=ROOT / "tests/invalid_arch.calm.json")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/pr_comment_preview.md")
    args = parser.parse_args()

    policy = read_json(args.policy)
    result = evaluate_policy(policy, read_json(args.architecture))
    failures = [check for check in result["checks"] if check["status"] == "FAIL"]
    if not failures:
        print("[PR preview] No comment needed because the policy check passed.")
        return 1

    lines = [
        "## LexCode policy gate: review required",
        "",
        "The submitted architecture failed the synthetic organization policy. This is not a legal finding.",
        "",
        "| Rule | Subject | Expected | Observed | Related catalog control |",
        "| --- | --- | --- | --- | --- |",
    ]
    for failure in failures:
        mapping_ids = ", ".join(item["id"] for item in failure["ccc_mappings"]) or "None stated"
        lines.append(
            f"| {failure['title']} | {failure['subject']} | `{failure['expected']}` | "
            f"`{failure['observed']}` | `{mapping_ids}` |"
        )
    lines.extend(
        [
            "",
            "Action: correct the architecture or request a policy exception through the organization process.",
            "This file is a preview only. The script does not post comments or contact GitHub.",
            "",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"[PR preview] Wrote {len(failures)} policy findings to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
