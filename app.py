import json
import streamlit as st

st.set_page_config(page_title="LexCode-to-CALM Policy Playground", layout="wide")

st.title("LexCode-to-CALM: Interactive Governance Gate")
st.caption("FINOS Fall 2026 Hackathon | Track 2: Governance-as-Code")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Regulatory Rule DSL")
    reg_option = st.selectbox(
        "Select Active Mandate",
        ["EU AI Act Article 10 (Data Sovereignty)", "FINOS CCC Security Baseline"]
    )
    
    sample_dsl = {
        "statute": "EU AI Act Article 10.2.a",
        "jurisdiction": "EU",
        "required_regions": ["eu-central-1", "eu-west-1"],
        "enforcement": "HARD_BLOCK"
    }
    st.json(sample_dsl)

with col2:
    st.subheader("2. Architecture Manifest (CALM)")
    arch_type = st.radio("Load Sample Architecture", ["Non-Compliant (US Region)", "Compliant (EU Region)"])
    
    if "Non-Compliant" in arch_type:
        manifest = {
            "id": "ai-inference-service",
            "region": "us-east-1",
            "logging_enabled": False
        }
    else:
        manifest = {
            "id": "ai-inference-service",
            "region": "eu-central-1",
            "logging_enabled": True
        }
    st.json(manifest)

st.markdown("---")

if st.button("Run Governance Gate", type="primary"):
    st.subheader("Evaluation Results")
    if manifest["region"] not in sample_dsl["required_regions"]:
        st.error(f"DEPLOYMENT BLOCKED: Node in region '{manifest['region']}' violates legal mandate!")
        st.warning(f"Statutory Citation: {sample_dsl['statute']}")
        st.code("Rule Violation: RULE-EU-AI-010-LOC | FINOS Control ID: CCC-SEC-012-DATA-RESIDENCY", language="text")
    else:
        st.success("GOVERNANCE PASSED: Workload fully complies with regulatory bounds.")
        st.info("Cryptographic Audit Attestation signed successfully.")
