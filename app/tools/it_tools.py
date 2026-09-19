"""
IT support tools for the Enterprise AI Operations Copilot.

Provides:
- create_it_ticket  — raise a new IT support ticket
- check_ticket_status — look up an existing ticket's status
"""

from langchain_core.tools import tool

from app.core.logging import get_logger

logger = get_logger(__name__)

# ── Demo ticket database ──────────────────────────────────────────────────────
_DEMO_TICKETS: dict[str, dict] = {
    "IT-1025-001": {
        "status": "Open",
        "priority": "High",
        "assigned_to": "IT Support Team",
    },
    "IT-2048-001": {
        "status": "In Progress",
        "priority": "Medium",
        "assigned_to": "Network Support Team",
    },
}

_VALID_PRIORITIES = {"low", "medium", "high", "critical"}


@tool
def create_it_ticket(
    employee_id: str,
    issue: str,
    priority: str = "medium",
) -> str:
    """Create an IT support ticket for an employee's technical issue.

    Args:
        employee_id: The employee's unique ID (e.g. EMP1025).
        issue: A description of the technical issue.
        priority: Ticket priority — low, medium, high, or critical.
    """
    priority_lower = priority.lower()

    if priority_lower not in _VALID_PRIORITIES:
        return (
            f"Invalid priority '{priority}'. "
            f"Choose from: {', '.join(sorted(_VALID_PRIORITIES))}."
        )

    # Generate a deterministic demo ticket ID from the last 4 chars of employee_id
    suffix = employee_id[-4:] if len(employee_id) >= 4 else employee_id.zfill(4)
    ticket_id = f"IT-{suffix}-001"

    logger.info(
        "IT ticket created | ticket_id=%s | employee_id=%s | priority=%s",
        ticket_id,
        employee_id,
        priority_lower,
    )

    return (
        f"✅ IT ticket created successfully.\n\n"
        f"**Ticket ID:** {ticket_id}\n"
        f"**Employee ID:** {employee_id}\n"
        f"**Issue:** {issue}\n"
        f"**Priority:** {priority_lower.capitalize()}"
    )


@tool
def check_ticket_status(ticket_id: str) -> str:
    """Check the current status of an existing IT support ticket.

    Args:
        ticket_id: The IT ticket ID (e.g. IT-1025-001).
    """
    logger.info("Checking ticket status | ticket_id=%s", ticket_id)

    ticket = _DEMO_TICKETS.get(ticket_id)

    if not ticket:
        return (
            f"No ticket found with ID **{ticket_id}**.\n"
            "Please verify the ticket ID and try again."
        )

    return (
        f"**Ticket ID:** {ticket_id}\n"
        f"**Status:** {ticket['status']}\n"
        f"**Priority:** {ticket['priority']}\n"
        f"**Assigned to:** {ticket['assigned_to']}"
    )
