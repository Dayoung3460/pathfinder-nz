# TODO — Pathfinder NZ

Priority levels: **P0** Critical · **P1** High · **P2** Medium · **P3** Low

---

## Bugs

| # | Priority | Task | Detail |
|---|---|---|---|
| ~~B1~~ | ~~**P0**~~ | ~~Fix blocking sync call in async FastAPI endpoint~~ | ✅ Done — `asyncio.to_thread()` applied in `chat.py`. |
| ~~B2~~ | ~~**P1**~~ | ~~Fix chat scroll behaviour~~ | ✅ Done — on answer load, scrolls to start of new assistant message (`block: 'start'`); scrolls to bottom only while loading. |

---

## PRD Gaps

| # | Priority | Task | Detail |
|---|---|---|---|
| ~~P1~~ | ~~**P1**~~ | ~~Show INZ page title alongside source URLs~~ | ✅ Done — title stored as metadata in `ingest.py`, returned from chain as `{url, title}`, API updated to `SourceItem`, frontend displays `[title] — url`. |
| ~~P2~~ | ~~**P1**~~ | ~~Add automated tests~~ | ✅ Done — 57 tests in `backend/tests/`: unit tests for `retrieve_with_scores` (11), `get_rag_response` (21), and `/chat` integration tests (25). Run: `cd backend && python -m pytest tests/ -v`. |

---

## Minor / Housekeeping

| # | Priority | Task | Detail |
|---|---|---|---|
| ~~M1~~ | ~~**P2**~~ | ~~Add `/health` endpoint to FastAPI~~ | ✅ Done — `GET /health` added to `main.py`. |
| ~~M2~~ | ~~**P2**~~ | ~~Update `CLAUDE.md` project structure~~ | ✅ Done — `frontend-react/` added to Project Structure; Tech Stack and Architecture Overview updated to reflect React as primary frontend. |
| M3 | **P3** | Resolve model inconsistency between docs | `CLAUDE.md` specifies `claude-haiku-4-5-20251001`, PRD specifies `claude-sonnet-4-20250514`. Align both documents with whichever model is actually in use. |

---

## Phase 3 — Production Readiness (Planned)

| # | Priority | Task | Detail |
|---|---|---|---|
| ~~F1~~ | ~~**P2**~~ | ~~Scheduled document refresh pipeline~~ | ✅ Done — `backend/rag/refresh.py` added with SHA-256 content hashing per URL; changed pages are re-ingested, unchanged pages skipped; Slack webhook alert on failures (`SLACK_WEBHOOK_URL`); APScheduler runs weekly via FastAPI lifespan (`REFRESH_INTERVAL_HOURS`, default 168h). |
| F2 | **P2** | Cloud deployment | Deploy to Render / Railway / AWS. `render.yaml` exists but deployment has not been completed. |
| F3 | **P2** | RAG answer quality evaluation framework | Build an eval set of known Q&A pairs from INZ documents. Measure retrieval recall and answer correctness. Needed to validate changes to the RAG pipeline. |
| F4 | **P3** | Conversation memory across sessions | Currently conversation history resets on page reload. Persist messages to localStorage (frontend) or a lightweight DB (backend). |
| F5 | **P3** | Analytics — track most common questions | Log anonymised question categories (not raw text) to understand which topics users ask about most. |
| F6 | **P3** | Demo video | Record a short walkthrough of the app (role selection → question → answer with sources). Required per PRD Section 11 success criteria. |
| F7 | **P3** | Multi-language support (Korean) | Add Korean UI option. Listed as a personal nice-to-have in PRD. Low priority until core features are stable. |