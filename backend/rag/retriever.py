"""ChromaDB retriever for INZ documents."""

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.config import GOOGLE_API_KEY, CHROMA_DB_PATH

# ChromaDB uses distance scores
# lower: more similar(Relevant query → scores ~0.45–0.50)
# higher: less relevant(Irrelevant query → scores ~0.80)

# Any chunk scoring above 0.70 gets filtered out,
# so irrelevant sources aren't shown to the user.
RELEVANCE_THRESHOLD = 0.70

_vectorstore: Chroma | None = None


def get_vectorstore() -> Chroma:
    """Return the shared ChromaDB vectorstore instance (initialised once)."""
    global _vectorstore
    if _vectorstore is None:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
        )
        _vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings,
        )
    return _vectorstore


def retrieve_with_scores(query: str, k: int = 5):
    """Return top-k documents filtered by relevance score.

    ChromaDB returns distance scores (lower = more relevant).
    Documents above RELEVANCE_THRESHOLD are excluded.
    """
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=k)
    return [(doc, score) for doc, score in results if score <= RELEVANCE_THRESHOLD]
