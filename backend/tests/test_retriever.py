"""Unit tests for backend/rag/retriever.py — retrieve_with_scores function.

All ChromaDB and embedding interactions are mocked; no real vector database or
Google API calls are made during these tests.
"""

from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from backend.rag.retriever import retrieve_with_scores, RELEVANCE_THRESHOLD


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_doc(content: str = "Test INZ content.", source: str = "https://immigration.govt.nz/test") -> Document:
    """Return a minimal LangChain Document for use in tests."""
    return Document(page_content=content, metadata={"source": source})


def mock_vectorstore(results: list) -> MagicMock:
    """Return a mock Chroma vectorstore with a fixed similarity_search_with_score output."""
    vs = MagicMock()
    vs.similarity_search_with_score.return_value = results
    return vs


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRetrieveWithScores:

    def test_returns_all_docs_when_all_scores_below_threshold(self):
        doc1 = make_doc("Doc 1", "https://immigration.govt.nz/page1")
        doc2 = make_doc("Doc 2", "https://immigration.govt.nz/page2")
        vs = mock_vectorstore([(doc1, 0.45), (doc2, 0.60)])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("visa requirements")

        assert len(results) == 2
        assert results[0] == (doc1, 0.45)
        assert results[1] == (doc2, 0.60)

    def test_filters_out_docs_above_threshold(self):
        doc_relevant = make_doc("Accredited employer info", "https://immigration.govt.nz/aewv")
        doc_irrelevant = make_doc("Unrelated content", "https://other.example.com/page")
        vs = mock_vectorstore([
            (doc_relevant, 0.50),    # below threshold — kept
            (doc_irrelevant, 0.85),  # above threshold — filtered out
        ])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("employer accreditation")

        assert len(results) == 1
        assert results[0][0] is doc_relevant

    def test_returns_empty_list_when_all_docs_above_threshold(self):
        doc = make_doc()
        vs = mock_vectorstore([(doc, 0.90)])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("Mars colonist visa")

        assert results == []

    def test_returns_empty_list_when_vectorstore_returns_nothing(self):
        vs = mock_vectorstore([])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("What is a VOC?")

        assert results == []

    def test_includes_doc_at_exact_threshold_boundary(self):
        """A score equal to RELEVANCE_THRESHOLD must be included (the filter is <=)."""
        doc = make_doc()
        vs = mock_vectorstore([(doc, RELEVANCE_THRESHOLD)])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("query")

        assert len(results) == 1
        assert results[0][1] == RELEVANCE_THRESHOLD

    def test_excludes_doc_just_above_threshold(self):
        """A score infinitesimally above RELEVANCE_THRESHOLD must be excluded."""
        doc = make_doc()
        vs = mock_vectorstore([(doc, RELEVANCE_THRESHOLD + 0.001)])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("query")

        assert results == []

    def test_passes_query_string_to_vectorstore(self):
        vs = mock_vectorstore([])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            retrieve_with_scores("accredited employer requirements")

        vs.similarity_search_with_score.assert_called_once_with(
            "accredited employer requirements", k=5
        )

    def test_default_k_is_five(self):
        """retrieve_with_scores must default to k=5."""
        vs = mock_vectorstore([])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            retrieve_with_scores("query")

        _, kwargs = vs.similarity_search_with_score.call_args
        assert kwargs.get("k") == 5

    def test_passes_custom_k_to_vectorstore(self):
        vs = mock_vectorstore([])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            retrieve_with_scores("query", k=10)

        vs.similarity_search_with_score.assert_called_once_with("query", k=10)

    def test_result_format_is_list_of_doc_score_tuples(self):
        doc = make_doc()
        vs = mock_vectorstore([(doc, 0.45)])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("query")

        assert isinstance(results, list)
        result_doc, result_score = results[0]
        assert result_doc is doc
        assert result_score == 0.45

    def test_mixed_scores_preserves_order(self):
        """Documents should be returned in the order the vectorstore provides them."""
        doc_a = make_doc("Doc A", "https://immigration.govt.nz/a")
        doc_b = make_doc("Doc B", "https://immigration.govt.nz/b")
        doc_c = make_doc("Doc C — irrelevant", "https://other.com/c")

        vs = mock_vectorstore([
            (doc_a, 0.40),
            (doc_b, 0.65),
            (doc_c, 0.80),  # filtered out
        ])

        with patch("backend.rag.retriever.get_vectorstore", return_value=vs):
            results = retrieve_with_scores("query")

        assert len(results) == 2
        assert results[0][0] is doc_a
        assert results[1][0] is doc_b
