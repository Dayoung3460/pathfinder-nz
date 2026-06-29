"""Render Cron Job entry point — triggers the /admin/refresh endpoint."""

import os
import sys

import requests

backend_url = os.environ["BACKEND_URL"]
secret = os.environ["REFRESH_SECRET"]

try:
    r = requests.post(
        f"{backend_url}/admin/refresh",
        headers={"Authorization": f"Bearer {secret}"},
        timeout=30,
    )
    print(r.status_code, r.text)
    if not r.ok:
        sys.exit(1)
except Exception as e:
    print(f"Failed to trigger refresh: {e}", file=sys.stderr)
    sys.exit(1)
