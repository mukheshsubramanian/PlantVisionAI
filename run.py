"""
PlantVision AI - Application Runner
Launches the FastAPI backend and serves the interactive frontend.
"""

import os
import sys
import webbrowser
from pathlib import Path

# Add backend to Python path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "backend"))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import uvicorn


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8000))
    reload = os.environ.get("RELOAD", "false").lower() in ("true", "1", "yes")

    print("=" * 65)
    print("PLANTVISION AI - Leaf Disease Detection & Care Solutions")
    print("=" * 65)
    print(f"Starting FastAPI backend server on {host}:{port}...")
    print(f"Web Application available at: http://{host}:{port}")
    print(f"Interactive API Docs available at: http://{host}:{port}/docs")
    print("=" * 65)

    # Automatically open browser if running locally
    if host in ("127.0.0.1", "localhost") and not os.environ.get("NO_BROWSER"):
        try:
            webbrowser.open(f"http://{host}:{port}")
        except Exception:
            pass

    # Run Uvicorn server
    uvicorn.run("backend.app:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()

