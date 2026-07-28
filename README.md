# Pathfinder NZ

NZ visa assistant that answers questions from official Immigration New Zealand documents.

> **Live demo:** https://pathfinder-nz-frontend.onrender.com (React frontend, deployed on Render)

## What it does

Pathfinder NZ answers visa-related questions using a RAG (Retrieval-Augmented Generation) pipeline. It retrieves information exclusively from official INZ documents and generates grounded answers with source citations.

**Two user modes:**
- **Employer / HR Manager** — accreditation, Job Check, hiring overseas workers
- **Visa Applicant / Immigrant** — visa types, eligibility, application procedures

**Key features:**
- Answers grounded in 76+ official INZ document sources
- Source URLs included with every answer
- Relevance filtering — irrelevant sources are excluded automatically
- Fallback response when no relevant document is found
- Legal disclaimer displayed persistently

## Demo

> Screenshots coming soon

<!-- Add screenshots here:
![Role Selection](docs/screenshots/role-selection.png)
![Chat - Employer Mode](docs/screenshots/chat-employer.png)
![Chat - Applicant Mode](docs/screenshots/chat-applicant.png)
-->

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Anthropic Claude (Haiku 4.5) |
| Embeddings | OpenAI (text-embedding-3-small) |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Backend API | FastAPI |
| Frontend UI | React + Vite + Tailwind CSS (primary), Streamlit (legacy) |
| Containerisation | Docker |

## Architecture

```
User (React UI — primary)
    |
Role Selection (Employer / Visa Applicant)
    |
FastAPI Backend (/chat endpoint)
    |
LangChain RAG Pipeline
    |           |
ChromaDB     Claude API
(INZ docs)
    |
Answer + Source URLs returned to UI
```

## Quick Start

### Prerequisites

- Python 3.11+
- [Anthropic API key](https://console.anthropic.com/)
- [OpenAI API key](https://platform.openai.com/api-keys) (for embeddings)

### Option 1: Docker (recommended)

```bash
git clone https://github.com/Dayoung3460/pathfinder-nz.git
cd pathfinder-nz

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Build and run
docker compose up
```

Open http://localhost:3000 in your browser (React frontend). The legacy Streamlit UI is also available at http://localhost:8501.

### Option 2: Local development

```bash
git clone https://github.com/Dayoung3460/pathfinder-nz.git
cd pathfinder-nz

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Ingest INZ documents into ChromaDB (first time only)
python -m backend.rag.ingest
```

Then start both dev servers with one command (Ctrl+C stops both):

```bash
./dev.sh
```

Or run them in separate terminals:

```bash
# Terminal 1 — backend (FastAPI on http://localhost:8000)
uvicorn backend.main:app --reload

# Terminal 2 — frontend (React + Vite)
cd frontend-react
npm install   # first time only
npm run dev
```

Open the URL Vite prints (usually http://localhost:5173) in your browser.

> Troubleshooting: if the chatbot replies "Sorry, an error occurred. Please try again.", check the backend is running: `curl http://localhost:8000/health`

<details>
<summary>Legacy Streamlit UI</summary>

```bash
streamlit run frontend/app.py
```

Open http://localhost:8501 in your browser.

</details>

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude LLM |
| `OPENAI_API_KEY` | Yes | OpenAI API key for embeddings |
| `CHROMA_DB_PATH` | No | ChromaDB storage path (default: `./data/chroma_db`) |
| `BACKEND_URL` | No | Backend URL for frontend (default: `http://localhost:8000`) |

## Project Structure

```
pathfinder-nz/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment variables
│   ├── Dockerfile
│   ├── routes/
│   │   └── chat.py          # POST /chat endpoint
│   ├── rag/
│   │   ├── ingest.py        # Document scraping and ingestion
│   │   ├── retriever.py     # ChromaDB retrieval with relevance filtering
│   │   ├── chain.py         # LangChain RAG chain
│   │   ├── manifest.py      # Content-hash manifest for refresh change detection
│   │   └── urls.py          # INZ source URLs
│   └── prompts/
│       ├── employer.py      # Employer mode system prompt
│       └── applicant.py     # Applicant mode system prompt
├── frontend-react/          # Primary React frontend (Vite + Tailwind CSS)
│   ├── src/
│   └── Dockerfile
├── frontend/                # Legacy Streamlit UI
│   ├── app.py
│   └── Dockerfile
├── data/
│   └── chroma_db/           # ChromaDB persistent storage (committed for Render deploys)
├── docs/
│   ├── PRD.md               # Product requirements
│   ├── ROADMAP.md           # Project roadmap
│   ├── PHASE2_NOTES.md      # Notes from the React rebuild
│   └── TODO.md              # Task tracker
├── .github/workflows/
│   └── refresh.yml          # Weekly document refresh (change detection + Slack summary)
├── docker-compose.yml
├── requirements.txt
└── CLAUDE.md                # AI agent instructions
```

## API

### POST /chat

**Request:**
```json
{
  "message": "What visa do I need to work in New Zealand?",
  "role": "applicant",
  "history": []
}
```

**Response:**
```json
{
  "answer": "Based on official INZ documents...",
  "sources": [
    "https://www.immigration.govt.nz/visas/accredited-employer-work-visa/"
  ]
}
```

## Document Sources

All 76 INZ document URLs are managed in `backend/rag/urls.py`. Categories include:

- Employer accreditation and AEWV
- Skilled Migrant Category (residence)
- Green List occupations
- Partner, student, and visitor visas
- Working holiday and post-study work visas
- Health, character, fees, and processing times
- Application process and supporting documents

A weekly GitHub Actions workflow (`.github/workflows/refresh.yml`) automatically re-scrapes every URL, re-embeds only the ones whose content changed (via a content-hash manifest in `data/refresh_manifest.json`), and posts a Slack summary.

To run this manually:
```bash
python -m backend.rag.ingest                   # full re-ingest
python -m backend.rag.ingest --resume          # only new URLs
python -m backend.rag.ingest --refresh-changed # only URLs whose content changed
python -m backend.rag.ingest --check           # dry run: report changes without embedding
```

## Roadmap

- **Phase 1:** MVP with Streamlit UI — complete
- **Phase 2:** React frontend rebuild for production-quality UX — complete
- **Phase 3 (current):** Production readiness — deployed to Render and automated document refresh are complete; conversation memory, analytics, and an answer-quality evaluation framework remain

See [docs/ROADMAP.md](docs/ROADMAP.md) for details.

## Licence

This project is for portfolio and educational purposes. Immigration New Zealand content is sourced from publicly accessible government web pages.
