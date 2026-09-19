"""
Central tool registry for the Enterprise AI Operations Copilot.

Import TOOLS, TOOLS_MAP, and ACTION_TOOLS from here instead of
importing individual tools directly in the agent layer.
"""

from app.tools.expense_tools import calculate_expense
from app.tools.it_tools import check_ticket_status, create_it_ticket
from app.tools.kb_tools import search_knowledge_base

# Ordered list passed to LLM.bind_tools()
TOOLS = [
    create_it_ticket,
    check_ticket_status,
    calculate_expense,
    search_knowledge_base,
]

# Dict for O(1) tool lookup by name
TOOLS_MAP: dict = {tool.name: tool for tool in TOOLS}

# Tools whose output is returned directly to the user (no LLM synthesis)
ACTION_TOOLS: frozenset[str] = frozenset(
    {
        "create_it_ticket",
        "check_ticket_status",
        "calculate_expense",
    }
)
