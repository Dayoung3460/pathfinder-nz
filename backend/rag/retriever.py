"""ChromaDB retriever for INZ documents."""

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.config import GOOGLE_API_KEY, CHROMA_DB_PATH


def get_retriever():
    """Return a ChromaDB retriever with top-k=5."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(search_kwargs={"k": 5})
