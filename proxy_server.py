"""
Render entrypoint.

Your Render service is currently configured to run:
  python proxy_server.py

This file starts the FastAPI app via Uvicorn and binds to Render's $PORT.
"""

import os

import uvicorn


def main() -> None:
    port_str = os.getenv("PORT", "8502")
    try:
        port = int(port_str)
    except ValueError:
        port = 8502

    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=port, log_level="info")


if __name__ == "__main__":
    main()

