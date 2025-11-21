import os
import streamlit as st
from openai import OpenAI

# Try to get API key from Streamlit secrets first, then environment variable
@st.cache_resource
def get_openai_client():
    """Cached OpenAI client to improve performance"""
    try:
        api_key = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    except:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set in Streamlit secrets or environment variables")
    
    return OpenAI(api_key=api_key)

# Get client instance
try:
    client = get_openai_client()
except:
    client = None

def generate_instructions(prompt, model="gpt-4o"):
    """
    Generate instructions using OpenAI API.
    
    Args:
        prompt: The prompt to send to the model
        model: The model to use (default: gpt-4o)
    
    Returns:
        Generated text content
    """
    if client is None:
        # Fallback if client not initialized
        try:
            api_key = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
            if not api_key or api_key == "your-openai-api-key-here":
                return "⚠️ **Configuration Error**: OpenAI API key not configured.\n\nPlease:\n1. Open `.streamlit/secrets.toml`\n2. Replace `your-openai-api-key-here` with your actual OpenAI API key\n3. Get your API key from: https://platform.openai.com/api-keys\n4. Restart the Streamlit app"
            temp_client = OpenAI(api_key=api_key)
        except Exception as e:
            return f"⚠️ **Configuration Error**: OpenAI API key not configured.\n\nPlease check your `.streamlit/secrets.toml` file and ensure `openai_api_key` is set correctly."
    else:
        temp_client = client
    
    # Check if API key is still placeholder
    try:
        current_key = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY", "")
        if "your-openai-api-key" in current_key.lower():
            return "⚠️ **Configuration Error**: OpenAI API key is still set to placeholder.\n\nPlease:\n1. Open `.streamlit/secrets.toml`\n2. Replace `your-openai-api-key-here` with your actual OpenAI API key\n3. Get your API key from: https://platform.openai.com/api-keys\n4. Restart the Streamlit app"
    except:
        pass
    
    try:
        response = temp_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a medical writer helping patients understand surgical instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_str = str(e)
        if "invalid_api_key" in error_str or "401" in error_str:
            return "⚠️ **API Key Error**: Invalid OpenAI API key.\n\nPlease:\n1. Check your API key in `.streamlit/secrets.toml`\n2. Ensure it's a valid key from: https://platform.openai.com/api-keys\n3. Make sure you haven't exceeded your API usage limits\n4. Restart the Streamlit app"
        return f"⚠️ **Error**: {error_str}"

