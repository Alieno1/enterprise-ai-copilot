"""
Lazy-loaded HuggingFace embeddings singleton.

The model is downloaded and initialised only on the first call to
get_embeddings(), not at import time, so the UI starts instantly.
"""

from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_embeddings: HuggingFaceEmbeddings | None = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """Return the shared embeddings instance, loading it on first call."""
    global _embeddings
    if _embeddings is None:
        logger.info("Loading embedding model: %s", settings.embedding_model)
        _embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
        logger.info("Embedding model loaded.")
    return _embeddings
