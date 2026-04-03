"""LangChain RAG chain connecting retriever, LLM, and role-based prompts."""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from backend.rag.retriever import get_retriever
from backend.prompts.employer import EMPLOYER_SYSTEM_PROMPT
from backend.prompts.applicant import APPLICANT_SYSTEM_PROMPT

DISCLAIMER = (
    "\n\n⚠️ This information is based on official Immigration New Zealand documents "
    "and is provided for general guidance only. It is not legal advice. "
    "For decisions that may significantly affect your visa status, "
    "please consult a licensed immigration adviser."
)

PROMPTS = {
    "employer": EMPLOYER_SYSTEM_PROMPT,
    "applicant": APPLICANT_SYSTEM_PROMPT,
}


def _format_docs(docs):
    """Format retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)


def _get_source_urls(docs):
    """Extract unique source URLs from retrieved documents."""
    seen = set()
    urls = []
    for doc in docs:
        url = doc.metadata.get("source", "")
        if url and url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def get_rag_response(message: str, role: str, history: list[dict] | None = None) -> dict:
    """Run the RAG chain and return answer with sources.

    Args:
        message: The user's question.
        role: Either "employer" or "applicant".
        history: Optional list of previous messages [{"role": ..., "content": ...}].

    Returns:
        dict with "answer" (str) and "sources" (list[str]).
    """
    retriever = get_retriever()
    docs = retriever.invoke(message)

    source_urls = _get_source_urls(docs)
    context = _format_docs(docs)

    system_prompt = PROMPTS.get(role, APPLICANT_SYSTEM_PROMPT)

    chat_messages = [("system", system_prompt)]
    if history:
        for msg in history:
            chat_messages.append((msg["role"], msg["content"]))
    chat_messages.append(("human", "{question}"))

    prompt = ChatPromptTemplate.from_messages(chat_messages)

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "question": message})

    if source_urls:
        sources_text = "\n".join(f"- {url}" for url in source_urls)
        answer += f"\n\n📌 Sources:\n{sources_text}"

    answer += DISCLAIMER

    return {"answer": answer, "sources": source_urls}
