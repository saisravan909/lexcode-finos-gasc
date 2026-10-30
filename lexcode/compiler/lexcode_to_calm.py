#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def compile_regulation_to_calm(lexcode_path: str, output_path: str):
    with open(lexcode_path, 'r') as f:
        reg_data = json.load(f)
    
    calm_controls = {
        "$schema": "https://finos.org/calm/v1/controls.json",
        "regulation_reference": reg_data["regulation_id"],
        "article": reg_data["article"],
        "generated_rules": []
    }

    for rule in reg_data["rules"]:
        calm_rule = {
            "control_id": rule["rule_id"],
            "finos_ccc_id": rule["finos_ccc_mapping"],
            "description": rule["description"],
            "evaluator": {
                "field": rule["property"],
                "operator": rule["operator"],
                "expected": rule["value"]
            },
            "enforcement": reg_data["enforcement_level"]
        }
        calm_controls["generated_rules"].append(calm_rule)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(calm_controls, f, indent=2)
    
    print(f"[LexCode Compiler] Successfully compiled {reg_data['regulation_id']} into CALM controls: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python lexcode_to_calm.py <lexcode_file> <output_calm_file>")
        sys.exit(1)
    compile_regulation_to_calm(sys.argv[1], sys.argv[2])
