# CLAUDE.md

This file provides context and guidance for Claude Code when working on the Pathfinder NZ project.
Read this file carefully before writing any code.
Also read `PRD.md` in the project root before starting any task.

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

### 4. Disclaimer on every response
Every response must end with:
"⚠️ This information is based on official Immigration New Zealand documents and is provided for general guidance only. It is not legal advice. For decisions that may significantly affect your visa status, please consult a licensed immigration adviser."

### 5. Document refresh pipeline (critical)
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

## INZ Document Sources

Documents are scraped from the following verified URLs.
All URLs were confirmed accessible as of April 2026.

### Employer / HR
- https://www.immigration.govt.nz/employ-migrants/new-employer-accreditation-and-work-visa
- https://www.immigration.govt.nz/employ-migrants/new-employer-accreditation-and-work-visa/accreditation-types-and-employers-requirements
- https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/aewv-employer-accreditation-and-job-check-process/
- https://www.immigration.govt.nz/work/for-employers/hiring-people-from-overseas/making-a-job-offer/
- https://www.immigration.govt.nz/about-us/news-centre/accredited-employer-work-visa-aewv-key-information-and-statistics/
- https://www.immigration.govt.nz/about-us/news-centre/how-changes-to-the-accredited-employer-work-visa-aewv-may-affect-you/

### AEWV (Work Visa)
- https://www.immigration.govt.nz/visas/accredited-employer-work-visa/
- https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-work-visa
- https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions
- https://www.immigration.govt.nz/work/requirements-for-work-visas/approved-employers/accredited-employer-list/

### Skilled Migrant Category (Residence)
- https://www.immigration.govt.nz/visas/skilled-migrant-category-resident-visa/
- https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/skilled-migrant-category-pathway-to-residence/
- https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/skilled-migrant-category-pathway-to-residence/pay-rates-for-the-skilled-migrant-category-resident-visa/
- https://www.immigration.govt.nz/formshelp/smc-eoi-form
- https://www.immigration.govt.nz/formshelp/smc-visa-application
- https://www.immigration.govt.nz/about-us/news-centre/further-changes-to-the-skilled-migrant-category-to-come-into-effect-in-august-2026/
- https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/
- https://www.immigration.govt.nz/process-to-apply/waiting-for-a-visa/interim-visas-so-you-can-stay-here-lawfully/skilled-migrant-category-interim-visa/

### Partner Visas
- https://www.immigration.govt.nz/process-to-apply/once-you-have-a-visa/bringing-family-to-new-zealand/partnership-and-how-to-prove-it/
- https://www.immigration.govt.nz/about-us/news-centre/partnership-visas/
- https://www.immigration.govt.nz/visas/partner-of-a-new-zealander-visa/
- https://www.immigration.govt.nz/visas/partner-of-a-student-work-visa/
- https://www.immigration.govt.nz/visas/partner-of-a-student-visitor-visa/

### Student Visas
- https://www.immigration.govt.nz/study/study-visas/
- https://www.immigration.govt.nz/assist-migrants-and-students/assist-students/student-visa-info
- https://www.immigration.govt.nz/study/once-you-have-a-student-visa/check-or-change-your-student-visa-conditions/
- https://www.immigration.govt.nz/about-us/news-centre/upcoming-changes-to-student-visa-work-rights/
- https://www.immigration.govt.nz/process-to-apply/once-you-have-a-visa/bringing-family-to-new-zealand/bringing-family-on-a-student-visa/

### VOC (Variation of Conditions)
- https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-work-visa
- https://www.immigration.govt.nz/study/once-you-have-a-student-visa/check-or-change-your-student-visa-conditions/
- https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-visitor-visa
- https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions
- https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions-student

### General
- https://www.immigration.govt.nz/new-zealand-visas/preparing-a-visa-application/character-and-identity/good-character/supporting-partner-character
- https://www.immigration.govt.nz/process-to-apply/waiting-for-a-visa/interim-visas-so-you-can-stay-here-lawfully/interim-visa-conditions/

---

## Environment Variables

Required in `.env`:

```
ANTHROPIC_API_KEY=your_key_here
CHROMA_DB_PATH=./data/chroma_db
```

---

## Development Notes

- Always verify INZ URLs before ingesting. URLs change when policies are updated.
- Do not use PyTorch, TensorFlow, or any ML training libraries. This project uses LLM APIs only.
- Keep Streamlit UI simple. The priority is functionality and reliability, not visual complexity.
- Write all user-facing strings in British English.
- All code comments and docstrings should be in English.
