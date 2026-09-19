"""
Document loader for the enterprise knowledge base.
Loads all Markdown files from the configured documents directory.
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

from app.core.config import settings
from app.core.exceptions import VectorStoreError
from app.core.logging import get_logger

logger = get_logger(__name__)


def load_documents() -> list[Document]:
    """Load all .md documents from the configured documents directory."""
    documents_dir = settings.documents_dir

    if not documents_dir.exists():
        raise VectorStoreError(
            f"Documents directory not found: {documents_dir}. "
            "Create the directory and add Markdown (.md) files."
        )

    logger.info("Loading documents from: %s", documents_dir)

    loader = DirectoryLoader(
        str(documents_dir),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = loader.load()
    logger.info("Loaded %d document(s).", len(documents))
    return documents
