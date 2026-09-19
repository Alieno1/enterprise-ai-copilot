import pytest
import os
from unittest.mock import patch
from app.core.config import Settings
from app.core.exceptions import ConfigurationError

def test_settings_valid(monkeypatch):
    """Test that valid configuration parses correctly."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key_123")
    monkeypatch.setenv("LLM_MODEL", "test-model")
    
    settings = Settings()
    settings.validate()
    
    assert settings.google_api_key == "test_key_123"
    assert settings.llm_model == "test-model"

def test_settings_missing_api_key(monkeypatch):
    """Test that missing Google API key raises an error."""
    # Ensure env variable is not set
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    
    settings = Settings()
    with pytest.raises(ConfigurationError) as exc_info:
        settings.validate()
    
    assert "GOOGLE_API_KEY is not set" in str(exc_info.value)
