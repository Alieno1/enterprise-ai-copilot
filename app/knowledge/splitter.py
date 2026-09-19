"""
Document splitter for the enterprise knowledge base.
Splits loaded documents into overlapping chunks for embedding.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks sized for embedding and retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    logger.info(
        "Split %d document(s) into %d chunk(s) "
        "(chunk_size=%d, overlap=%d).",
        len(documents),
        len(chunks),
        settings.chunk_size,
        settings.chunk_overlap,
    )
    return chunks
