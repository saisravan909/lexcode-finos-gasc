#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p artifacts calm/architecture

printf '%s\n' 'LexCode policy to CALM demonstration'
printf '%s\n' '1. Compile the internal policy into a CALM architecture'
python3 lexcode/compiler/lexcode_to_calm.py \
  lexcode/dsl/sample_internal_policy.json \
  tests/valid_arch.calm.json \
  calm/architecture/lexcode_policy_architecture.json

printf '\n%s\n' '2. Validate the generated architecture with the FINOS CALM CLI'
npx --yes @finos/calm-cli@1.72.0 validate \
  --architecture calm/architecture/lexcode_policy_architecture.json \
  --format pretty
npx --yes @finos/calm-cli@1.72.0 validate \
  --architecture tests/invalid_arch.calm.json \
  --format pretty

printf '\n%s\n' '3. Confirm the compliant sample passes'
python3 scripts/run_policy_gate.py \
  --architecture tests/valid_arch.calm.json \
  > artifacts/valid_policy_result.json
python3 -c 'import json; r=json.load(open("artifacts/valid_policy_result.json")); print("[PASS]", r["status"], "checks:", len(r["checks"]))'

printf '\n%s\n' '4. Confirm the unsafe sample fails closed'
if python3 scripts/run_policy_gate.py \
  --architecture tests/invalid_arch.calm.json \
  > artifacts/invalid_policy_result.json; then
  printf '%s\n' '[ERROR] The invalid sample unexpectedly passed.'
  exit 1
else
  result_code=$?
  if [ "$result_code" -ne 2 ]; then
    printf 'Policy runner exited with unexpected code %s.\n' "$result_code"
    exit "$result_code"
  fi
  python3 -c 'import json; r=json.load(open("artifacts/invalid_policy_result.json")); print("[BLOCK]", r["failure_count"], "internal policy findings; no legal conclusion")'
fi

printf '\n%s\n' '5. Write the local pull request comment preview'
python3 scripts/pr_bot_sim.py

printf '\n%s\n' '6. Create a content addressed record for the passing sample'
python3 scripts/generate_attestation.py \
  --architecture tests/valid_arch.calm.json \
  --output artifacts/audit_attestation.json

printf '\n%s\n' '7. Run the policy and compiler checks'
python3 -m unittest discover -s tests -p 'test_*.py' -v
printf '\n%s\n' 'Demo complete. CI signs the attestation with Sigstore.'
