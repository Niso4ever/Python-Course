"""
TEMPLATE: SDK Agent with Tools
CURRICULUM PATTERN: Ph5-L02
DESCRIPTION: Agent with 3 practical tools — calculator, text analyzer, knowledge search.
             Focus: writing tool descriptions the LLM can use to make correct decisions.
Run with: python template_sdk_tools.py
"""

import asyncio
import re
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

DEMO_MODE = True

# ──────────────────────────────────────────────
# TOOL IMPLEMENTATIONS (real functions)
# ──────────────────────────────────────────────

def calculate(expression: str) -> str:
    """Safely evaluate a math expression.

    Args:
        expression: Python-compatible math string, e.g. '15/100 * 240'.

    Returns:
        Result as a string, or an error message.
    """
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: only numbers and +-*/() allowed"
    try:
        return str(round(eval(expression), 6))  # noqa: S307
    except Exception as e:
        return f"Error: {e}"


def analyze_text(text: str) -> str:
    """Count words, sentences, and characters in text.

    Args:
        text: The text to analyze.

    Returns:
        JSON-style string with word_count, sentence_count, char_count.
    """
    words = len(text.split())
    sentences = len(re.findall(r'[.!?]+', text)) or 1
    chars = len(text)
    return f'{{"word_count": {words}, "sentence_count": {sentences}, "char_count": {chars}}}'


KNOWLEDGE_BASE: dict[str, str] = {
    "rag": "RAG combines a retrieval system with an LLM to ground responses in real documents.",
    "mcp": "MCP (Model Context Protocol) is Anthropic's universal standard for connecting AI to tools.",
    "pydantic": "Pydantic is a Python library for data validation using type hints and BaseModel.",
    "dspy": "DSPy replaces hand-written prompts with declared input/output signatures that optimize automatically.",
}

def search_knowledge(query: str) -> str:
    """Search the knowledge base for factual information.

    Args:
        query: The question or topic to look up.

    Returns:
        Matching knowledge or 'Not found' message.
    """
    q = query.lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key in q:
            return value
    return f"No result found for '{query}' in knowledge base."


# ──────────────────────────────────────────────
# TOOL SCHEMAS (what the LLM sees)
# ──────────────────────────────────────────────

TOOL_SCHEMAS = [
    {
        "name": "calculate",
        "description": (
            "Evaluate a mathematical expression. Use when the user asks for "
            "arithmetic, percentages, conversions, or any numeric calculation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Python-valid math expression, e.g. '15/100 * 240' or '(3+4)*2'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "analyze_text",
        "description": (
            "Count words, sentences, and characters in a piece of text. "
            "Use for text statistics only — NOT for summarization or translation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to analyze"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "search_knowledge",
        "description": (
            "Search the knowledge base for factual information about AI concepts. "
            "Use for questions about RAG, MCP, Pydantic, DSPy, and related topics."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Topic or question to search"}
            },
            "required": ["query"]
        }
    },
]

TOOL_MAP: dict[str, callable] = {
    "calculate":      lambda args: calculate(args["expression"]),
    "analyze_text":   lambda args: analyze_text(args["text"]),
    "search_knowledge": lambda args: search_knowledge(args["query"]),
}


# ──────────────────────────────────────────────
# DEMO TASK ROUTER
# ──────────────────────────────────────────────

class DemoResult(BaseModel):
    task: str = Field(description="Original task")
    tool_called: str = Field(description="Which tool was selected")
    tool_input: str = Field(description="Input sent to the tool")
    tool_result: str = Field(description="Tool output")
    final_answer: str = Field(description="Synthesized answer")

def _demo_run(task: str) -> DemoResult:
    """Simulate the LLM deciding which tool to use."""
    t = task.lower()
    if any(op in t for op in ["%", "calculate", "what is", "how much", "*", "+", "/"]) and any(c.isdigit() for c in t):
        expr = re.findall(r"[\d\s\.\+\-\*\/\(\)%]+", task)
        expression = expr[0].strip().replace("%", "/100*") if expr else "100 * 0.15"
        result = calculate(expression)
        return DemoResult(task=task, tool_called="calculate",
                         tool_input=expression, tool_result=result,
                         final_answer=f"The result of {expression} is {result}.")
    elif any(w in t for w in ["words", "sentences", "characters", "count", "analyze"]):
        sample = "This is a sample text. It has two sentences."
        result = analyze_text(sample)
        return DemoResult(task=task, tool_called="analyze_text",
                         tool_input=sample, tool_result=result,
                         final_answer=f"Text analysis: {result}")
    else:
        result = search_knowledge(task)
        return DemoResult(task=task, tool_called="search_knowledge",
                         tool_input=task, tool_result=result,
                         final_answer=result)


# ──────────────────────────────────────────────
# REAL SDK RUNNER
# ──────────────────────────────────────────────

async def run_tool_agent(task: str) -> str:
    """Run a task through the Agent SDK with all three tools available.

    Args:
        task: The user's question or instruction.

    Returns:
        The agent's final answer.
    """
    if DEMO_MODE:
        result = _demo_run(task)
        return (f"[Tool: {result.tool_called}({result.tool_input})] "
                f"→ {result.tool_result}\nAnswer: {result.final_answer}")

    from claude_agent_sdk import (  # type: ignore
        query, ClaudeAgentOptions, ResultMessage, tool, create_sdk_mcp_server,
    )

    # Each SDK tool = @tool(name, description, input_schema) on an async handler
    # that returns {"content": [{"type": "text", "text": ...}]}.
    py_functions = {"calculate": calculate, "analyze_text": analyze_text,
                    "search_knowledge": search_knowledge}

    def make_sdk_tool(schema: dict):
        func = py_functions[schema["name"]]

        @tool(schema["name"], schema["description"], schema["input_schema"])
        async def handler(args: dict) -> dict:
            return {"content": [{"type": "text", "text": func(**args)}]}
        return handler

    # Tools live on an in-process MCP server; allowed_tools takes NAME STRINGS
    # in the form "mcp__<server key>__<tool name>".
    server = create_sdk_mcp_server(
        name="lesson_tools", version="1.0.0",
        tools=[make_sdk_tool(s) for s in TOOL_SCHEMAS],
    )
    options = ClaudeAgentOptions(
        model="claude-sonnet-5-5",
        system_prompt="Answer using the available tools. Be concise.",
        mcp_servers={"lesson": server},
        allowed_tools=[f"mcp__lesson__{s['name']}" for s in TOOL_SCHEMAS],
    )
    async for msg in query(prompt=task, options=options):
        if isinstance(msg, ResultMessage):
            return msg.result
    return ""


# ──────────────────────────────────────────────
# DEMO
# ──────────────────────────────────────────────

async def main() -> None:
    print("Agent SDK — Tool Use Demo")
    print("=" * 50)
    print("Tools available: calculate | analyze_text | search_knowledge\n")

    tasks = [
        "What is 15% of 240?",
        "How many words are in a typical paragraph?",
        "What is RAG?",
    ]

    for task in tasks:
        print(f"Task: {task}")
        result = await run_tool_agent(task)
        print(f"Result: {result}")
        print()

    mode = "DEMO" if DEMO_MODE else "REAL API"
    print(f"[{mode} MODE]")


if __name__ == "__main__":
    asyncio.run(main())
