"""Scheduled document refresh pipeline — re-scrape changed INZ pages and re-ingest."""

import hashlib
import json
import logging
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config import (
    CHROMA_DB_PATH,
    GOOGLE_API_KEY,
    HASH_STORE_PATH,
    SLACK_WEBHOOK_URL,
)
from backend.rag.urls import ALL_URLS

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BATCH_SIZE = 50
BATCH_DELAY_SECONDS = 65
MAX_RETRIES = 3


def get_page_hash(url: str) -> str | None:
    """Scrape URL and return SHA-256 hex digest of the page text; None on failure."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        return hashlib.sha256(text.encode()).hexdigest()
    except Exception as e:
        logger.error("Failed to fetch %s: %s", url, e)
        return None


def load_hash_store() -> dict[str, str]:
    """Load url→hash mapping from disk; return empty dict if file does not exist."""
    path = Path(HASH_STORE_PATH)
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save_hash_store(store: dict[str, str]) -> None:
    """Persist url→hash mapping to disk, creating parent directories as needed."""
    path = Path(HASH_STORE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(store, f, indent=2)


def delete_url_chunks(url: str, vectorstore: Chroma) -> None:
    """Remove all ChromaDB chunks whose metadata source matches the given URL."""
    vectorstore._collection.delete(where={"source": url})
    logger.info("Deleted old chunks for: %s", url)


def send_slack_alert(message: str) -> None:
    """POST a message to SLACK_WEBHOOK_URL; silently no-ops if the var is not set."""
    if not SLACK_WEBHOOK_URL:
        return
    try:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
    except Exception as e:
        logger.warning("Failed to send Slack alert: %s", e)


def refresh_documents() -> dict:
    """Re-scrape all INZ URLs, detect changes, and re-ingest only changed pages.

    Returns a summary dict with keys: checked, updated, skipped, failed, failures.
    """
    checked = 0
    updated = 0
    skipped = 0
    failed = 0
    failures: list[str] = []

    hash_store = load_hash_store()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )
    vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for url in ALL_URLS:
        checked += 1
        new_hash = get_page_hash(url)

        if new_hash is None:
            failed += 1
            failures.append(url)
            continue

        if hash_store.get(url) == new_hash:
            skipped += 1
            logger.info("Unchanged: %s", url)
            continue

        try:
            delete_url_chunks(url, vectorstore)

            loader = WebBaseLoader(url)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = url

            chunks = splitter.split_documents(docs)
            total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE

            for i in range(0, len(chunks), BATCH_SIZE):
                batch = chunks[i : i + BATCH_SIZE]
                batch_num = i // BATCH_SIZE + 1

                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        logger.info(
                            "Embedding batch %d/%d for %s...",
                            batch_num, total_batches, url,
                        )
                        vectorstore.add_documents(batch)
                        break
                    except Exception as e:
                        if "429" in str(e) and attempt < MAX_RETRIES:
                            wait = BATCH_DELAY_SECONDS * attempt
                            logger.warning(
                                "Rate limited, retrying in %ds (attempt %d/%d)...",
                                wait, attempt, MAX_RETRIES,
                            )
                            time.sleep(wait)
                        else:
                            raise

                if i + BATCH_SIZE < len(chunks):
                    time.sleep(BATCH_DELAY_SECONDS)

            hash_store[url] = new_hash
            updated += 1
            logger.info("Updated: %s (%d chunks)", url, len(chunks))

        except Exception as e:
            failed += 1
            failures.append(url)
            logger.error("Failed to re-ingest %s: %s", url, e)

    save_hash_store(hash_store)

    summary = {
        "checked": checked,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "failures": failures,
    }

    if failures:
        send_slack_alert(
            f"Pathfinder NZ document refresh completed with {failed} failure(s): "
            + ", ".join(failures)
        )

    logger.info(
        "Refresh complete. Checked: %d, Updated: %d, Skipped: %d, Failed: %d.",
        checked, updated, skipped, failed,
    )
    return summary
