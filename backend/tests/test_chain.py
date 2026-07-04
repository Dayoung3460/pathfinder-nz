"""Unit tests for backend/rag/chain.py — get_rag_response function.

Both the ChromaDB retriever and the Anthropic LLM are mocked so that no
real API calls are made during these tests.

Mocking strategy
----------------
* ``retrieve_with_scores`` is patched in the ``backend.rag.chain`` namespace
  (where it was imported) so the patched version is called when
  ``get_rag_response`` runs.
* The module-level ``_llm`` singleton is replaced with a ``RunnableLambda``
  that returns a fixed ``AIMessage``.  ``RunnableLambda`` properly implements
  LangChain's ``Runnable`` interface, so the chain composition
  ``prompt | fake_llm | StrOutputParser()`` works correctly without any real
  LLM client.
"""

from unittest.mock import patch

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from backend.rag.chain import get_rag_response


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_doc(content: str = "NZ visa information.", source: str = "https://immigration.govt.nz/test", title: str = "Test Page") -> Document:
    return Document(page_content=content, metadata={"source": source, "title": title})


def make_fake_llm(response_text: str = "Mocked LLM answer.") -> RunnableLambda:
    """Return a ``RunnableLambda`` that acts as a drop-in LLM replacement."""
    return RunnableLambda(lambda _prompt_value: AIMessage(content=response_text))


_FAKE_DOC = make_doc()
_FAKE_RESULTS = [(_FAKE_DOC, 0.45)]


# ---------------------------------------------------------------------------
# Tests — return structure
# ---------------------------------------------------------------------------

class TestGetRagResponseReturnShape:

    def test_returns_dict(self):
        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("What visa do I need?", "applicant")

        assert isinstance(result, dict)

    def test_dict_has_answer_key(self):
        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        assert "answer" in result

    def test_dict_has_sources_key(self):
        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        assert "sources" in result

    def test_answer_is_string(self):
        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=make_fake_llm("Specific answer text.")):
                result = get_rag_response("question", "applicant")

        assert result["answer"] == "Specific answer text."

    def test_sources_is_list(self):
        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        assert isinstance(result["sources"], list)

    def test_sources_contains_dicts_with_url_and_title(self):
        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        for source in result["sources"]:
            assert isinstance(source, dict)
            assert "url" in source
            assert "title" in source


# ---------------------------------------------------------------------------
# Tests — source extraction
# ---------------------------------------------------------------------------

class TestGetRagResponseSources:

    def test_extracts_url_and_title_from_retrieved_docs(self):
        docs = [
            make_doc("Info A", "https://immigration.govt.nz/page-a", "Page A"),
            make_doc("Info B", "https://immigration.govt.nz/page-b", "Page B"),
        ]
        results = [(doc, 0.45) for doc in docs]

        with patch("backend.rag.chain.retrieve_with_scores", return_value=results):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        urls = [s["url"] for s in result["sources"]]
        titles = [s["title"] for s in result["sources"]]
        assert "https://immigration.govt.nz/page-a" in urls
        assert "https://immigration.govt.nz/page-b" in urls
        assert "Page A" in titles
        assert "Page B" in titles

    def test_deduplicates_sources_by_url(self):
        """Two chunks from the same page should produce only one source entry."""
        shared_url = "https://immigration.govt.nz/same-page"
        docs = [
            make_doc("Chunk A", shared_url, "Same Page"),
            make_doc("Chunk B", shared_url, "Same Page"),
        ]
        results = [(doc, 0.45) for doc in docs]

        with patch("backend.rag.chain.retrieve_with_scores", return_value=results):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        urls = [s["url"] for s in result["sources"]]
        assert urls.count(shared_url) == 1

    def test_sources_order_matches_document_order(self):
        url_a = "https://immigration.govt.nz/a"
        url_b = "https://immigration.govt.nz/b"
        docs = [make_doc("Doc A", url_a, "A"), make_doc("Doc B", url_b, "B")]
        results = [(doc, 0.45) for doc in docs]

        with patch("backend.rag.chain.retrieve_with_scores", return_value=results):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        urls = [s["url"] for s in result["sources"]]
        assert urls == [url_a, url_b]

    def test_empty_sources_when_no_docs_retrieved(self):
        with patch("backend.rag.chain.retrieve_with_scores", return_value=[]):
            with patch("backend.rag.chain._llm", new=make_fake_llm("No relevant info found.")):
                result = get_rag_response("What is the visa policy for Mars colonists?", "applicant")

        assert result["sources"] == []

    def test_docs_without_source_metadata_are_skipped(self):
        """Documents that have no 'source' key in metadata must not produce an entry."""
        doc_with_source = make_doc("Doc A", "https://immigration.govt.nz/page", "Page")
        doc_no_source = Document(page_content="Doc B", metadata={})
        results = [(doc_with_source, 0.45), (doc_no_source, 0.50)]

        with patch("backend.rag.chain.retrieve_with_scores", return_value=results):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        urls = [s["url"] for s in result["sources"]]
        assert "" not in urls
        assert "https://immigration.govt.nz/page" in urls

    def test_title_is_empty_string_when_metadata_has_no_title(self):
        """A doc with no title metadata should produce a source with title=''."""
        doc = Document(page_content="content", metadata={"source": "https://immigration.govt.nz/page"})
        results = [(doc, 0.45)]

        with patch("backend.rag.chain.retrieve_with_scores", return_value=results):
            with patch("backend.rag.chain._llm", new=make_fake_llm()):
                result = get_rag_response("question", "applicant")

        assert result["sources"][0]["title"] == ""


