# Quick Start Guide

## Fix the API Key Error

You're seeing this error because the API key in `secrets.toml` is still set to the placeholder value.

### Steps to Fix:

1. **Get your OpenAI API key:**
   - Go to https://platform.openai.com/api-keys
   - Sign in or create an account
   - Click "Create new secret key"
   - Copy the key (it starts with `sk-`)

2. **Update the secrets file:**
   ```bash
   # Open the secrets file
   nano .streamlit/secrets.toml
   # or use your preferred editor
   ```

3. **Replace the placeholder:**
   ```toml
   # Change this:
   openai_api_key = "your-openai-api-key-here"
   
   # To this (with your actual key):
   openai_api_key = "sk-your-actual-key-here"
   ```

4. **Save and restart:**
   - Save the file
   - Stop the Streamlit app (Ctrl+C)
   - Restart: `python3 -m streamlit run app.py`

### For Google Sheets (Optional - Resource Finder logging):

If you want the Resource Finder to log searches to Google Sheets:

1. Go to https://console.cloud.google.com/
2. Create a project
3. Enable Google Sheets API
4. Create a Service Account
5. Download the JSON key file
6. Copy the entire JSON content into the `[google_service_account]` section of `secrets.toml`

The app will work without Google Sheets - it just won't log searches.

## Test the Apps

1. **Resource Finder**: Should work immediately (uses backend API)
2. **Perioperative Translator**: Needs OpenAI API key configured

Both apps should now have proper padding and spacing!

