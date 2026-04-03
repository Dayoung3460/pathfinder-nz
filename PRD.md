# PRD — Pathfinder NZ

**Product Requirements Document**
Last updated: April 2026

---

## 1. Product Summary

**Pathfinder NZ** is an AI-powered visa assistant that helps users navigate New Zealand's immigration system. It answers visa-related questions based exclusively on official Immigration New Zealand (INZ) documents, using a Retrieval-Augmented Generation (RAG) pipeline.

It serves two distinct user groups: employers/HR managers hiring overseas workers, and immigrants/visa applicants navigating the visa process themselves.

---

## 2. Problem Statement

New Zealand's immigration system is complex and frequently updated. Official INZ documentation is comprehensive but scattered across hundreds of pages, making it difficult for:

- **HR managers** to quickly understand employer obligations, accreditation requirements, and hiring procedures for overseas workers.
- **Immigrants and visa applicants** to find clear, accurate, and up-to-date information about which visa they need, what documents to prepare, and how to navigate the application process.

The consequences of misunderstanding visa requirements can be severe — delayed hires, visa rejections, or legal non-compliance.

---

## 3. Goals

- Provide accurate, document-grounded answers to NZ visa questions.
- Reduce the time users spend navigating the INZ website.
- Build trust through source transparency — every answer cites the INZ document it was based on.
- Serve as a portfolio project demonstrating RAG-based Agentic AI engineering skills for NZ job applications.

---

## 4. Non-Goals

- This is not a legal advice service. It does not replace a licensed immigration adviser.
- It does not support visa applications or form submissions.
- It does not cover immigration law outside of New Zealand.
- It does not handle real-time visa application status checks.

---

## 5. Target Users

### User A — Employer / HR Manager
- Works at a New Zealand company that wants to hire overseas workers.
- Needs to understand the AEWV accreditation process, Job Check requirements, and employer obligations.
- May not be familiar with immigration terminology.

**Example questions:**
- "What type of accreditation do I need to hire 3 overseas workers?"
- "Do I need to advertise the job before applying for a Job Check?"
- "What documents do I need to include in a Job Offer?"

### User B — Visa Applicant / Immigrant
- An overseas worker, student, or family member navigating the NZ visa system.
- Needs to understand visa eligibility, required documents, and application procedures.
- May be planning long-term residence (e.g., SMC Resident Visa).

**Example questions:**
- "What visa do I need to work as a software engineer in NZ?"
- "How long do I need to have lived with my partner to apply for a partner visa?"
- "What are the risks of my student visa being declined?"
- "My employer has changed — do I need to apply for a VOC or Job Change?"

---

## 6. User Flow

### Step 1 — Landing Screen
User lands on the Pathfinder NZ home page.

Displayed elements:
- Product name: **Pathfinder NZ**
- Tagline: *"Your guide to New Zealand visas — powered by official INZ documents."*
- Two role selection buttons:
  - **I'm an Employer / HR Manager**
  - **I'm a Visa Applicant or Immigrant**
- Disclaimer: *"Pathfinder NZ provides general information based on official Immigration New Zealand documents. It is not legal advice. For complex situations, please consult a licensed immigration adviser."*

### Step 2 — Chat Screen
After role selection, user enters the main chat interface.

Displayed elements:
- Selected role badge (e.g., "Employer / HR Mode")
- "Change Role" button
- Welcome message with 3 suggested questions relevant to the selected role
- Chat history
- Text input field + Send button
- "Clear Conversation" button

### Step 3 — Answer Display
Each answer follows this structure:

```
[Answer content in clear, plain British English]

📌 Sources:
- [INZ page title] — immigration.govt.nz/...
- [INZ page title] — immigration.govt.nz/...

⚠️ This information is based on official Immigration New Zealand documents
and is provided for general guidance only. It is not legal advice.
For decisions that may significantly affect your visa status,
please consult a licensed immigration adviser.
```

---

## 7. Features

### MVP (Must Have)

