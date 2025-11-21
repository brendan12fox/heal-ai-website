# HEAL-AI Website

**Health Equity and Accessibility through Language and Artificial Intelligence**

A centralized web platform hosting AI-powered healthcare applications designed to serve underserved populations.

## Overview

HEAL-AI is an informal lab group dedicated to advancing health equity and accessibility through cutting-edge artificial intelligence and natural language processing technologies. This website serves as a central hub for our applications.

## Applications

### 1. Community Resource Finder 🔍
Find verified local resources for underserved communities. Search for food assistance, housing, medical care, mental health support, and more in your area. Get hyperlocal, verified information tailored to your ZIP code.

### 2. Perioperative Note Translator 📋
Generate patient-friendly surgical instructions in multiple languages. This AI-powered tool helps patients and healthcare providers understand complex perioperative documentation through:
- Multilingual support (English, Spanish, Arabic, Bengali)
- Adjustable reading levels (Standard, High School, 5th Grade)
- Post-operative instructions and consent forms
- PDF export functionality

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/brendan12fox/dnv-streamlit-app.git
cd dnv-streamlit-app/heal-ai-website
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up configuration:
   - See `SETUP.md` for detailed configuration instructions
   - Create `.streamlit/secrets.toml` with your API keys:
     - OpenAI API key (required for both applications)
     - Google Service Account credentials (required for Resource Finder logging)

4. Run the application:
```bash
python3 -m streamlit run app.py
```

Or if you have `streamlit` installed:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
heal-ai-website/
├── app.py                      # Main landing page
├── pages/
│   ├── 1_Resource_Finder.py   # Community Resource Finder application
│   └── 2_Perioperative_Translator.py  # Perioperative Note Translator
├── utils/                      # Shared utilities
│   ├── __init__.py
│   ├── openai_utils.py         # OpenAI API utilities
│   └── pdf_export.py          # PDF generation utilities
├── assets/                     # Static assets
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── SETUP.md                    # Detailed setup guide
├── PRIVACY_POLICY.md          # Privacy policy
└── TERMS_OF_USE.md            # Terms of use
```

## Configuration

### Google Sheets Integration

The Resource Finder uses Google Sheets for logging. To enable this:

1. Create a Google Service Account
2. Download the service account JSON key
3. Add it to Streamlit secrets as `google_service_account`
4. Share your Google Sheets with the service account email

### Backend API

The Resource Finder connects to a backend proxy API at `https://ai-resource-guide.fly.dev/chat`. Ensure this service is running or update the endpoint in the application code.

## Deployment

This application can be deployed to:
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure
- Any platform supporting Streamlit applications

For Streamlit Cloud deployment:
1. Push code to GitHub
2. Connect your repository to Streamlit Cloud
3. Configure secrets in the Streamlit Cloud dashboard
4. Deploy!

## Development

### Adding New Applications

To add a new application to the HEAL-AI website:

1. Create a new file in `pages/` with naming convention: `N_Application_Name.py`
2. Update `app.py` to include a card for the new application
3. Add any new dependencies to `requirements.txt`

### Contributing

This is currently an internal project. For contributions or questions, contact: brendan12fox@gmail.com

## License

© 2025 HEAL-AI. All Rights Reserved.

This software is proprietary and not licensed for public use or modification.
For licensing inquiries, contact: brendan12fox@gmail.com

## Contact

HEAL-AI  
Email: brendan12fox@gmail.com

## Mission

HEAL-AI is committed to:
- **Health Equity**: Ensuring all individuals have fair access to healthcare resources
- **Accessibility**: Making healthcare information understandable and actionable
- **Innovation**: Leveraging AI and NLP to solve real-world healthcare challenges
- **Community Focus**: Serving underserved populations with targeted solutions

