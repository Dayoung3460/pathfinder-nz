"""Application configuration loaded from environment variables."""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Validate required settings
_missing = []
if not GOOGLE_API_KEY:
    _missing.append("GOOGLE_API_KEY")

if _missing:
    print(
        f"ERROR: Missing required environment variables: {', '.join(_missing)}. "
        "Please set them in your .env file.",
        file=sys.stderr,
    )
