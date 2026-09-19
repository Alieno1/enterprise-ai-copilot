#!/usr/bin/env python
"""
Build (or rebuild) the ChromaDB vector store from enterprise documents.

Run from the project root:
    python scripts/build_vectorstore.py

You only need to run this once, or whenever you add/update documents
in data/documents/.
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path when run as a standalone script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.logging import get_logger
from app.knowledge.vectorstore import build_vectorstore

logger = get_logger(__name__)


def main() -> None:
    logger.info("Starting vector store build...")
    try:
        build_vectorstore()
        logger.info("✅ Vector store built successfully.")
    except Exception as exc:
        logger.error("❌ Failed to build vector store: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
