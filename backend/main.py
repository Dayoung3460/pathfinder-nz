"""FastAPI application entry point for Pathfinder NZ."""

import asyncio
import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import REFRESH_INTERVAL_HOURS
from backend.rag.refresh import refresh_documents
from backend.routes.admin import router as admin_router
from backend.routes.chat import router as chat_router

logger = logging.getLogger(__name__)


async def _scheduled_refresh() -> None:
    await asyncio.to_thread(refresh_documents)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(_scheduled_refresh, "interval", hours=REFRESH_INTERVAL_HOURS)
    scheduler.start()
    logger.info("Scheduled document refresh every %dh.", REFRESH_INTERVAL_HOURS)
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Pathfinder NZ",
    description="AI-powered NZ visa assistant",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(admin_router)


@app.get("/")
async def root():
    return {"message": "Pathfinder NZ API is running."}


@app.get("/health")
async def health():
    return {"status": "ok"}
