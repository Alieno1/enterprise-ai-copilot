import pytest
from app.tools.expense_tools import calculate_expense
from app.tools.it_tools import create_it_ticket, check_ticket_status

def test_calculate_expense():
    """Test expense calculation with tax."""
    result = calculate_expense.invoke({"amount": 1000, "category": "Travel", "tax_rate": 18})
    assert "1,180.00" in result
    
    result = calculate_expense.invoke({"amount": 200, "category": "Meals", "tax_rate": 5})
    assert "210.00" in result

def test_create_it_ticket():
    """Test IT ticket generation and formatting."""
    result = create_it_ticket.invoke({"employee_id": "EMP123", "issue": "Laptop cracked", "priority": "high"})
    assert "IT ticket created successfully" in result
    assert "IT-" in result
    assert "EMP123" in result

def test_check_ticket_status_not_found():
    """Test ticket status check for a non-existent ticket."""
    result = check_ticket_status.invoke({"ticket_id": "1234"})
    assert "No ticket found with ID **1234**" in result

def test_check_ticket_status_valid():
    """Test valid ticket status lookup."""
    # Based on _DEMO_TICKETS in it_tools.py, valid ID is IT-1025-001
    result = check_ticket_status.invoke({"ticket_id": "IT-1025-001"})
    assert "**Ticket ID:** IT-1025-001" in result
    assert "**Status:** Open" in result
