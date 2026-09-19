"""
ChromaDB vector-store management for the enterprise knowledge base.
"""

from langchain_chroma import Chroma

from app.core.config import settings
from app.core.exceptions import VectorStoreError
from app.core.logging import get_logger
from app.knowledge.loader import load_documents
from app.knowledge.splitter import split_documents
from app.llm.embeddings import get_embeddings

logger = get_logger(__name__)


def build_vectorstore() -> Chroma:
    """
    Build and persist the ChromaDB vector store from enterprise documents.
    Call this once (or whenever documents change) before running the app.
    """
    logger.info("Building vector store...")
    documents = load_documents()

    if not documents:
        raise VectorStoreError(
            "No documents found. Add .md files to the documents directory."
        )

    chunks = split_documents(documents)

    persist_dir = settings.chroma_persist_dir
    persist_dir.mkdir(parents=True, exist_ok=True)

    logger.info(
        "Embedding %d chunks into ChromaDB at: %s", len(chunks), persist_dir
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=settings.chroma_collection_name,
        persist_directory=str(persist_dir),
    )

    logger.info("Vector store built successfully.")
    return vectorstore


def get_vectorstore() -> Chroma:
    """
    Load the persisted ChromaDB vector store.
    Raises VectorStoreError if the store has not been built yet.
    """
    persist_dir = settings.chroma_persist_dir

    if not persist_dir.exists() or not any(persist_dir.iterdir()):
        raise VectorStoreError(
            "Vector store not found. Run: python scripts/build_vectorstore.py"
        )

    logger.debug("Loading vector store from: %s", persist_dir)
    return Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=get_embeddings(),
        persist_directory=str(persist_dir),
    )
