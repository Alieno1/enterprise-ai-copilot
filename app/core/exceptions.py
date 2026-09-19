"""
Custom exception hierarchy for the Enterprise AI Operations Copilot.
All application exceptions inherit from CopilotError for uniform catch blocks.
"""


class CopilotError(Exception):
    """Base exception for all copilot errors."""


class ConfigurationError(CopilotError):
    """Raised when required configuration is missing or invalid."""


class VectorStoreError(CopilotError):
    """Raised for vector store build/load failures."""


class LLMError(CopilotError):
    """Raised when the LLM call fails."""


class ToolExecutionError(CopilotError):
    """Raised when a tool invocation fails unexpectedly."""
