# HEAL-AI Setup Guide

This guide will help you set up the HEAL-AI website locally and prepare it for deployment.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Cloud account (for Google Sheets integration)
- OpenAI API key

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Streamlit Secrets

Create a `.streamlit/secrets.toml` file in the project root with the following structure:

```toml
# OpenAI API Key (required for both applications)
openai_api_key = "your-openai-api-key-here"

# Google Sheets Integration (required for Resource Finder logging)
# This should be a JSON object containing your Google Service Account credentials
[google_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

**Note**: For security, never commit your `secrets.toml` file to version control. Add it to `.gitignore`.

### 3. Google Sheets Setup (Resource Finder)

The Resource Finder uses Google Sheets to log searches and feedback. To set this up:

1. **Create a Google Service Account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Sheets API
   - Create a Service Account
   - Download the JSON key file

2. **Create Google Sheets**:
   - Create two Google Sheets:
     - `Search_Log` - for logging search queries
     - `Feedback_Log` - for logging user feedback
   - Share both sheets with the service account email (found in the JSON key file)
   - Give the service account "Editor" permissions

3. **Add Service Account to Secrets**:
   - Copy the entire JSON content from the downloaded key file
   - Paste it into the `[google_service_account]` section of `secrets.toml`

### 4. OpenAI API Key Setup

1. **Get an API Key**:
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Create an account or sign in
   - Navigate to API Keys section
   - Create a new API key

2. **Add to Secrets**:
   - Add the API key to `secrets.toml` as shown above

### 5. Run the Application

```bash
python3 -m streamlit run app.py
```

Or if you have `streamlit` installed:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Application Structure

```
heal-ai-website/
├── app.py                          # Main landing page
├── pages/
│   ├── 1_Resource_Finder.py        # Community Resource Finder
│   └── 2_Perioperative_Translator.py  # Perioperative Note Translator
├── utils/
│   ├── __init__.py
│   ├── openai_utils.py             # OpenAI API utilities
│   └── pdf_export.py               # PDF generation utilities
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml                # API keys and credentials (not in git)
└── README.md
```

## Features

### 1. Community Resource Finder
- Searches for hyperlocal community resources by ZIP code
- Categories: Food assistance, Housing, Medical care, Mental health, Legal aid, etc.
- Logs searches and feedback to Google Sheets
- Uses backend API proxy for GPT requests

### 2. Perioperative Note Translator
- Generates patient-friendly surgical instructions
- Supports multiple languages: English, Spanish, Arabic, Bengali
- Adjustable reading levels: Standard, High School, 5th Grade
- Supports both Post-Op instructions and Consent forms
- PDF export functionality

## Troubleshooting

### Google Sheets Integration Not Working
- Verify the service account JSON is correctly formatted in `secrets.toml`
- Ensure the Google Sheets are shared with the service account email
- Check that the Google Sheets API is enabled in your Google Cloud project

### OpenAI API Errors
- Verify your API key is correct in `secrets.toml`
- Check your OpenAI account has sufficient credits
- Ensure you have access to the GPT-4o model

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.8 or higher: `python --version`

## Deployment

### Streamlit Cloud
1. Push code to GitHub (excluding `secrets.toml`)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Add secrets in the Streamlit Cloud dashboard (Settings → Secrets)
5. Deploy!

### Other Platforms
The application can be deployed to any platform supporting Streamlit:
- Heroku
- AWS (Elastic Beanstalk, EC2)
- Google Cloud Platform
- Azure
- DigitalOcean

For each platform, ensure:
- All dependencies are in `requirements.txt`
- Secrets are configured via the platform's environment variables or secrets management
- The entry point is `streamlit run app.py`

## Cost Considerations

With a $2000 budget, you can:
- **Domain**: ~$10-15/year (e.g., heal-ai.org)
- **Hosting**: 
  - Streamlit Cloud: Free tier available, paid plans start at $20/month
  - Other platforms: Varies, but can be $5-50/month depending on traffic
- **OpenAI API**: Pay-per-use, typically $0.01-0.10 per request depending on model
- **Google Sheets**: Free for basic usage

Estimated monthly costs for moderate usage:
- Hosting: $20-50/month
- OpenAI API: $50-200/month (depending on usage)
- **Total**: ~$70-250/month

## Support

For questions or issues, contact: brendan12fox@gmail.com

