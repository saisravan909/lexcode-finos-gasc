![FINOS Governance Pipeline](https://github.com/saisravan909/lexcode-finos-gasc/actions/workflows/governance-pipeline.yml/badge.svg)

# lexcode-finos-gasc
Automated legal-to-architecture governance-as-code pipeline extending the FINOS Steel Thread demo.
# LexCode-to-CALM: Automated Legal-to-Architecture Governance-as-Code

## Overview
Submitted for **Track 2: Extend & Utilize FINOS Governance-as-Code** at the FINOS Fall 2026 Hackathon.

Financial institutions often spend months manually translating regulatory mandates into engineering policies and cloud configurations. **LexCode-to-CALM** eliminates that lag by extending the FINOS Steel Thread demonstration. It automatically translates machine-readable regulations (such as the EU AI Act) into **FINOS CALM** controls, evaluates them using **Fluxnova**, and enforces compliance via **Common Cloud Controls (CCC)** and the **AI Governance Framework (AIGF)**.

## Key Features
**Regulatory Parser:** Compiles machine-readable legal text into structured validation rules.
- **CALM Schema Integration:** Automatically updates architectural compliance constraints.
- **Automated Gating:** Halts non-compliant infrastructure deployments and cites exact legal articles.
- **Interactive Policy Playground:** Provides a built-in Streamlit web interface to test regulations against architecture manifests in real time.
- **Verifiable Audit Attestations:** Generates cryptographic SHA-256 compliance receipts mapping directly to FINOS control frameworks.

## How to Run the Demo
1. Clone the repository.
2. Run the demonstration script:
   ```bash
   bash scripts/demo.sh
## System Architecture

```text
[ Legal DSL Regulation ] 
           │
           ▼
[ LexCode Compiler ] 
           │
           ▼
[ FINOS CALM Rules ] 
           │
           ▼
[ Fluxnova Policy Gate ] ◄── [ Architecture Manifest ]
       ├──► [Compliant] ──────► [ FINOS CCC Attestation Signed ]
       └──► [Non-Compliant] ──► [ Deployment Blocked + Legal Citation ]
