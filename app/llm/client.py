"""
LLM client factory for the Enterprise AI Operations Copilot.

Uses OpenRouter via langchain-openai to interact with any target AI model structure.
"""

from typing import Sequence

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_llm() -> ChatOpenAI:
    """Return a configured OpenRouter LLM instance."""
    logger.debug("Initialising LLM client | model=%s via OpenRouter", settings.llm_model)
    return ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        max_tokens=1024,
    )


def get_llm_with_tools(tools: Sequence) -> ChatOpenAI:
    """Return the LLM with the given tools bound for function-calling."""
    llm = get_llm()
    if not tools:
        return llm
    logger.debug("Binding %d tools to LLM", len(tools))
    return llm.bind_tools(list(tools))
