"""
Agent orchestration for the Enterprise AI Operations Copilot.

Flow:
  1. User input → LLM (with tools bound)
  2. If no tool calls → return LLM content directly
  3. If action tool(s) called → execute and return results directly
  4. If knowledge-base tool called → execute, then ask LLM to synthesise answer
"""

from app.core.exceptions import LLMError, ToolExecutionError
from app.core.logging import get_logger
from app.llm.client import get_llm_with_tools
from app.tools.registry import ACTION_TOOLS, TOOLS, TOOLS_MAP

logger = get_logger(__name__)


def run_agent(user_input: str) -> str:
    """
    Run the agent for a single user turn.

    Args:
        user_input: The raw message from the user.

    Returns:
        A response string ready to display in the UI.

    Raises:
        LLMError: If the LLM call fails.
    """
    logger.info("Agent invoked | input=%r", user_input[:120])

    # ── Step 1: Ask LLM which tool(s) to call (or answer directly) ─────────
    try:
        llm_with_tools = get_llm_with_tools(TOOLS)
        response = llm_with_tools.invoke(user_input)
    except Exception as exc:
        raise LLMError(f"LLM invocation failed: {exc}") from exc

    # ── Step 2: No tool calls — return content directly ────────────────────
    if not response.tool_calls:
        logger.info("No tool calls — returning direct LLM response.")
        
        # Extact text cleanly if Gemini returns a list of content blocks
        content = response.content
        if isinstance(content, list):
            return "\n\n".join(
                str(block.get("text", "")) if isinstance(block, dict) else str(block)
                for block in content
            )
        
        # If it returned a stringified list, try to unpack it
        if isinstance(content, str) and content.startswith("[{'type': "):
            import ast
            try:
                parsed = ast.literal_eval(content)
                return "\n\n".join(str(b.get("text", "")) for b in parsed if isinstance(b, dict))
            except Exception:
                pass
                
        return content

    # ── Step 3: Execute each tool ───────────────────────────────────────────
    tool_results: list[str] = []
    action_tool_called = False

    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool = TOOLS_MAP.get(tool_name)

        logger.info("Tool call: %s | args=%s", tool_name, tool_args)

        if not tool:
            logger.warning("Unknown tool requested: %s", tool_name)
            tool_results.append(
                f"⚠️ Tool '{tool_name}' is not available."
            )
            continue

        try:
            result = tool.invoke(tool_args)
        except Exception as exc:
            logger.error("Tool execution failed | tool=%s | error=%s", tool_name, exc)
            raise ToolExecutionError(
                f"Tool '{tool_name}' failed: {exc}"
            ) from exc

        if tool_name in ACTION_TOOLS:
            action_tool_called = True

        tool_results.append(result)

    # ── Step 4a: Action tool(s) — return results directly (no LLM re-write) ─
    if action_tool_called:
        logger.info("Action tool(s) executed — returning results directly.")
        return "\n\n---\n\n".join(tool_results)

    # ── Step 4b: Knowledge-base — ask LLM to synthesise a natural response ──
    logger.info("Knowledge-base tool executed — synthesising response.")

    synthesis_prompt = f"""\
You are an enterprise AI operations assistant.

The user asked:
{user_input}

A knowledge-base search was performed. Here are the results:

{chr(10).join(tool_results)}

Using ONLY the information above, give the user a concise, helpful answer.
Do NOT invent information that is not present in the tool results.
"""

    try:
        llm = get_llm_with_tools([])   # No tools needed for synthesis
        final_response = llm.invoke(synthesis_prompt)
    except Exception as exc:
        raise LLMError(f"Response synthesis failed: {exc}") from exc

    content = final_response.content
    if isinstance(content, list):
        return "\n\n".join(
            str(block.get("text", "")) if isinstance(block, dict) else str(block)
            for block in content
        )
    if isinstance(content, str) and content.startswith("[{'type': "):
        import ast
        try:
            parsed = ast.literal_eval(content)
            return "\n\n".join(str(b.get("text", "")) for b in parsed if isinstance(b, dict))
        except Exception:
            pass
            
    return content
