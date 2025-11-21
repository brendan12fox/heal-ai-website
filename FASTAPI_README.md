# FastAPI Version - HEAL-AI

This is the **FastAPI version** with full control over layout and no padding issues!

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   ./run_fastapi.sh
   ```
   
   Or manually:
   ```bash
   python3 -m uvicorn fastapi_app:app --host 0.0.0.0 --port 8502 --reload
   ```

3. **Open in browser:**
   ```
   http://localhost:8502
   ```

## Features

- ✅ **Full control** over HTML/CSS - no padding issues!
- ✅ **Direct OpenAI API** integration
- ✅ **Fast and responsive**
- ✅ **Clean, simple code**
- ✅ **Same solid prompt** you know works

## File Structure

```
fastapi_app.py          # Main FastAPI application
templates/
  ├── index.html        # Home page
  ├── resource_finder.html  # Resource Finder app
  └── perioperative.html    # Perioperative Translator (to be added)
static/
  └── css/
      └── style.css      # All your styling
```

## API Endpoints

- `GET /` - Home page
- `GET /resource-finder` - Resource Finder page
- `POST /api/find-resources` - Find resources API
- `POST /api/generate-instructions` - Generate instructions API

## Notes

- The OpenAI API key is hardcoded in `fastapi_app.py` (line 18)
- For production, move it to environment variables
- The app runs on port 8502 (different from Streamlit's 8501)

Enjoy your padding-free app! 🎉

