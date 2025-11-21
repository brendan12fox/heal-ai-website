# © 2025 HEAL-AI. All Rights Reserved.
# Perioperative Note Translator Application

import streamlit as st

# --- PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(
    page_title="Perioperative Note Translator | HEAL-AI",
    page_icon="📋",
    layout="centered"
)

import sys
import os

# Add parent directory to path for shared utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.openai_utils import generate_instructions
from utils.pdf_export import create_pdf_from_text

# --- CUSTOM STYLES ---
st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 800px;
    }
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
    }
    .app-header h1 {
        color: white;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .app-header p {
        color: rgba(255, 255, 255, 0.95);
        margin: 0;
    }
    .card {
        background-color: #f7f9fc;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        border: 1px solid #d0d4da;
        margin-bottom: 2rem;
    }
    .back-link {
        margin-bottom: 1.5rem;
    }
    .back-link a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
    }
    .back-link a:hover {
        text-decoration: underline;
    }
    .stButton > button {
        background-color: #667eea;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #5568d3;
    }
    .stRadio > div {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #d3d3d3;
        margin-bottom: 1.5rem;
    }
    /* Form element spacing */
    .stSelectbox {
        margin-bottom: 1.5rem;
    }
    div[data-baseweb="select"] {
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- BACK TO HOME ---
st.markdown('<div class="back-link"><a href="/">← Back to HEAL-AI Home</a></div>', unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="app-header">
    <h1>📋 Perioperative Note Translator</h1>
    <p>Multilingual, Literacy-Optimized Consent & Post-Op Instructions</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT PANEL ---
st.markdown("### Patient Instruction Options")

col1, col2 = st.columns(2)
with col1:
    instruction_type = st.radio("Instruction Type", ["Post-Op", "Consent"], horizontal=True)
with col2:
    language = st.selectbox("Language", ["English", "Spanish", "Arabic", "Bengali"])

reading_level = st.selectbox("Reading Level", ["Standard", "High School", "5th Grade"])

procedure = st.selectbox("Procedure", [
    "Appendectomy", "Cholecystectomy", "Hernia Repair", "Cesarean Section",
    "Colonoscopy", "Endoscopy", "Tonsillectomy", "Mastectomy", "Hysterectomy",
    "Circumcision", "Cataract Surgery", "Joint Replacement (Hip or Knee)",
    "Carpal Tunnel Release", "Abscess Drainage", "Laparoscopic Gallbladder Removal"
])

# --- GENERATE BUTTON ---
if st.button("Generate Instructions"):
    with st.spinner("Curating a medically equitable, patient-friendly document..."):
        base_behavior = (
            "You are a medical communication expert. Your task is to translate clinical documents "
            "into plain language for patients with limited health literacy. Your tone should be clear, empathetic, and respectful. "
            "Avoid medical jargon unless defined simply. Use short sentences, bullet points, and bold section headers."
        )

        if instruction_type == "Post-Op":
            prompt = (
                f"{base_behavior} Rewrite the post-operative instructions for a {procedure}. "
                f"Translate the output into {language} at a {reading_level} reading level. "
                "Include the following sections: 1) Wound Care, 2) Pain Management, 3) Activity Restrictions, "
                "4) Diet, 5) When to Call the Doctor (Red Flag Symptoms), and 6) Follow-Up Instructions. "
                "Make the instructions actionable and easy to follow at home."
            )
        else:
            prompt = (
                f"{base_behavior} Write a simplified pre-operative surgical consent explanation for a {procedure}. "
                f"Translate the output into {language} at a {reading_level} reading level. "
                "Include the following sections: 1) What the procedure is, 2) Why it is needed, "
                "3) Risks and complications, 4) Benefits, 5) Alternatives (including doing nothing), "
                "6) Recovery expectations, and 7) Patient rights (right to ask questions and refuse). "
                "Use language a family member without medical training can understand."
            )

        output = generate_instructions(prompt)

    # --- DISPLAY OUTPUT ---
    st.markdown("<h3 style='margin-top: 2rem;'>Generated Instructions</h3>", unsafe_allow_html=True)
    with st.expander("View Instructions", expanded=True):
        st.markdown(output)

    # --- PDF DOWNLOAD ---
    pdf_path = create_pdf_from_text(
        output,
        title=f"{instruction_type} Instructions: {procedure}"
    )

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name=f"{instruction_type.lower()}_{procedure.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

# --- ABOUT SECTION ---
st.markdown("---")
st.markdown("""
## About This Application

The Perioperative Note Translator provides:

- **Medical Terminology Translation**: Convert complex surgical terminology into plain language
- **Patient-Friendly Summaries**: Generate clear, concise summaries of surgical procedures
- **Multilingual Support**: Make surgical notes accessible across different languages (English, Spanish, Arabic, Bengali)
- **Health Literacy Optimization**: Adjust reading levels to match patient needs
- **PDF Export**: Download instructions for offline use

This application is part of HEAL-AI's mission to improve health equity and accessibility 
through innovative AI-powered language tools.
""")

