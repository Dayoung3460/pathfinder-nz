# ROADMAP — Pathfinder NZ

This document outlines the current state of the project and planned future improvements.

---

## Phase 1 — MVP (Current)

**Status: In Progress**

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

## Phase 2 — React Frontend Rebuild (Planned)

**Status: Planned**

Replace Streamlit with a production-quality React frontend using a DESIGN.md-driven design system.

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
- Use `fetch()` or `axios` to call the existing `/chat` POST endpoint
- `st.session_state` equivalents: `useState` for role and message history

### Suggested React Stack
- React + TypeScript
- Tailwind CSS (design token mapping from DESIGN.md)
- Axios or native fetch for API calls
- Vite for build tooling

---

## Phase 3 — Production Readiness (Future)

**Status: Future Consideration**

Further improvements after Phase 2 is complete.

- Scheduled document refresh pipeline (auto re-scrape INZ URLs weekly)
- Conversation memory across sessions
- Deployment to a cloud platform (e.g., Render, Railway, or AWS)
- Analytics to track most common questions
- Evaluation framework to measure RAG answer quality

---

## Notes for Claude Code

When working on Phase 2:
1. Read the chosen DESIGN.md file before writing any React components
2. Do not modify any files in `backend/` — the FastAPI backend is reused as-is
3. Create the React app in a new `frontend-react/` directory
4. Ensure CORS is working before building UI components
5. Replicate all features from the Streamlit UI: role selection, chat, source citation, disclaimer
