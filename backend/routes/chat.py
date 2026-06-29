"""Chat endpoint for the Pathfinder NZ API."""

import asyncio

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.rag.chain import get_rag_response

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    role: str  # "employer" or "applicant"
    history: list[dict] = []


class SourceItem(BaseModel):
    url: str
    title: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message through the RAG pipeline."""
    if request.role not in ("employer", "applicant"):
        raise HTTPException(status_code=400, detail="Role must be 'employer' or 'applicant'.")

    result = await asyncio.to_thread(
        get_rag_response,
        message=request.message,
        role=request.role,
        history=request.history,
    )

    return ChatResponse(answer=result["answer"], sources=result["sources"])
