"""
RAG (Retrieval-Augmented Generation) pipeline for the enterprise knowledge base.
"""

from app.core.exceptions import LLMError, VectorStoreError
from app.core.logging import get_logger
from app.knowledge.vectorstore import get_vectorstore
from app.llm.client import get_llm

logger = get_logger(__name__)

_RAG_PROMPT = """\
You are an enterprise IT and HR support assistant.

Answer the user's question using ONLY the provided context.

If the answer is not present in the context, respond with:
"I don't have enough information in the knowledge base to answer that."

Do NOT invent policies, procedures, or facts.

Context:
{context}

User question:
{question}
"""


def answer_question(question: str) -> str:
    """
    Retrieve relevant documents and generate a grounded answer.

    Returns the LLM answer with a list of source documents appended.
    Raises VectorStoreError or LLMError on failure.
    """
    logger.info("RAG query: %s", question)

    try:
        vectorstore = get_vectorstore()
    except VectorStoreError:
        raise

    from app.core.config import settings

    documents = vectorstore.similarity_search(question, k=settings.rag_top_k)
    logger.info("Retrieved %d document chunk(s).", len(documents))

    if not documents:
        return (
            "I don't have enough information in the knowledge base to answer that.\n\n"
            "Sources:\n- (none)"
        )

    context = "\n\n---\n\n".join(doc.page_content for doc in documents)

    # Collect unique sources
    sources: list[str] = []
    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        if source not in sources:
            sources.append(source)

    prompt = _RAG_PROMPT.format(context=context, question=question)

    try:
        llm = get_llm()
        response = llm.invoke(prompt)
    except Exception as exc:
        raise LLMError(f"LLM call failed: {exc}") from exc

    content = response.content
    if isinstance(content, list):
        content = "\n\n".join(
            str(block.get("text", "")) if isinstance(block, dict) else str(block)
            for block in content
        )
    elif isinstance(content, str) and content.startswith("[{'type': "):
        import ast
        try:
            parsed = ast.literal_eval(content)
            content = "\n\n".join(str(b.get("text", "")) for b in parsed if isinstance(b, dict))
        except Exception:
            pass

    source_text = "\n".join(f"- {s}" for s in sources)
    return f"{content}\n\nSources:\n{source_text}"
