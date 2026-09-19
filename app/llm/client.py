"""
LLM client factory for the Enterprise AI Operations Copilot.

Uses Google Gemini via langchain-google-genai.
"""

from typing import Sequence

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_llm() -> ChatGoogleGenerativeAI:
    """Return a configured Gemini LLM instance."""
    logger.debug("Initialising LLM client | model=%s", settings.llm_model)
    return ChatGoogleGenerativeAI(
        model=settings.llm_model,
        google_api_key=settings.google_api_key,
    )


def get_llm_with_tools(tools: Sequence) -> ChatGoogleGenerativeAI:
    """Return the Gemini LLM with the given tools bound for function-calling."""
    llm = get_llm()
    if not tools:
        return llm
    logger.debug("Binding %d tools to LLM", len(tools))
    return llm.bind_tools(list(tools))

