"""
Streamlit chat UI for the Enterprise AI Operations Copilot.

Run with:
    streamlit run app/ui/app.py
"""

import sys
from pathlib import Path

# Add project root to sys.path so Streamlit can import the 'app' module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st

from app.agent.runner import run_agent
from app.core.exceptions import CopilotError
from app.core.logging import get_logger

logger = get_logger(__name__)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Enterprise AI Copilot",
    page_icon="🤖",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🤖 Enterprise AI Copilot")
    st.caption("Powered by OpenRouter · LangChain · ChromaDB")
    st.divider()

    st.subheader("🛠️ Available Tools")
    st.markdown(
        """
- **🎫 Create IT Ticket** — Raise a support ticket
- **📋 Check Ticket Status** — Look up a ticket
- **💰 Calculate Expense** — Compute reimbursable amount
- **🔍 Search Knowledge Base** — Query company policies & docs
        """
    )
    st.divider()

    st.subheader("💬 Example Queries")
    examples = [
        "How many leave days do employees get?",
        "Create a high priority IT ticket for EMP1025 — laptop broken",
        "What is the status of IT-2048-001?",
        "Calculate expense of ₹5000 with 18% GST",
        "What are the IT support hours?",
    ]
    for example in examples:
        st.markdown(f"• *{example}*")

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Main chat area ────────────────────────────────────────────────────────────
st.title("Enterprise AI Operations Copilot")
st.caption("Ask about company policies or perform IT and expense operations.")

# Initialise session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your question or request...")

if user_input:
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent and display response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = run_agent(user_input)
                logger.info("Response delivered to UI.")
            except CopilotError as exc:
                logger.error("CopilotError in UI: %s", exc)
                response = f"⚠️ **Error:** {exc}"
            except Exception as exc:
                logger.exception("Unexpected error in UI: %s", exc)
                response = (
                    "⚠️ An unexpected error occurred. "
                    "Please check the console logs or try again."
                )

        st.markdown(response)

    # Append assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})


def main() -> None:
    """Entry point when called as a module."""
    pass  # Streamlit runs the module top-level; this exists for import clarity.
