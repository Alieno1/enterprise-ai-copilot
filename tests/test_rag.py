import pytest
from unittest.mock import MagicMock, patch
from app.knowledge.rag import answer_question
from app.core.exceptions import LLMError

@patch("app.knowledge.rag.get_llm")
@patch("app.knowledge.rag.get_vectorstore")
def test_answer_question_valid(mock_get_vectorstore, mock_get_llm):
    """Test that RAG completes successfully when documents are found."""
    # Mock vectorstore
    mock_vectorstore = MagicMock()
    mock_get_vectorstore.return_value = mock_vectorstore
    
    # Mock retriever returning some context
    mock_doc = MagicMock()
    mock_doc.page_content = "Employees get 18 leave days."
    mock_doc.metadata = {"source": "hr_policy.md"}
    mock_vectorstore.similarity_search.return_value = [mock_doc]
    
    # Mock LLM response
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Employees receive 18 days of leave."
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm
    
    # Run test
    result = answer_question("How many leave days?")
    
    assert "Employees receive 18 days of leave" in result
    assert "hr_policy" in result

@patch("app.knowledge.rag.get_llm")
@patch("app.knowledge.rag.get_vectorstore")
def test_answer_question_no_context(mock_get_vectorstore, mock_get_llm):
    """Test that RAG returns a default message if no context matches."""
    mock_vectorstore = MagicMock()
    mock_get_vectorstore.return_value = mock_vectorstore
    
    # Vector store finds no matches
    mock_vectorstore.similarity_search.return_value = []
    
    # Mock LLM response for empty context
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "I don't have information on that in the company knowledge base"
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm
    
    result = answer_question("What is the meaning of life?")
    assert "I don't have enough information" in result
