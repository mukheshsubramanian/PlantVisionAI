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
    print("=" * 65)
    print("PLANTVISION AI - Leaf Disease Detection & Care Solutions")
    print("=" * 65)
    print("Starting FastAPI backend server...")
    print("Web Application available at: http://127.0.0.1:8000")
    print("Interactive API Docs available at: http://127.0.0.1:8000/docs")
    print("=" * 65)

    # Automatically open browser
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass

    # Run Uvicorn server
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
