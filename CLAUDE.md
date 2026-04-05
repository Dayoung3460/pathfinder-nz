# CLAUDE.md

This file provides context and guidance for Claude Code when working on the Pathfinder NZ project.
Read this file carefully before writing any code.
Also read `docs/PRD.md` and `docs/ROADMAP.md` before starting any task.

---

## Current LLM Configuration

**Current:**
- LLM: `claude-haiku-4-5-20251001` via `langchain-anthropic`
- Embeddings: `gemini-embedding-001` via `langchain-google-genai`
- Env vars: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`

```python
# LLM (backend/rag/chain.py)
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024)

# Embeddings (backend/rag/retriever.py, backend/rag/ingest.py)
from langchain_google_genai import GoogleGenerativeAIEmbeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
```

---

## Project Overview

**Pathfinder NZ** is an AI-powered New Zealand visa assistant that answers visa-related questions based exclusively on official Immigration New Zealand (INZ) documents.

The developer is a Korean speaker building this project as a portfolio piece for job applications in New Zealand (AI Engineer / AI Software Engineer roles).

**Important language rule:** All user-facing content must be in British English (e.g., "colour" not "color", "organise" not "organize", "authorise" not "authorize").

---

## Target Users

Two distinct user roles, selected at the start of each session:

1. **Employer / HR Manager** — Questions about hiring overseas workers, employer accreditation, Job Check process, Job Offer requirements.
2. **Visa Applicant / Immigrant** — Questions about visa types, requirements, application procedures, SMC residence, partner visas, student visas, VOC.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| LLM | Anthropic Claude API (claude-sonnet-4-20250514) |
| Agent / Chain | LangChain |
| Vector DB | ChromaDB |
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| Containerisation | Docker |

---

## Architecture Overview

```
User (Streamlit UI)
    ↓
Role Selection (Employer / Visa Applicant)
    ↓
FastAPI Backend
    ↓
LangChain RAG Pipeline
    ↓  ↓
ChromaDB   Anthropic Claude API
(INZ docs)
    ↓
Answer + Source URLs returned to UI
```

---

## Key Design Decisions

### 1. Role-based system prompts
When a user selects a role, a different system prompt is passed to the Claude API:
- Employer mode: Answer from the employer's perspective, focusing on accreditation, Job Check, and compliance obligations.
- Visa Applicant mode: Answer from the applicant's perspective, focusing on eligibility, required documents, and step-by-step procedures.

### 2. RAG-only answers
The assistant must only answer based on retrieved INZ documents stored in ChromaDB.
It must never answer from general knowledge alone.
If the relevant document is not found, respond: "I wasn't able to find specific information on that in the official INZ documents. Please check immigration.govt.nz directly or consult a licensed immigration adviser."

### 3. Source citation
Every answer must include the source URLs of the INZ documents used to generate the response.
This is a core trust and reliability feature of the product.

### 4. Disclaimer display
The disclaimer is displayed persistently in the Streamlit sidebar (and will be shown in a fixed location in the React frontend). It is NOT appended to individual chat responses. The LLM system prompts explicitly instruct the model not to include a disclaimer in its output.

### 5. URL validation before adding
Before adding any new URL to `backend/rag/urls.py`, you MUST validate that the URL returns a successful HTTP response (2xx). Never add a URL without checking it first. Do not ask the user to validate URLs — handle it yourself before modifying `urls.py`.

### 6. Document refresh pipeline (critical)
Immigration NZ changes its policies and URLs frequently.
The document ingestion pipeline must be designed to re-scrape and re-index documents on a scheduled or manual basis, not hardcoded as a one-time load.
Do not hardcode document content. Always load from URLs.

---

## Project Structure

```
pathfinder-nz/
├── CLAUDE.md
├── PRD.md
├── README.md
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── main.py               # FastAPI entry point
│   ├── routes/
│   │   └── chat.py           # Chat endpoint
│   ├── rag/
│   │   ├── ingest.py         # Document scraping and ingestion into ChromaDB
│   │   ├── retriever.py      # ChromaDB retrieval logic
│   │   └── chain.py          # LangChain RAG chain
│   ├── prompts/
│   │   ├── employer.py       # System prompt for employer mode
│   │   └── applicant.py      # System prompt for visa applicant mode
│   └── config.py             # Environment variables and settings
├── frontend/
│   └── app.py                # Streamlit UI
├── data/
│   └── chroma_db/            # ChromaDB persistent storage (gitignored)
└── requirements.txt
```

---

## Environment Variables

Required in `.env`:

```
ANTHROPIC_API_KEY=
CHROMA_DB_PATH=./data/chroma_db
```

---

## QA Policy

Always ask the user before running QA. Never run QA automatically without asking first.

Prompt the user to run QA at the following moments:

1. **Feature complete** — when a major feature is fully implemented (e.g. ingest pipeline, RAG chain, FastAPI endpoint, Streamlit UI)
2. **After a bug fix** — when a bug has been fixed, to verify nothing else has broken
3. **Before deployment** — before any cloud deployment to confirm the app is in a releasable state

Use this exact message when prompting:

"✅ [feature/fix name] is complete. Would you like me to run QA now to verify everything is working correctly?"

Wait for the user's confirmation before proceeding with QA.

---



Agents are defined in `.claude/agents/`. **Always automatically select and use the most appropriate agent(s) for each task. Never wait for the user to specify which agent to use.**

For tasks that span multiple areas, use multiple agents in sequence.

| Task type | Agent to use |
|---|---|
| Scraping INZ pages, ChromaDB ingestion, URL config | `document-ingestion-agent` |
| RAG chain, retriever, LLM connection, answer quality | `rag-chain-agent` |
| System prompts, employer/applicant mode, disclaimer | `prompt-engineer-agent` |
| FastAPI endpoints, routes, CORS, error handling | `fastapi-agent` |
| Streamlit UI, role selection, chat interface | `streamlit-ui-agent` |
| Dockerfile, docker-compose, volumes, env vars | `docker-agent` |
| Testing, QA, grounding verification, edge cases | `qa-agent` |

---

## Development Notes

- Always verify INZ URLs before ingesting. URLs change when policies are updated.
- Do not use PyTorch, TensorFlow, or any ML training libraries. This project uses LLM APIs only.
- Keep Streamlit UI simple. The priority is functionality and reliability, not visual complexity.
- Write all user-facing strings in British English.
- All code comments and docstrings should be in English.