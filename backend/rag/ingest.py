"""Scrape INZ documents and ingest them into ChromaDB."""

import logging
import time

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.config import GOOGLE_API_KEY, CHROMA_DB_PATH
from backend.rag.urls import ALL_URLS

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BATCH_SIZE = 50
BATCH_DELAY_SECONDS = 65
MAX_RETRIES = 3


def _get_ingested_urls() -> set[str]:
    """Return source URLs already stored in ChromaDB."""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )
        vs = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        results = vs._collection.get(include=["metadatas"])
        return {m.get("source", "") for m in results["metadatas"]}
    except Exception:
        return set()


def ingest_documents(resume: bool = False) -> None:
    """Scrape INZ URLs and store chunks in ChromaDB.

    Args:
        resume: If True, skip URLs already in ChromaDB.
    """
    urls_to_ingest = ALL_URLS
    if resume:
        already_ingested = _get_ingested_urls()
        urls_to_ingest = [u for u in ALL_URLS if u not in already_ingested]
        logger.info("Resume mode: %d URLs already ingested, %d remaining.", len(already_ingested), len(urls_to_ingest))
        if not urls_to_ingest:
            logger.info("All URLs already ingested. Nothing to do.")
            return

    documents = []

    for url in urls_to_ingest:
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = url
            documents.extend(docs)
            logger.info("Loaded: %s", url)
        except Exception as e:
            logger.error("Failed to load %s: %s", url, e)
            continue

    if not documents:
        logger.error("No documents were loaded. Aborting ingestion.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    logger.info("Split into %d chunks from %d documents.", len(chunks), len(documents))

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
    )

    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info("Embedding batch %d/%d (%d chunks)...", batch_num, total_batches, len(batch))
                vectorstore.add_documents(batch)
                break
            except Exception as e:
                if "429" in str(e) and attempt < MAX_RETRIES:
                    wait = BATCH_DELAY_SECONDS * attempt
                    logger.warning("Rate limited on batch %d, retrying in %ds (attempt %d/%d)...", batch_num, wait, attempt, MAX_RETRIES)
                    time.sleep(wait)
                else:
                    raise

        if i + BATCH_SIZE < len(chunks):
            logger.info("Waiting %ds for rate limit...", BATCH_DELAY_SECONDS)
            time.sleep(BATCH_DELAY_SECONDS)

    logger.info(
        "Ingestion complete. %d chunks stored in %s.",
        len(chunks),
        CHROMA_DB_PATH,
    )


if __name__ == "__main__":
    import sys
    ingest_documents(resume="--resume" in sys.argv)
