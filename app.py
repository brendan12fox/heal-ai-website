# © 2025 HEAL-AI. All Rights Reserved.
# Health Equity and Accessibility through Language and Artificial Intelligence

import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="HEAL-AI - Health Equity & Accessibility",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM STYLES ---
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .heal-ai-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .heal-ai-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .heal-ai-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    .app-card {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
        margin-bottom: 2rem;
        transition: transform 0.3s, box-shadow 0.3s;
        height: 100%;
    }
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .app-card h2 {
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.8rem;
    }
    .app-card p {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1.5rem;
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
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        margin-top: 4rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="heal-ai-header">
    <h1>🏥 HEAL-AI</h1>
    <p>Health Equity and Accessibility through Language and Artificial Intelligence</p>
    <p style="font-size: 1rem; margin-top: 1rem;">Empowering underserved communities through innovative AI-powered healthcare tools</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.markdown("""
## Welcome to HEAL-AI

HEAL-AI is an informal lab group dedicated to advancing health equity and accessibility through 
cutting-edge artificial intelligence and natural language processing technologies. Our mission 
is to bridge healthcare gaps and provide accessible tools for underserved populations.
""")

st.markdown("---")

# --- APPLICATION CARDS ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="app-card">
        <h2>🔍 Community Resource Finder</h2>
        <p>
            Find verified local resources for underserved communities. Search for food assistance, 
            housing, medical care, mental health support, and more in your area. Get hyperlocal, 
            verified information tailored to your ZIP code.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Launch Resource Finder →", key="resource_finder"):
        st.switch_page("pages/1_Resource_Finder.py")

with col2:
    st.markdown("""
    <div class="app-card">
        <h2>📋 Perioperative Note Translator</h2>
        <p>
            Translate and understand surgical notes with ease. This AI-powered tool helps 
            patients and healthcare providers translate complex perioperative documentation 
            into clear, accessible language.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Launch Note Translator →", key="note_translator"):
        st.switch_page("pages/2_Perioperative_Translator.py")

st.markdown("---")

# --- ABOUT SECTION ---
st.markdown("""
## About HEAL-AI

HEAL-AI (Health Equity and Accessibility through Language and Artificial Intelligence) 
is committed to:

- **Health Equity**: Ensuring all individuals have fair access to healthcare resources
- **Accessibility**: Making healthcare information understandable and actionable
- **Innovation**: Leveraging AI and NLP to solve real-world healthcare challenges
- **Community Focus**: Serving underserved populations with targeted solutions

Our applications are designed to break down barriers and empower individuals with the 
information they need to make informed healthcare decisions.
""")

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p>© 2025 HEAL-AI. All Rights Reserved.</p>
    <p>
        <a href="PRIVACY_POLICY.md" style="color: #667eea; margin: 0 1rem;">Privacy Policy</a> | 
        <a href="TERMS_OF_USE.md" style="color: #667eea; margin: 0 1rem;">Terms of Use</a>
    </p>
</div>
""", unsafe_allow_html=True)

