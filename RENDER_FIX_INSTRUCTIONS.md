# Render Deployment Fix - Critical Issue

## Problem

Your Render service is trying to run `python proxy_server.py` but can't find the file because:

**Render is connected to the WRONG repository:**
- Currently connected: `brendan12fox/ai-resource-finder` (branch: `app-deploy`)
- Should be connected: `brendan12fox/heal-ai-website` (branch: `main`)

## Solution: Fix Render Repository Connection

### Option A: Update Existing Service (if possible)

1. Go to Render Dashboard
2. Click on your service (the one showing the error)
3. Go to **Settings** tab
4. Find **"Repository"** or **"Git"** section
5. Click **"Change"** or **"Edit"** next to the repository
6. Update to:
   - **Repository**: `brendan12fox/heal-ai-website`
   - **Branch**: `main`
   - **Root Directory**: (leave blank - repo root)
7. Click **Save**
8. Go to **Manual Deploy** → **Deploy latest commit**

### Option B: Create New Service (if you can't change repo)

1. Render Dashboard → **New** → **Web Service**
2. Connect GitHub → Select `brendan12fox/heal-ai-website`
3. Configure:
   - **Name**: `heal-ai-website` (or any name)
   - **Branch**: `main`
   - **Root Directory**: (blank)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python proxy_server.py`
4. Add Environment Variables:
   - `OPENAI_API_KEY` = your key
   - `GOOGLE_SHEET_ID` = `1wSGt3i8eSX4k_kP3GTR0NaHABFixk3zx2Ppo1_RGhKs`
   - `GOOGLE_SERVICE_ACCOUNT_JSON` = (minified JSON from service_account.json)
5. Create Service → Deploy

## What Should Happen After Fix

After connecting to the correct repo, you should see in Render logs:

```
✅ Connected to Google Sheet by ID: 1wSGt3i8eSX4k_kP3GTR0NaHABFixk3zx2Ppo1_RGhKs
✅ Google Sheets logging initialized successfully
INFO:     Started server process [X]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX (Press CTRL+C to quit)
```

## Current Status

✅ All code is committed to `brendan12fox/heal-ai-website` (branch: `main`)
✅ `proxy_server.py` exists in the repo
✅ Google Sheets logging works locally
✅ Environment variables documented

## Files in Correct Repo

- `proxy_server.py` - Entrypoint for Render
- `fastapi_app.py` - Main FastAPI app
- `utils/google_sheets.py` - Google Sheets logging
- `requirements.txt` - All dependencies
- All templates and static files

## Next Steps

1. Fix Render repository connection (Option A or B above)
2. Add environment variables in Render
3. Deploy and verify logs show success messages
4. Test the deployed site - searches should log to Google Sheets
