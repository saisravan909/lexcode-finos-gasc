#!/usr/bin/env python3
"""Create a content addressed record for a passing synthetic policy check."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_revision() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=ROOT / "lexcode/dsl/sample_internal_policy.json")
    parser.add_argument("--architecture", type=Path, default=ROOT / "tests/valid_arch.calm.json")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/audit_attestation.json")
    args = parser.parse_args()

    policy = read_json(args.policy)
    architecture = read_json(args.architecture)
    result = evaluate_policy(policy, architecture)
    if result["status"] != "PASS":
        print("[Attestation] Refusing to create a pass record for a failed policy check.", file=sys.stderr)
        return 2

    payload = {
        "schema_version": "1.0",
        "attestation_kind": "synthetic_internal_policy_evaluation",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_revision": git_revision(),
        "policy": {
            "id": policy["policy_id"],
            "version": policy["version"],
            "sha256": sha256(args.policy),
        },
        "subject": {
            "name": str(args.architecture.relative_to(ROOT)) if args.architecture.is_relative_to(ROOT) else args.architecture.name,
            "sha256": sha256(args.architecture),
        },
        "result": {
            "status": result["status"],
            "checks_passed": len(result["checks"]),
            "failures": result["failure_count"],
            "control_ids": sorted(
                {mapping["id"] for check in result["checks"] for mapping in check["ccc_mappings"]}
            ),
        },
        "runner": "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local demo",
        "signature": "The CI workflow signs this payload with a Sigstore bundle.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"[Attestation] Wrote passing policy record to {args.output}")
    print("[Attestation] The JSON is signed only when the Sigstore CI step creates its bundle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
