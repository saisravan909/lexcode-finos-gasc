import json
import unittest
from pathlib import Path

from lexcode.compiler.lexcode_to_calm import compile_policy
from lexcode.policy import evaluate_policy

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class PolicyEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load(ROOT / "lexcode/dsl/sample_internal_policy.json")

    def test_valid_architecture_passes_all_rules(self):
        result = evaluate_policy(self.policy, load(ROOT / "tests/valid_arch.calm.json"))
        self.assertEqual("PASS", result["status"])
        self.assertEqual(0, result["failure_count"])
        self.assertEqual(6, len(result["checks"]))

    def test_invalid_architecture_fails_closed(self):
        result = evaluate_policy(self.policy, load(ROOT / "tests/invalid_arch.calm.json"))
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(4, result["failure_count"])
        self.assertIsNone(result["legal_conclusion"])

    def test_missing_nodes_fail_closed(self):
        result = evaluate_policy(self.policy, {"workflow": {"human_decision_required": True}})
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(3, result["failure_count"])

    def test_compiler_emits_calm_control_requirements(self):
        result = compile_policy(self.policy, load(ROOT / "tests/valid_arch.calm.json"))
        requirements = result["controls"]["lexcode-policy-controls"]["requirements"]
        self.assertEqual(4, len(requirements))
        self.assertEqual("LEXCODE_REGION_BOUNDARY_001", requirements[0]["config"]["control-id"])
        self.assertEqual("https://calm.finos.org/release/1.3/meta/control-requirement.json", requirements[0]["requirement-url"])


if __name__ == "__main__":
    unittest.main()
