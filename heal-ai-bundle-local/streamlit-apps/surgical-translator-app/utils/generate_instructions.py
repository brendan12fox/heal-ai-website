from openai import OpenAI
import streamlit as st

# Create OpenAI client using Streamlit secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

def generate_instructions(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()