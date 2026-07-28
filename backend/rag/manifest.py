"""Content-hash manifest for the INZ document refresh pipeline.

Tracks a SHA-256 hash of each ingested URL's scraped text so that
`backend.rag.ingest.refresh_changed` can detect which INZ pages have
actually changed since the last run and skip re-embedding unchanged
pages, keeping unattended scheduled refreshes cheap and fast.

Stdlib only — no third-party dependencies.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

# backend/rag/manifest.py -> backend/rag -> backend -> repo root
MANIFEST_PATH = Path(__file__).resolve().parents[2] / "data" / "refresh_manifest.json"

_EMPTY_MANIFEST = {"version": 1, "urls": {}}


def load_manifest() -> dict:
    """Load the refresh manifest from disk.

    Returns the empty skeleton if the file is missing, empty, or fails
    to parse. Never raises.
    """
    try:
        raw = MANIFEST_PATH.read_text(encoding="utf-8")
        if not raw.strip():
            return {"version": 1, "urls": {}}
        data = json.loads(raw)
        if not isinstance(data, dict):
            return {"version": 1, "urls": {}}
        data.setdefault("version", 1)
        data.setdefault("urls", {})
        return data
    except Exception:
        return {"version": 1, "urls": {}}


def save_manifest(manifest: dict) -> None:
    """Write the manifest to disk as pretty-printed, sorted JSON."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(manifest, indent=2, sort_keys=True)
    if not text.endswith("\n"):
        text += "\n"
    MANIFEST_PATH.write_text(text, encoding="utf-8")


def normalise_text(text: str) -> str:
    """Collapse whitespace runs and lowercase, to avoid false "changed"
    detections caused by nav/footer whitespace noise or case differences
    in scraped HTML.
    """
    return " ".join(text.split()).lower()


def content_hash(text: str) -> str:
    """Return the SHA-256 hex digest of the normalised text."""
    return hashlib.sha256(normalise_text(text).encode("utf-8")).hexdigest()


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string, e.g. 2026-07-28T03:04:11Z."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
