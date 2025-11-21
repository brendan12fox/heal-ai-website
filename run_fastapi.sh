#!/bin/bash
# Run FastAPI app

python3 -m uvicorn fastapi_app:app --host 0.0.0.0 --port 8502 --reload

