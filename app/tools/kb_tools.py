"""
Knowledge base search tool for the Enterprise AI Operations Copilot.
Wraps the RAG pipeline as a LangChain tool.
"""

from langchain_core.tools import tool

from app.core.exceptions import LLMError, VectorStoreError
from app.core.logging import get_logger

logger = get_logger(__name__)


@tool
def search_knowledge_base(question: str) -> str:
    """Search the enterprise knowledge base and answer using company documents.

    Args:
        question: The question to look up in the enterprise knowledge base.
    """
    logger.info("Searching knowledge base | question=%s", question)

    try:
        from app.knowledge.rag import answer_question
        return answer_question(question)
    except VectorStoreError as exc:
        logger.error("Vector store unavailable: %s", exc)
        return (
            "⚠️ The knowledge base is not available right now. "
            f"Reason: {exc}"
        )
    except LLMError as exc:
        logger.error("LLM error during RAG: %s", exc)
        return (
            "⚠️ An error occurred while generating the answer. "
            "Please try again."
        )