| Feature | Description |
|---|---|
| Role selection | User selects Employer or Visa Applicant at the start |
| RAG-based Q&A | Answers grounded in ChromaDB-indexed INZ documents |
| Source citation | Every answer displays the INZ source URLs used |
| Role-specific system prompts | Different Claude prompts per role for contextual answers |
| Disclaimer on every answer | Standard legal disclaimer appended to all responses |
| Document ingestion pipeline | Script to scrape and index INZ pages into ChromaDB |
| Streamlit chat UI | Simple, clean chat interface |
| FastAPI backend | REST API connecting frontend to RAG pipeline |
| Docker support | docker-compose for local development |
| Fallback response | When no relevant document is found, direct user to immigration.govt.nz |

### Nice to Have (Post-MVP)

| Feature | Description |
|---|---|
| Document refresh scheduler | Automatically re-scrape INZ URLs on a weekly basis |
| Conversation memory | Remember previous messages within a session for follow-up questions |
| Free-text role detection | Detect user role from context without requiring explicit selection |
| Multi-language support | Korean language option for the developer's personal use case |

---

## 8. Visa Topics Covered

### Employer / HR
- AEWV employer accreditation (Standard, High-volume, Triangular)
- Job Check process and advertising requirements
- Job Offer requirements and supporting documents
- Employer obligations and post-accreditation checks
- AEWV recent policy changes (2025)

### Visa Applicant / Immigrant
- Accredited Employer Work Visa (AEWV) — eligibility, requirements, procedure
- Skilled Migrant Category Resident Visa (SMC) — points, median wage, EOI process, 2026 changes
- Partner visas — de facto relationships, cohabitation evidence, 12-month requirement
- Student visas — eligibility, work rights (25 hrs/week), rejection risk factors
- Variation of Conditions (VOC) — job change, employer change, study conditions
- Interim visas — conditions while waiting for a decision

---

## 9. Technical Requirements

### RAG Pipeline
- Documents scraped using LangChain `WebBaseLoader`
- Text split using `RecursiveCharacterTextSplitter` (chunk size: 1000, overlap: 200)
- Embeddings generated using Anthropic or OpenAI embeddings
- Stored and retrieved using ChromaDB (persistent local storage)
- Top-k retrieval: 5 most relevant chunks per query

### LLM
- Model: `claude-sonnet-4-20250514`
- Role-specific system prompts passed per session
- Max tokens: 1024 per response

### API
- FastAPI with a single `/chat` POST endpoint
- Request body: `{ "message": string, "role": "employer" | "applicant", "history": [] }`
- Response body: `{ "answer": string, "sources": [string] }`

### UI
- Streamlit single-page app
- Role selection on first load, stored in `st.session_state`
- Chat history stored in `st.session_state`
- British English throughout all UI copy

### Infrastructure
- Docker Compose for local development
- `.env` file for secrets (not committed to git)
- ChromaDB data directory gitignored

---

## 10. Important Design Constraints

### URL Stability
INZ URLs change when policies are updated. The document ingestion script must:
- Load URLs from a config file (not hardcoded in pipeline logic)
- Log any failed URL fetches clearly
- Be easy to update when URLs change

### Accuracy over completeness
If the retrieved documents do not contain enough information to answer a question confidently, the assistant must say so and direct the user to immigration.govt.nz. It must not hallucinate or guess.

### No personal data storage
The app does not store any user messages or personal information beyond the current browser session.

---

## 11. Success Criteria

This is a portfolio project. Success is defined as:

- A fully functional RAG chatbot that can correctly answer the questions listed in Section 8.
- Source citations appearing on every answer.
- Clean, working Docker setup.
- A well-documented GitHub repository with README, CLAUDE.md, and PRD.md.
- A short demo video showing the app in action.

---

## 12. Timeline

| Phase | Tasks | Duration |
|---|---|---|
| Month 1 | Python fundamentals, Anthropic API basics, LangChain intro, INZ document ingestion into ChromaDB | 4 weeks |
| Month 2 | RAG pipeline, FastAPI backend, role-specific prompts, Streamlit UI | 4 weeks |
| Month 3 | Docker setup, testing, README, demo video, GitHub polish | 4 weeks |
