# ROADMAP — Pathfinder NZ

This document outlines the current state of the project and planned future improvements.

---

## Phase 1 — MVP

**Status: Complete**

Build a fully functional RAG-based visa assistant with a simple Streamlit UI.

### Goals
- Ingest all verified Immigration NZ documents into ChromaDB
- Role-based Q&A (Employer / Visa Applicant) via LangChain RAG pipeline
- Source citation on every answer
- Standard disclaimer on every answer
- FastAPI backend with `/chat` endpoint
- Streamlit chat UI
- Docker setup for local development

### Tech Stack
- Python, LangChain, ChromaDB, Anthropic Claude API
- FastAPI (backend)
- Streamlit (frontend)
- Docker

---

## Phase 2 — React Frontend Rebuild

**Status: Complete**

Replaced Streamlit with a production-quality React frontend (Vite + Tailwind CSS) in `frontend-react/`. The React app is now the primary frontend deployed on Render; the Streamlit UI remains in `frontend/` as legacy. The FastAPI backend was reused unchanged.

### Why
Streamlit is sufficient for MVP and demo purposes, but has limitations in UI customisation. A React frontend will:
- Deliver a significantly higher quality user experience
- Allow full control over design, layout, and interactions
- Make the project more representative of production-grade AI applications
- Demonstrate full-stack AI engineering capability for portfolio purposes

### Design Approach
Use a DESIGN.md file from [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) to guide the visual design. Candidate styles:
- **Notion** — warm minimalism, clean typography, government-service appropriate
- **Linear** — clean, professional, fast-feeling UI
- **Vercel** — black and white precision, developer-friendly

Claude Code will use the chosen DESIGN.md file to generate consistent, polished React components.

### What Changes
Only the frontend changes. The FastAPI backend (`/chat` endpoint) remains untouched.

| Layer | Phase 1 | Phase 2 |
|---|---|---|
| Frontend | Streamlit | React |
| Backend | FastAPI | FastAPI (unchanged) |
| RAG Pipeline | LangChain + ChromaDB | LangChain + ChromaDB (unchanged) |
| LLM | Anthropic Claude API | Anthropic Claude API (unchanged) |

### Key Implementation Notes
- FastAPI CORS is already configured to accept React frontend requests from day one
- Role selection, chat history, and source citation UI all need to be rebuilt in React
- Use `fetch()` to call the existing `/chat` POST endpoint
- `st.session_state` equivalents: `useState` for role and message history

### Suggested React Stack
- React + TypeScript
- Tailwind CSS (design token mapping from DESIGN.md)
- Native fetch for API calls
- Vite for build tooling

---

## Phase 3 — Production Readiness

**Status: In Progress**

### Completed
- Document refresh pipeline with Slack alerting on every run
  - Implemented as a scheduled job first (Render Cron, then GitHub Actions weekly), then deliberately switched to manual refresh — scheduled runs re-ingested regardless of whether INZ content had changed, which was wasteful on the free tier
- Deployment to Render (React frontend + FastAPI backend, ChromaDB snapshot committed for deploys)
- Automated tests for the retriever, RAG chain, and chat endpoint

### Remaining
- Change detection before re-ingestion, so refresh can be safely re-automated
- Conversation memory across sessions
- Analytics to track most common questions
- Evaluation framework to measure RAG answer quality
