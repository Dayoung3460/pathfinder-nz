#!/usr/bin/env bash
# Start backend and frontend dev servers together. Ctrl+C stops both.

set -e

cd "$(dirname "$0")"

cleanup() {
  echo ""
  echo "Stopping dev servers..."
  kill 0
}
trap cleanup INT TERM

.venv/bin/uvicorn backend.main:app --reload &

(cd frontend-react && npm run dev) &

wait
