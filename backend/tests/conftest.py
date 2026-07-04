"""Shared pytest configuration for the Pathfinder NZ backend test suite.

This module runs before any test file is imported, so module-level code here
(env var setup, sys.path manipulation) takes effect before the backend packages
are loaded.  This prevents API key validation errors from ChatAnthropic and
GoogleGenerativeAIEmbeddings when running tests without real credentials.
"""

import os
import sys

# ---------------------------------------------------------------------------
# 1. Set dummy API keys BEFORE any backend module is imported.
#    `setdefault` keeps real keys if already present; otherwise uses placeholders
#    so third-party SDK constructors do not raise "missing API key" errors.
#    The actual client calls are always mocked in tests, so fake keys are safe.
# ---------------------------------------------------------------------------
if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-placeholder-do-not-use"

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "test-google-key-placeholder-do-not-use"

if not os.environ.get("CHROMA_DB_PATH"):
    os.environ["CHROMA_DB_PATH"] = "/tmp/test_chroma_db"

# ---------------------------------------------------------------------------
# 2. Ensure the project root is on sys.path so that absolute imports like
#    `from backend.rag.chain import get_rag_response` resolve correctly.
#    pytest.ini already sets pythonpath = .. but this is kept as a belt-and-
#    braces fallback for editors and direct `python -m pytest` invocations.
# ---------------------------------------------------------------------------
_tests_dir = os.path.dirname(os.path.abspath(__file__))
_backend_dir = os.path.dirname(_tests_dir)
_project_root = os.path.dirname(_backend_dir)

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
