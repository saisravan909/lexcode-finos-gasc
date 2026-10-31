![FINOS Governance Pipeline](https://github.com/saisravan909/lexcode-finos-gasc/actions/workflows/governance-pipeline.yml/badge.svg)

# lexcode-finos-gasc
Automated legal-to-architecture governance-as-code pipeline extending the FINOS Steel Thread demo.
# LexCode-to-CALM: Automated Legal-to-Architecture Governance-as-Code

## Overview
Submitted for **Track 2: Extend & Utilize FINOS Governance-as-Code** at the FINOS Fall 2026 Hackathon. 

This project bridges the gap between external legal regulations and internal cloud architecture by extending the FINOS Steel Thread demo. It automatically translates machine-readable regulations (such as the EU AI Act) into **FINOS CALM** controls, evaluates them using **Fluxnova**, and enforces compliance via **Common Cloud Controls (CCC)**.

## Key Features
- **Regulatory Parser:** Compiles legal text into structured validation rules.
- **CALM Schema Integration:** Automatically updates architectural compliance constraints.
- **Automated Gating:** Halts non-compliant infrastructure deployments and cites exact legal articles.

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
