"""Admin routes for internal operations."""

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException

from backend.config import REFRESH_SECRET
from backend.rag.refresh import refresh_documents

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/refresh")
async def trigger_refresh(
    background_tasks: BackgroundTasks,
    authorization: str = Header(None),
):
    if not REFRESH_SECRET or authorization != f"Bearer {REFRESH_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorised")
    background_tasks.add_task(refresh_documents)
    return {"status": "refresh started"}
