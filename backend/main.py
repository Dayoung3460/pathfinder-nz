"""FastAPI application entry point for Pathfinder NZ."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.chat import router as chat_router

app = FastAPI(title="Pathfinder NZ", description="AI-powered NZ visa assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Pathfinder NZ API is running."}
