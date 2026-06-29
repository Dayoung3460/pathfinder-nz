"""Admin routes for internal operations."""

import asyncio

from fastapi import APIRouter, Header, HTTPException

from backend.config import REFRESH_SECRET
from backend.rag.refresh import refresh_documents

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/refresh")
async def trigger_refresh(authorization: str = Header(None)):
    if not REFRESH_SECRET or authorization != f"Bearer {REFRESH_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorised")
    result = await asyncio.to_thread(refresh_documents)
    return result
