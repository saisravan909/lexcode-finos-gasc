"""Small deterministic policy evaluator used by the LexCode demonstration."""

from __future__ import annotations

from typing import Any


MISSING = object()


def _matches(actual: Any, operator: str, expected: Any) -> bool:
    if operator == "equals":
        return actual is not MISSING and actual == expected
    if operator == "in":
        return actual is not MISSING and actual in expected
    if operator == "not_equals":
        return actual is not MISSING and actual != expected
    raise ValueError(f"Unsupported policy operator: {operator}")


def _check(rule: dict[str, Any], actual: Any, subject: str) -> dict[str, Any]:
    passed = _matches(actual, rule["operator"], rule["expected"])
    return {
        "rule_id": rule["id"],
        "title": rule["title"],
        "subject": subject,
        "status": "PASS" if passed else "FAIL",
        "operator": rule["operator"],
        "expected": rule["expected"],
        "observed": "[missing]" if actual is MISSING else actual,
        "ccc_mappings": rule.get("ccc_mappings", []),
        "aigf_reference": rule.get("aigf_reference"),
    }


def evaluate_policy(policy: dict[str, Any], architecture: dict[str, Any]) -> dict[str, Any]:
    """Evaluate declared rules without making a legal conclusion."""
    checks: list[dict[str, Any]] = []
    nodes = architecture.get("nodes", [])

    for rule in policy.get("rules", []):
        scope = rule["scope"]
        if scope == "nodes":
            if not nodes:
                checks.append(_check(rule, MISSING, "nodes"))
            for node in nodes:
                node_id = node.get("unique-id", "unnamed node")
                checks.append(_check(rule, node.get(rule["field"], MISSING), node_id))
        elif scope == "workflow":
            workflow = architecture.get("workflow", {})
            checks.append(_check(rule, workflow.get(rule["field"], MISSING), "workflow"))
        else:
            raise ValueError(f"Unsupported policy scope: {scope}")

    failures = [item for item in checks if item["status"] == "FAIL"]
    return {
        "policy_id": policy["policy_id"],
        "policy_version": policy["version"],
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failure_count": len(failures),
        "legal_conclusion": None,
        "notice": "A failed internal policy check is not a finding of legal noncompliance.",
    }
