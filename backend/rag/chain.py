"""LangChain RAG chain connecting retriever, LLM, and role-based prompts."""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from backend.rag.retriever import retrieve_with_scores
from backend.prompts.employer import EMPLOYER_SYSTEM_PROMPT
from backend.prompts.applicant import APPLICANT_SYSTEM_PROMPT


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
    results = retrieve_with_scores(message)
    docs = [doc for doc, _score in results]

    source_urls = _get_source_urls(docs)
    context = _format_docs(docs) if docs else ""

    system_prompt = PROMPTS.get(role, APPLICANT_SYSTEM_PROMPT)

    chat_messages = [("system", system_prompt)]
    if history:
        for msg in history:
            chat_messages.append((msg["role"], msg["content"]))
    chat_messages.append(("human", "{question}"))

    prompt = ChatPromptTemplate.from_messages(chat_messages)

    llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=1024)

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "question": message})

    if source_urls:
        sources_text = "\n".join(f"- {url}" for url in source_urls)
        answer += f"\n\n📌 Sources:\n{sources_text}"

    return {"answer": answer, "sources": source_urls}
