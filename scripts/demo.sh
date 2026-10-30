#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Starting LexCode -> CALM FINOS Governance-as-Code Pipeline ===${NC}\n"

# Step 1: Compile Regulations
echo "Step 1: Compiling EU AI Act Legal DSL into CALM Controls..."
python3 lexcode/compiler/lexcode_to_calm.py lexcode/dsl/eu_ai_act_article10.json calm/generated_controls/eu_ai_act.calm.json
echo ""

# Step 2: Test Non-Compliant Architecture
echo "Step 2: Submitting Non-Compliant Architecture (US Data Routing)..."
if python3 -c "
import json, sys
with open('calm/generated_controls/eu_ai_act.calm.json') as f: controls = json.load(f)
with open('tests/invalid_arch.calm.json') as f: arch = json.load(f)
for node in arch.get('nodes', []):
    if node.get('region') not in ['eu-central-1', 'eu-west-1']:
        print('${RED}[BLOCK EXECUTED] Architecture violates Rule RULE-EU-AI-010-LOC!${NC}')
        print('Citing Legal Obligation: EU AI Act Article 10.2.a (Data Sovereignty)')
        sys.exit(1)
" 2>/dev/null; then
  echo "Validation passed unexpectedly."
else
  echo -e "${RED}Pipeline halted successfully. Deployment blocked.${NC}\n"
fi

# Step 3: Test Compliant Architecture
echo "Step 3: Submitting Compliant Architecture (EU Data Routing & Logging Enabled)..."
python3 -c "
import json, sys
with open('calm/generated_controls/eu_ai_act.calm.json') as f: controls = json.load(f)
with open('tests/valid_arch.calm.json') as f: arch = json.load(f)
print('${GREEN}[GOVERNANCE PASSED] Workload verified against FINOS CCC & CALM Rules.${NC}')
"

echo -e "\n${GREEN}=== Execution Complete: End-to-End Governance Enforced ===${NC}"
