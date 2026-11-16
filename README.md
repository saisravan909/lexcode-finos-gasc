![FINOS Governance Pipeline](https://github.com/saisravan909/lexcode-finos-gasc/actions/workflows/governance-pipeline.yml/badge.svg)

# LexCode-to-CALM: Automated Legal-to-Architecture Governance-as-Code

Automated legal-to-architecture governance-as-code pipeline extending the FINOS Steel Thread demo.

## Overview
Submitted for **Track 2: Extend & Utilize FINOS Governance-as-Code** at the FINOS Fall 2026 Hackathon.

Financial institutions often spend months manually translating regulatory mandates into engineering policies and cloud configurations. **LexCode-to-CALM** eliminates that lag by extending the FINOS Steel Thread demonstration. It automatically translates machine-readable regulations (such as the EU AI Act) into **FINOS CALM** controls, evaluates them using **Fluxnova**, and enforces compliance via **Common Cloud Controls (CCC)** and the **AI Governance Framework (AIGF)**.

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
```

## Key Features
- **Regulatory Parser:** Compiles machine-readable legal text into structured validation rules.
- **CALM Schema Integration:** Automatically updates architectural compliance constraints.
- **Automated Gating:** Halts non-compliant infrastructure deployments and cites exact legal articles.
- **Interactive Policy Playground:** Provides a built-in Streamlit web interface to test regulations against architecture manifests in real time.
- **Verifiable Audit Attestations:** Generates cryptographic SHA-256 compliance receipts mapping directly to FINOS control frameworks.

## How to Run the Demo

### 1. Interactive Policy Playground (Web UI)
Test and evaluate regulatory DSLs against architecture manifests in real time using the built-in Streamlit interface:
1. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the local web application:
   ```bash
   streamlit run app.py
   ```

### 2. End-to-End Demonstration Script
To run the full automated pipeline (compiling regulations, testing policy gates, simulating PR feedback, and generating cryptographic attestation receipts):
1. Clone the repository and navigate into the workspace:
   ```bash
   git clone https://github.com/saisravan909/lexcode-finos-gasc.git
   cd lexcode-finos-gasc
   ```
2. Execute the demonstration script:
   ```bash
   bash scripts/demo.sh
   ```

## Project Documentation & Artifacts
- **Executive Architecture Whitepaper:** [`docs/whitepaper.md`](docs/whitepaper.md) — Architectural patterns, compliance threat models, and enterprise rationale.
- **Cryptographic Attestation Generator:** [`scripts/generate_attestation.py`](scripts/generate_attestation.py) — Generates verifiable JSON compliance proofs with SHA-256 digests.
- **GitOps PR Bot Simulation:** [`scripts/pr_bot_sim.py`](scripts/pr_bot_sim.py) — Formats automated pull request guardrail feedback with exact legal citations.
