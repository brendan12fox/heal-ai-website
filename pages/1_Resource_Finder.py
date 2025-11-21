# © 2025 HEAL-AI. All Rights Reserved.
# Community Resource Finder Application

import streamlit as st
import requests
import os
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Community Resource Finder | HEAL-AI", page_icon="🔍", layout="centered")

# Minimal CSS - only what's needed
st.markdown("""
<style>
    .block-container {padding: 1rem 1rem 1rem 1rem; max-width: 800px;}
    .app-header {text-align: center; margin: 0 0 1rem 0; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;}
    .app-header h1 {color: white; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 1.8rem;}
    .app-header p {color: rgba(255,255,255,0.95); margin: 0;}
    .card {background: #f7f9fc; padding: 2rem; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); border: 1px solid #d0d4da; margin: 1rem 0;}
    .stButton > button {background: #667eea; color: white; border-radius: 6px; padding: 0.5rem 1rem;}
    .back-link {margin: 0 0 0.5rem 0;}
    .back-link a {color: #667eea; text-decoration: none; font-weight: 500;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="back-link"><a href="/">← Back to HEAL-AI Home</a></div>', unsafe_allow_html=True)
st.markdown("""<div class="app-header"><h1>🔍 Community Resource Finder</h1><p>Find verified local help near you</p></div>""", unsafe_allow_html=True)

# Compact inputs - no extra spacing
with st.container():
    category = st.selectbox("What type of help are you looking for?", [
        "Food assistance", "Housing or shelter", "Medical care", 
        "Mental health support", "Legal aid", "Employment services", 
        "Addiction recovery", "Transportation assistance", "Elder care", "Other"
    ])
    zip_code = st.text_input("Enter ZIP Code", placeholder="e.g. 14201")

def build_prompt(category, zip_code):
    return f"""You are acting as a clinical social work assistant helping a healthcare provider identify free or low-cost hyperlocal community resources for vulnerable adults.

Return a list of 3 to 5 unique, verifiable services that provide assistance in the category of **{category}**, specifically located in **ZIP Code {zip_code}** (and surrounding neighborhoods if necessary).

Requirements:
- Only include local or regional nonprofits, public agencies, health systems, or government-run services.
- Each entry must include: Service Name, One-sentence description, Contact Info (Address with ZIP, phone if available, website if available)

Strict Guidelines:
- Avoid listing national hotlines or broad advice like "try local churches."
- Do not list duplicate organizations.
- If no services are found, return: "No appropriate services found."

Present results as a clean numbered list or table, readable for both patients and care staff."""

@st.cache_data(ttl=3600, show_spinner=False)
def get_resources_from_gpt(prompt):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = requests.post("https://ai-resource-guide.fly.dev/chat", json={"messages": messages}, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"Failed to get response: {e}")

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    def record_search(zip_code, category):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("Search_Log").sheet1
        sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), zip_code, category])
    LOGGING_ENABLED = True
except:
    LOGGING_ENABLED = False

if 'results' not in st.session_state:
    st.session_state.results = None
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False

if st.button("Find Resources"):
    if not zip_code.strip():
        st.error("Please enter a ZIP code.")
    else:
        with st.spinner("Searching..."):
            try:
                if LOGGING_ENABLED:
                    record_search(zip_code, category)
                st.session_state.results = get_resources_from_gpt(build_prompt(category, zip_code))
                st.session_state.show_feedback = True
            except Exception as e:
                st.error(str(e))

if st.session_state.results:
    st.markdown(f"<div class='card'>{st.session_state.results}</div>", unsafe_allow_html=True)
    if st.session_state.show_feedback:
        resource_number = st.selectbox("Which resource (1-5) did you use?", ["1", "2", "3", "4", "5"], key="resource_select")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Helpful", key="helpful_btn"):
                st.success("Thanks!")
                st.session_state.show_feedback = False
        with col2:
            if st.button("👎 Not Helpful", key="not_helpful_btn"):
                st.info("Thanks!")
                st.session_state.show_feedback = False
