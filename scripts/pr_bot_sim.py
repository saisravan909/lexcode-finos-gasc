import json

def generate_pr_comment():
    comment = """### FINOS Governance-as-Code Guardrail Alert
> **Status:** FAILED | Deployment Blocked

#### Violation Summary
* **Node ID:** `ai-inference-service`
* **Violating Property:** `region: us-east-1`
* **Mandated Region:** `eu-central-1` or `eu-west-1`

#### Legal & Regulatory Mapping
* **Statute:** EU AI Act Article 10.2.a (High-Risk AI Data Governance)
* **FINOS Control Mapping:** `CCC-SEC-012-DATA-RESIDENCY`

*Action Required: Update the region parameter in your CALM manifest to an approved EU region to unblock CI/CD deployment.*
"""
    with open("pr_comment_preview.md", "w") as f:
        f.write(comment)
    print("[GITOPS BOT] PR comment simulation written to: pr_comment_preview.md")

if __name__ == "__main__":
    generate_pr_comment()
