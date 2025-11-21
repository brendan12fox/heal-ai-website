import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from utils.export_weasy_pdf import export_instruction_to_pdf
from utils.generate_instructions import generate_instructions

# --- PAGE CONFIG ---
st.set_page_config(page_title="ACS Surgical Translations", layout="centered")

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
    body {
        background-color: #f0f2f5;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 800px;
        margin: auto;
        font-family: 'Segoe UI', sans-serif;
        color: #1e1e1e;
    }

    h1, h3 {
        color: #001f3f;
        font-weight: 600;
    }

    .app-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .card {
        background-color: #f7f9fc;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        border: 1px solid #d0d4da;
        margin-bottom: 2rem;
    }

    .stButton > button {
        background-color: #003366;
        color: white;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        border: none;
    }

    .stButton > button:hover {
        background-color: #004080;
    }

    .stRadio > div {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #d3d3d3;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="app-header">
        <h1>ACS Surgical Translations</h1>
        <p style="color: gray; font-size: 16px;">
            Multilingual, Literacy-Optimized Consent & Post-Op Instructions
        </p>
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

# --- GENERATE INSTRUCTIONS ---
if st.button("Generate Instructions"):
    with st.spinner("Curating a medically equitable, patient-friendly document..."):
        base_prompt = (
            "You are a medical communication expert. Your task is to translate clinical documents "
            "into plain language for patients with limited health literacy. Your tone should be clear, empathetic, and respectful. "
            "Avoid medical jargon unless defined simply. Use short sentences, bullet points, and bold section headers."
        )

        if instruction_type == "Post-Op":
            prompt = (
                f"{base_prompt} Rewrite the post-operative instructions for a {procedure}. "
                f"Translate the output into {language} at a {reading_level} reading level. "
                "Include the following sections: 1) Wound Care, 2) Pain Management, 3) Activity Restrictions, "
                "4) Diet, 5) When to Call the Doctor (Red Flag Symptoms), and 6) Follow-Up Instructions. "
                "Make the instructions actionable and easy to follow at home."
            )
        else:
            prompt = (
                f"{base_prompt} Write a simplified pre-operative surgical consent explanation for a {procedure}. "
                f"Translate the output into {language} at a {reading_level} reading level. "
                "Include the following sections: 1) What the procedure is, 2) Why it is needed, "
                "3) Risks and complications, 4) Benefits, 5) Alternatives (including doing nothing), "
                "6) Recovery expectations, and 7) Patient rights (right to ask questions and refuse). "
                "Use language a family member without medical training can understand."
            )

        output = generate_instructions(prompt)

    st.markdown("### Generated Instructions")
    with st.expander("View Instructions"):
        st.write(output)

    # --- PDF DOWNLOAD ---
    pdf_path = export_instruction_to_pdf(output, title=f"{instruction_type} Instructions: {procedure}")
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name=f"{instruction_type.lower()}_{procedure.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

# --- FOOTER ---
st.markdown("""
    <hr style="margin-top: 3rem;">
    <div style="text-align: center; color: gray; font-size: 12px;">
        ACS Surgical Translations &nbsp;|&nbsp; Built by medical students for equitable care
    </div>
""", unsafe_allow_html=True)