"""Scrape INZ documents and ingest them into ChromaDB."""

import logging

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.config import GOOGLE_API_KEY, CHROMA_DB_PATH
from backend.rag.urls import ALL_URLS

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def ingest_documents() -> None:
    """Scrape all INZ URLs and store chunks in ChromaDB."""
    documents = []

    for url in ALL_URLS:
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
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
    )
    logger.info(
        "Ingestion complete. %d chunks stored in %s.",
        len(chunks),
        CHROMA_DB_PATH,
    )


if __name__ == "__main__":
    ingest_documents()
