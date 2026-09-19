"""
Expense calculation tool for the Enterprise AI Operations Copilot.
"""

from langchain_core.tools import tool

from app.core.logging import get_logger

logger = get_logger(__name__)


@tool
def calculate_expense(
    amount: float,
    category: str,
    tax_rate: float = 0.0,
) -> str:
    """Calculate the final reimbursable expense amount after applying tax.

    Args:
        amount: Base expense amount (must be >= 0).
        category: Expense category (e.g. Travel, Accommodation, Meals).
        tax_rate: Tax percentage, e.g. 18 for 18% GST. Range: 0–100.
    """
    if amount < 0:
        return "❌ Expense amount cannot be negative."

    if tax_rate < 0 or tax_rate > 100:
        return "❌ Tax rate must be between 0 and 100."

    tax_amount = amount * (tax_rate / 100)
    total_amount = amount + tax_amount

    logger.info(
        "Expense calculated | category=%s | base=%.2f | tax=%.2f | total=%.2f",
        category,
        amount,
        tax_amount,
        total_amount,
    )

    return (
        f"💰 Expense calculation complete.\n\n"
        f"**Category:** {category}\n"
        f"**Base Amount:** ₹{amount:,.2f}\n"
        f"**Tax ({tax_rate}%):** ₹{tax_amount:,.2f}\n"
        f"**Total (Reimbursable):** ₹{total_amount:,.2f}"
    )
