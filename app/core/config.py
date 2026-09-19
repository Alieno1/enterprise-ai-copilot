"""
Typed application settings loaded from environment variables / .env file.
Import `settings` — do not instantiate Settings directly.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from app.core.exceptions import ConfigurationError

load_dotenv()

# Resolve project root as two levels above this file (app/core/config.py)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass(frozen=True)
class Settings:
    # ── LLM ──────────────────────────────────────────────────────────────────
    google_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gemini-3.6-flash"))

    # ── Embeddings ────────────────────────────────────────────────────────────
    embedding_model: str = field(
        default_factory=lambda: os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )
    )

    # ── Knowledge base ────────────────────────────────────────────────────────
    documents_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("DOCUMENTS_DIR", str(_PROJECT_ROOT / "data" / "documents"))
        )
    )
    chroma_persist_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("CHROMA_PERSIST_DIR", str(_PROJECT_ROOT / "data" / "chroma"))
        )
    )
    chroma_collection_name: str = field(
        default_factory=lambda: os.getenv("CHROMA_COLLECTION", "enterprise_knowledge")
    )

    # ── RAG ───────────────────────────────────────────────────────────────────
    rag_top_k: int = field(default_factory=lambda: int(os.getenv("RAG_TOP_K", "4")))
    chunk_size: int = field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "500")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "100")))

    def validate(self) -> None:
        """Raise ConfigurationError if any required setting is missing."""
        if not self.google_api_key:
            raise ConfigurationError(
                "GOOGLE_API_KEY is not set. "
                "Get your key at https://aistudio.google.com/app/apikey "
                "and create a .env file with GOOGLE_API_KEY=<your_key>."
            )


# Singleton — loaded once at import time
settings = Settings()
settings.validate()
