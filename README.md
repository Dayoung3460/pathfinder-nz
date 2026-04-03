# Pathfinder NZ

AI-powered New Zealand visa assistant built on official Immigration New Zealand documents.

> **Note:** This project is under active development.

## What it does

- Answers visa-related questions using a RAG pipeline over official INZ documents
- Two modes: **Employer / HR Manager** and **Visa Applicant / Immigrant**
- Every answer includes source URLs and a legal disclaimer

## Tech Stack

- **Backend:** FastAPI, LangChain, ChromaDB
- **Frontend:** Streamlit
- **LLM:** Google Gemini (development) / Anthropic Claude (planned)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API key

# Ingest INZ documents into ChromaDB
python -m backend.rag.ingest

# Start the backend
uvicorn backend.main:app --reload

# Start the frontend (in a separate terminal)
streamlit run frontend/app.py
```

## Project Structure

```
backend/
  main.py          # FastAPI entry point
  config.py        # Environment variables
  routes/chat.py   # /chat endpoint
  rag/
    ingest.py      # Document scraping and ingestion
    retriever.py   # ChromaDB retrieval
    chain.py       # LangChain RAG chain
    urls.py        # INZ source URLs
  prompts/
    employer.py    # Employer mode system prompt
    applicant.py   # Applicant mode system prompt
frontend/
  app.py           # Streamlit UI
```
