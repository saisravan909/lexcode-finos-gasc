![Governance pipeline](https://github.com/saisravan909/lexcode-finos-gasc/actions/workflows/governance-pipeline.yml/badge.svg)

# LexCode to CALM

A small, reproducible policy compiler for Track 2 of the FINOS Fall 2026 Hackathon. LexCode turns a versioned policy file into FINOS CALM control requirements, checks a sample architecture with the official CALM CLI, and produces evidence that can be signed with Sigstore in CI.

## Scope and accuracy

The sample region allowlist is an internal organization policy. Regulation (EU) 2024/1689 Article 10 concerns data and data governance for high risk AI systems. This project does not claim that Article 10 creates a general EU data residency rule. A failed policy check is not a legal finding.

The sample also requires human review for every case disposition and prohibits automatic alert closure. Those controls align with the FINOS AI Governance Framework anti financial crime investigation use case, which is marked draft in that project. The investigator remains responsible for each disposition.

## Architecture

```text
Versioned policy JSON
        |
        v
LexCode compiler -----> CALM control requirements
        |                         |
        v                         v
Deterministic gate       Official FINOS CALM CLI
        |
        +----> local policy playground
        +----> pull request comment preview
        +----> content addressed evidence JSON
                                |
                                v
                    Sigstore bundle in CI
```

## What works today

* Policy rules compile into the CALM `controls` structure, with one generated control requirement for each rule.
* The generated CALM architecture is checked by `@finos/calm-cli`.
* The deterministic evaluator checks every modeled service, data store, and workflow rule. Missing data fails closed.
* The browser playground edits architecture JSON and shows each result. It binds to loopback and makes no external model call.
* The comment bot writes a Markdown preview locally. It does not call GitHub.
* A passing evaluation produces a content addressed JSON record. GitHub Actions signs that record with a keyless Sigstore bundle and verifies the bundle identity.

The repository demonstrates the policy compiler and CALM path. Fluxnova runtime orchestration is demonstrated separately in the FINOS team submission, [Omicron AML Alert Triage](https://github.com/finos-hack/fall-hackathon-2026-omicron).

## Run the end to end demo

Requirements: Python 3.9 or newer, Node.js 22.13 or newer, and npm.

```sh
bash scripts/demo.sh
```

The script compiles the policy, validates the output with the official FINOS CALM CLI, confirms that one sample passes and one sample fails, writes a local comment preview and attestation record, then runs the policy checks.

## Open the playground

```sh
python3 app.py
```

Open `http://127.0.0.1:8501`. The server listens only on the local computer. It reads the checked in sample files and does not send the architecture to a hosted service.

## Verify a CI attestation

The CI workflow writes `artifacts/audit_attestation.json` and `artifacts/audit_attestation.sigstore.json` as a downloadable workflow artifact. Verify the detached signature with Cosign and the expected repository workflow identity:

```sh
cosign verify-blob artifacts/audit_attestation.json \
  --bundle artifacts/audit_attestation.sigstore.json \
  --certificate-identity-regexp '^https://github\.com/saisravan909/lexcode-finos-gasc/.github/workflows/governance-pipeline.yml@refs/(heads|pull)/.*$' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

A local demo record is unsigned. The signature exists only when the CI job creates the Sigstore bundle. The record proves the bytes that were checked and the policy result; it is not a regulatory certification or a deployment authorization.

## FINOS mappings

| Source | Use in this repository | Limit |
| --- | --- | --- |
| [CALM schema](https://github.com/finos/calm-schema) and [CALM CLI](https://github.com/finos/architecture-as-code/tree/main/cli) | Generated controls are part of a valid CALM architecture, checked by the official CLI | Schema validity does not prove a control is legally sufficient |
| [Common Cloud Controls](https://github.com/finos/common-cloud-controls) `CCC.Core.CN06` | Related trust perimeter control for the sample region boundary | It is not a residency mandate |
| Common Cloud Controls `CCC.Core.CN04` | Related access and change logging control | The sample checks a boolean field, not the integrity of a production log system |
| [AI Governance Framework UC 4](https://github.com/finos/ai-governance-framework/blob/main/docs/_usecases/uc-4_anti-financial-crime-investigation.md) | Human disposition and no automatic alert closure | The use case is draft and the project is a small demonstration |

## Sources and legal boundary

* [Regulation (EU) 2024/1689, official EUR Lex text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
* [31 U.S.C. 5324, official United States Code](https://uscode.house.gov/us/usc/119-124/t31/s5324/)

A transaction pattern or threshold in a monitoring policy does not establish intent to evade reporting. The demo does not decide whether activity is suspicious, determine whether a report is required, or file a report.

## Hackathon rubric map

* **Ecosystem integration:** CALM CLI and schema, CCC catalog mappings, and AIGF use case references. The companion Omicron submission adds Fluxnova BPMN orchestration.
* **Technical execution:** one command checks a valid and invalid architecture, emits a generated CALM architecture, and creates a verifiable CI evidence bundle.
* **Business value:** a versioned policy change is compiled and evaluated consistently, while a human remains responsible for disposition.
* **Innovation and build velocity:** this repository was built with Codex and has a local interactive policy playground.

## Project files

* `lexcode/dsl/sample_internal_policy.json` is the synthetic internal policy and its legal context.
* `lexcode/compiler/lexcode_to_calm.py` compiles policy rules into CALM controls.
* `lexcode/policy.py` evaluates the deterministic rules.
* `calm/architecture/lexcode_policy_architecture.json` is the generated sample.
* `web/` and `app.py` provide the local playground.
* `scripts/generate_attestation.py` creates the content addressed record.
* `scripts/pr_bot_sim.py` writes a local comment preview.
* `docs/whitepaper.md` explains design and limits.

## Contributing

Run `bash scripts/demo.sh` before proposing changes. The CI workflow runs the same demonstration, CALM validation, and Sigstore signing.
