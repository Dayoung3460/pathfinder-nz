"""Integration tests for the /chat POST endpoint (backend/routes/chat.py).

``get_rag_response`` is mocked at the route module level so that no real
ChromaDB or Anthropic API calls are made.  FastAPI's ``TestClient`` (backed
by ``httpx``) is used to exercise the full HTTP request/response cycle
including Pydantic validation and HTTP status codes.
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.main import app

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    """Return a Starlette TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture()
def mock_rag(monkeypatch):
    """Patch get_rag_response in the routes module to return a canned response."""
    canned = {
        "answer": "You need an Accredited Employer Work Visa.",
        "sources": [{"url": "https://immigration.govt.nz/aewv", "title": "Accredited Employer Work Visa"}],
    }

    with patch("backend.routes.chat.get_rag_response", return_value=canned) as m:
        yield m


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _post_chat(client: TestClient, payload: dict):
    return client.post("/chat", json=payload)


# ---------------------------------------------------------------------------
# Tests — health check
# ---------------------------------------------------------------------------

class TestRootEndpoint:

    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_running_message(self, client):
        data = client.get("/").json()
        assert "message" in data

    def test_health_endpoint_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_ok_status(self, client):
        data = client.get("/health").json()
        assert data.get("status") == "ok"


# ---------------------------------------------------------------------------
# Tests — happy path
# ---------------------------------------------------------------------------

class TestChatEndpointHappyPath:

    def test_employer_role_returns_200(self, client, mock_rag):
        response = _post_chat(client, {"message": "How do I hire overseas workers?", "role": "employer"})
        assert response.status_code == 200

    def test_applicant_role_returns_200(self, client, mock_rag):
        response = _post_chat(client, {"message": "What visa do I need?", "role": "applicant"})
        assert response.status_code == 200

    def test_response_body_has_answer_field(self, client, mock_rag):
        response = _post_chat(client, {"message": "question", "role": "applicant"})
        assert "answer" in response.json()

    def test_response_body_has_sources_field(self, client, mock_rag):
        response = _post_chat(client, {"message": "question", "role": "applicant"})
        assert "sources" in response.json()

    def test_answer_value_is_string(self, client, mock_rag):
        response = _post_chat(client, {"message": "question", "role": "applicant"})
        assert isinstance(response.json()["answer"], str)

    def test_sources_value_is_list(self, client, mock_rag):
        response = _post_chat(client, {"message": "question", "role": "applicant"})
        assert isinstance(response.json()["sources"], list)

    def test_sources_items_have_url_and_title(self, client, mock_rag):
        response = _post_chat(client, {"message": "question", "role": "applicant"})
        for source in response.json()["sources"]:
            assert "url" in source
            assert "title" in source

    def test_response_reflects_rag_answer(self, client, mock_rag):
        response = _post_chat(client, {"message": "question", "role": "applicant"})
        assert response.json()["answer"] == "You need an Accredited Employer Work Visa."

    def test_response_reflects_rag_sources(self, client, mock_rag):
        response = _post_chat(client, {"message": "question", "role": "applicant"})
        assert response.json()["sources"] == [
            {"url": "https://immigration.govt.nz/aewv", "title": "Accredited Employer Work Visa"}
        ]

    def test_empty_message_with_valid_role_returns_200(self, client, mock_rag):
        """An empty string is a valid ``str`` for Pydantic; the RAG layer handles it."""
        response = _post_chat(client, {"message": "", "role": "applicant"})
        assert response.status_code == 200

    def test_request_with_history_returns_200(self, client, mock_rag):
        payload = {
            "message": "follow-up question",
            "role": "applicant",
            "history": [
                {"role": "human", "content": "earlier question"},
                {"role": "assistant", "content": "earlier answer"},
            ],
        }
        response = _post_chat(client, payload)
        assert response.status_code == 200

    def test_history_is_forwarded_to_rag(self, client, mock_rag):
        history = [{"role": "human", "content": "Earlier message"}]
        _post_chat(client, {"message": "follow-up", "role": "applicant", "history": history})
        _, kwargs = mock_rag.call_args
        assert kwargs.get("history") == history or mock_rag.call_args[0][2] == history


# ---------------------------------------------------------------------------
# Tests — role validation (400 from route guard, not Pydantic)
# ---------------------------------------------------------------------------

class TestChatEndpointInvalidRole:

    def test_invalid_role_returns_400(self, client):
        response = _post_chat(client, {"message": "question", "role": "admin"})
        assert response.status_code == 400

    def test_invalid_role_error_detail_mentions_role(self, client):
        response = _post_chat(client, {"message": "question", "role": "superuser"})
        detail = response.json().get("detail", "")
        assert "employer" in detail or "applicant" in detail

    def test_empty_role_returns_400(self, client):
        """An empty string is syntactically valid but rejected by the route guard."""
        response = _post_chat(client, {"message": "question", "role": ""})
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# Tests — Pydantic validation (422)
# ---------------------------------------------------------------------------

class TestChatEndpointValidation:

    def test_missing_message_field_returns_422(self, client):
        response = _post_chat(client, {"role": "applicant"})
        assert response.status_code == 422

    def test_missing_role_field_returns_422(self, client):
        response = _post_chat(client, {"message": "question"})
        assert response.status_code == 422

    def test_missing_both_required_fields_returns_422(self, client):
        response = _post_chat(client, {})
        assert response.status_code == 422

    def test_null_message_returns_422(self, client):
        response = _post_chat(client, {"message": None, "role": "applicant"})
        assert response.status_code == 422

    def test_null_role_returns_422(self, client):
        response = _post_chat(client, {"message": "question", "role": None})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# Tests — upstream error handling
# ---------------------------------------------------------------------------

class TestChatEndpointErrorHandling:

    def test_rag_exception_returns_500(self):
        """If the RAG pipeline raises an unhandled exception, FastAPI returns 500.

        ``raise_server_exceptions=False`` is required here: Starlette's
        ``TestClient`` defaults to re-raising server-side exceptions on the
        client side (to aid debugging), which would turn the 500 into a
        Python exception rather than an HTTP response.  Disabling that
        behaviour lets us assert on the actual HTTP status code.
        """
        no_raise_client = TestClient(app, raise_server_exceptions=False)
        with patch(
            "backend.routes.chat.get_rag_response",
            side_effect=RuntimeError("LLM unreachable"),
        ):
            response = _post_chat(no_raise_client, {"message": "question", "role": "applicant"})
        assert response.status_code == 500
