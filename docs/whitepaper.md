# LexCode to CALM: policy compilation for architecture review

## Executive summary

Financial institutions often maintain security, data handling, and model oversight rules in documents that are hard to connect to architecture changes. LexCode is a small demonstration of a controlled path from a versioned policy source to CALM control requirements and a deterministic review result.

The sample policy deliberately separates organizational requirements from law. It includes a synthetic processing region allowlist, access logging, mandatory human review, and a prohibition on automatic alert closure. Regulation (EU) 2024/1689 Article 10 is recorded as context for data governance. The project does not claim that the article mandates a general EU data residency boundary.

## Design

1. The policy JSON records identifiers, version, scope, evaluation fields, source type, and related control references.
2. The Python compiler emits CALM controls with one control requirement per policy rule.
3. The FINOS CALM CLI validates the generated architecture against the released CALM schema.
4. The local policy evaluator checks each service, data store, and workflow fact. Absent values fail closed.
5. A passing evaluation produces a JSON record containing the policy and architecture digests. CI signs the file using keyless Sigstore and publishes the signature bundle as a workflow artifact.
6. A separate preview script renders failures as a possible pull request comment. It does not post to GitHub.

## Control relationships

`CCC.Core.CN06` is titled “Restrict Deployments to Trust Perimeter.” It is a related control for the sample region boundary, not evidence of a legal residency mandate. `CCC.Core.CN04` is titled “Log All Access and Changes.” The local boolean check is only a partial demonstration of that objective.

The FINOS AI Governance Framework anti financial crime investigation use case is marked draft. It says an AI assistant may summarize and recommend, while the investigator remains accountable for every disposition and the MLRO or BSA officer remains accountable for each filing. This repository translates that workflow boundary into a sample policy check. It does not integrate a model or file a report.

## Threats and safeguards

| Threat | Safeguard in this demonstration | Remaining limit |
| --- | --- | --- |
| Policy wording is mistaken for law | The policy source marks its type and legal relationship explicitly | A real institution still needs legal and compliance review |
| Incomplete architecture data | Missing values fail the rule check | The evaluator only sees fields represented in its input |
| Automated case closure | A rule requires human disposition and forbids AI closure | The web demo is not an identity or access management system |
| Evidence substituted after evaluation | The attestation records SHA 256 digests and CI signs the exact JSON bytes | A signature proves origin and integrity, not correctness of policy |
| Unintended disclosure | The playground listens on loopback and sends no data to a model | Operators must apply equivalent controls in production |
| Misleading control mapping | CCC mappings are labeled related and partial where appropriate | Catalog coverage needs a control owner and evidence in production |

## Legal and policy scope

The official EUR Lex text of Regulation (EU) 2024/1689 describes data and data governance requirements in Article 10 for high risk AI systems. It does not create the generic EU only region rule used by this sample. The synthetic region rule is included as an internal policy example.

The official United States Code text for 31 U.S.C. 5324 describes structuring transactions for the purpose of evading specified reporting or recordkeeping requirements. A repeated deposit pattern by itself does not prove that purpose. The companion Omicron AML demonstration therefore produces an investigator queue priority only and never declares a statutory violation.

## Reproduction

Run `bash scripts/demo.sh` to compile the CALM architecture, validate it with the official FINOS CLI, evaluate both samples, create a local preview, generate the unsigned local record, and run the checks. GitHub Actions signs the record using the workflow identity and retains both files as a downloadable artifact.

## References

* [FINOS CALM schema](https://github.com/finos/calm-schema)
* [FINOS CALM CLI](https://github.com/finos/architecture-as-code/tree/main/cli)
* [FINOS Common Cloud Controls](https://github.com/finos/common-cloud-controls)
* [FINOS AI Governance Framework use case 4](https://github.com/finos/ai-governance-framework/blob/main/docs/_usecases/uc-4_anti-financial-crime-investigation.md)
* [Regulation (EU) 2024/1689, EUR Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
* [31 U.S.C. 5324, United States Code](https://uscode.house.gov/us/usc/119-124/t31/s5324/)
* [Sigstore blob signing](https://docs.sigstore.dev/cosign/signing/signing_with_blobs/)