# ---------------------------------------------------------------------------
# Tests — role-based system prompts
# ---------------------------------------------------------------------------

class TestGetRagResponseRolePrompts:
    """Verify that the correct system prompt is used for each role."""

    def _capture_system_content(self, role: str, fake_answer: str = "Answer.") -> str:
        captured = []

        def capturing_llm(prompt_value):
            captured.append(prompt_value)
            return AIMessage(content=fake_answer)

        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=RunnableLambda(capturing_llm)):
                get_rag_response("test question", role)

        messages = captured[0].to_messages()
        return messages[0].content  # SystemMessage content

    def test_employer_role_uses_employer_system_prompt(self):
        system_content = self._capture_system_content("employer")
        assert "New Zealand employers and HR managers" in system_content

    def test_applicant_role_uses_applicant_system_prompt(self):
        system_content = self._capture_system_content("applicant")
        assert "people planning to live, work, or study in New Zealand" in system_content

    def test_employer_role_does_not_use_applicant_prompt(self):
        system_content = self._capture_system_content("employer")
        assert "people planning to live, work, or study in New Zealand" not in system_content

    def test_applicant_role_does_not_use_employer_prompt(self):
        system_content = self._capture_system_content("applicant")
        assert "New Zealand employers and HR managers" not in system_content

    def test_unknown_role_falls_back_to_applicant_system_prompt(self):
        """An unrecognised role must fall back to APPLICANT_SYSTEM_PROMPT."""
        system_content = self._capture_system_content("unknown_role")
        assert "people planning to live, work, or study in New Zealand" in system_content


# ---------------------------------------------------------------------------
# Tests — conversation history
# ---------------------------------------------------------------------------

class TestGetRagResponseHistory:

    def _capture_messages(self, history):
        captured = []

        def capturing_llm(prompt_value):
            captured.append(prompt_value)
            return AIMessage(content="Answer.")

        with patch("backend.rag.chain.retrieve_with_scores", return_value=_FAKE_RESULTS):
            with patch("backend.rag.chain._llm", new=RunnableLambda(capturing_llm)):
                get_rag_response("follow-up question", "applicant", history=history)

        return captured[0].to_messages()

    def test_no_history_produces_two_messages(self):
        """Without history: system message + human message = 2 total."""
        messages = self._capture_messages(history=None)
        assert len(messages) == 2

    def test_empty_history_produces_two_messages(self):
        messages = self._capture_messages(history=[])
        assert len(messages) == 2

    def test_history_messages_are_appended(self):
        history = [
            {"role": "human", "content": "Previous question"},
            {"role": "assistant", "content": "Previous answer"},
        ]
        messages = self._capture_messages(history=history)
        # system + 2 history + 1 current human = 4
        assert len(messages) == 4

    def test_history_content_is_present_in_messages(self):
        history = [
            {"role": "human", "content": "My earlier question"},
        ]
        messages = self._capture_messages(history=history)
        message_contents = [m.content for m in messages]
        assert "My earlier question" in message_contents
