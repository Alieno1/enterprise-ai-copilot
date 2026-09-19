import pytest
from unittest.mock import MagicMock, patch
from app.agent.runner import run_agent
from app.core.exceptions import ToolExecutionError, LLMError

@patch("app.agent.runner.get_llm_with_tools")
def test_run_agent_no_tools(mock_get_llm):
    """Test when the LLM returns text with no tool calls."""
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.tool_calls = []
    mock_response.content = "I am an AI assistant and do not use tools for this answer."
    
    # First invoke returns the simple response
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm
    
    result = run_agent("Hello")
    assert result == "I am an AI assistant and do not use tools for this answer."

@patch("app.agent.runner.TOOLS_MAP")
@patch("app.agent.runner.ACTION_TOOLS")
@patch("app.agent.runner.get_llm_with_tools")
def test_run_agent_with_action_tool(mock_get_llm, mock_action_tools, mock_tools_map):
    """Test when the LLM decides to call an action tool (like create_ticket)."""
    # Configure tool registry mocks
    mock_action_tools.__contains__.side_effect = lambda x: x == "create_it_ticket"
    mock_tool = MagicMock()
    mock_tool.invoke.return_value = "Ticket created: IT-001"
    mock_tools_map.get.return_value = mock_tool
    
    mock_llm = MagicMock()
    
    # First response makes a tool call
    mock_response_1 = MagicMock()
    mock_response_1.tool_calls = [
        {
            "name": "create_it_ticket",
            "args": {"emp_id": "EMP123", "issue": "break"}
        }
    ]
    
    mock_llm.invoke.return_value = mock_response_1
    mock_get_llm.return_value = mock_llm
    
    result = run_agent("Create ticket")
    assert result == "Ticket created: IT-001"
