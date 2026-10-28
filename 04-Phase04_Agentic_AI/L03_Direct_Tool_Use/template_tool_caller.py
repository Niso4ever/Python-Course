"""
Template: Direct Tool Use — Runnable Demo
==========================================
Run this file as-is: python template_tool_caller.py

DEMO MODE (default): All tools run locally. No API key needed.
REAL MODE:           Set DEMO_MODE = False + ANTHROPIC_API_KEY in environment.

What this demonstrates:
  - Defining tool schemas
  - Registering tools with the API
  - Parsing tool_use blocks from responses
  - Executing tools and returning results
  - The full one-shot tool use flow (no loop — single tool call)
  - The agent loop flow (multiple tool calls)
"""

import os
import json

DEMO_MODE = True   # Set to False + add ANTHROPIC_API_KEY for real Claude

# ============================================================
# TOOL SCHEMAS (what the LLM sees)
# ============================================================

TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "Search a knowledge base for information about AI, agents, and LLMs. Use this when you need to look up facts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic or question to search for"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform a mathematical calculation. Supports basic arithmetic (+, -, *, /) and percentages.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g. '100 * 0.15'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "format_report",
        "description": "Format content into a structured report section.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Section title"
                },
                "content": {
                    "type": "string",
                    "description": "Main body text"
                },
                "style": {
                    "type": "string",
                    "description": "Formatting style",
                    "enum": ["paragraph", "bullet_points", "summary"],
                    "default": "paragraph"
                }
            },
            "required": ["title", "content"]
        }
    }
]

# ============================================================
# REAL TOOL FUNCTIONS
# ============================================================

KNOWLEDGE_BASE = {
    "rag":    "RAG (Retrieval-Augmented Generation) combines document retrieval with LLM generation to ground responses in real data.",
    "agent":  "An AI agent is an LLM that runs tools in a loop to complete a goal autonomously.",
    "mcp":    "MCP (Model Context Protocol) is an open standard for connecting AI models to tools and data sources universally.",
    "claude": "Claude is Anthropic's family of AI models. Claude Opus 5.5 is the recommended default as of late 2026; Fable 5.1 is for the hardest reasoning.",
    "tool":   "In AI systems, a tool is a function the LLM can call to get information or take action in the world.",
}

def search_knowledge_base(query: str) -> str:
    query_lower = query.lower()
    for key, value in KNOWLEDGE_BASE.items():
        if key in query_lower:
            return value
    return f"No entry found for '{query}'. Try: rag, agent, mcp, claude, tool."

def calculate(expression: str) -> str:
    try:
        # Only safe math operations
        allowed = set("0123456789+-*/.() %")
        if not all(c in allowed for c in expression):
            return "Error: Only basic math allowed."
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

def format_report(title: str, content: str, style: str = "paragraph") -> str:
    if style == "bullet_points":
        lines = content.split(". ")
        body = "\n".join(f"  • {line.strip()}" for line in lines if line.strip())
    elif style == "summary":
        body = content[:200] + ("..." if len(content) > 200 else "")
    else:
        body = content
    return f"\n=== {title.upper()} ===\n{body}\n"

# ============================================================
# DISPATCHER
# ============================================================

TOOL_MAP = {
    "search_knowledge_base": search_knowledge_base,
    "calculate":              calculate,
    "format_report":          format_report,
}

def execute_tools(content_blocks: list) -> list:
    """Execute all tool_use blocks. Returns tool_result list."""
    results = []
    for block in content_blocks:
        if hasattr(block, "type") and block.type == "tool_use":
            print(f"    ⚙  Tool: {block.name}")
            print(f"    →  Args: {json.dumps(block.input)}")
            fn = TOOL_MAP.get(block.name)
            if fn:
                result = fn(**block.input)
            else:
                result = f"Unknown tool: {block.name}"
            print(f"    ←  Result: {str(result)[:100]}")
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result)
            })
    return results

# ============================================================
# DEMO: Simulated LLM responses
# ============================================================

class MockBlock:
    def __init__(self, btype, **kwargs):
        self.type = btype
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockResponse:
    def __init__(self, stop_reason, content):
        self.stop_reason = stop_reason
        self.content = content

_demo_scenarios = {}

def demo_call(scenario: str, messages: list, call_number: list) -> MockResponse:
    """Returns pre-scripted responses for different scenarios."""
    call_number[0] += 1
    n = call_number[0]

    if scenario == "single_tool":
        if n == 1:
            return MockResponse("tool_use", [
                MockBlock("text", text="Let me look up RAG for you."),
                MockBlock("tool_use", id="tu_01", name="search_knowledge_base", input={"query": "rag"})
            ])
        return MockResponse("end_turn", [
            MockBlock("text", text="RAG (Retrieval-Augmented Generation) combines document retrieval with LLM generation to ground responses in real data. It's the foundation of most enterprise AI systems in 2026.")
        ])

    elif scenario == "multi_tool":
        if n == 1:
            return MockResponse("tool_use", [
                MockBlock("text", text="I'll research agents and calculate a cost estimate."),
                MockBlock("tool_use", id="tu_02", name="search_knowledge_base", input={"query": "agent"}),
                MockBlock("tool_use", id="tu_03", name="calculate", input={"expression": "0.000015 * 5000"})
            ])
        elif n == 2:
            return MockResponse("tool_use", [
                MockBlock("text", text="Now I'll format the results."),
                MockBlock("tool_use", id="tu_04", name="format_report",
                          input={"title": "AI Agent Overview", "content": "AI agents run tools in loops. Cost for 5000 tokens: $0.075.", "style": "bullet_points"})
            ])
        return MockResponse("end_turn", [
            MockBlock("text", text="Here's your report:\n\n=== AI AGENT OVERVIEW ===\n  • AI agents run tools in loops.\n  • Cost for 5000 tokens: $0.075.\n\nAgents are the core pattern behind all modern AI automation.")
        ])

# ============================================================
# DEMO 1: Single Tool Call (one-shot)
# ============================================================

def demo_single_tool():
    print("\n" + "="*60)
    print("DEMO 1: Single Tool Call")
    print("Question: What is RAG?")
    print("="*60)

    messages = [{"role": "user", "content": "What is RAG?"}]
    call_num = [0]

    if DEMO_MODE:
        response = demo_call("single_tool", messages, call_num)
    else:
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-opus-5-5", max_tokens=1024,
            tools=TOOLS, messages=messages
        )

    print(f"\nstop_reason: {response.stop_reason}")

    if response.stop_reason == "tool_use":
        print("\nAgent called a tool:")
        tool_results = execute_tools(response.content)

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user",      "content": tool_results})

        if DEMO_MODE:
            final = demo_call("single_tool", messages, call_num)
        else:
            final = client.messages.create(
                model="claude-opus-5-5", max_tokens=1024,
                tools=TOOLS, messages=messages
            )

        print(f"\nFinal answer:\n{final.content[0].text}")

# ============================================================
# DEMO 2: Multiple Tools in One Response
# ============================================================

def demo_multi_tool():
    print("\n" + "="*60)
    print("DEMO 2: Multiple Tools in One Response")
    print("Question: Explain AI agents and the cost for 5000 tokens.")
    print("="*60)

    messages = [{"role": "user", "content": "Explain AI agents and estimate cost for 5000 tokens at $0.000015/token."}]
    call_num = [0]

    while True:
        if DEMO_MODE:
            response = demo_call("multi_tool", messages, call_num)
        else:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-opus-5-5", max_tokens=1024,
                tools=TOOLS, messages=messages
            )

        print(f"\n[Call {call_num[0]}] stop_reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            print(f"\nFinal answer:\n{response.content[0].text}")
            break

        tool_results = execute_tools(response.content)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user",      "content": tool_results})

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    demo_single_tool()
    demo_multi_tool()

    if DEMO_MODE:
        print("\n" + "="*60)
        print("[DEMO MODE] Set DEMO_MODE = False + ANTHROPIC_API_KEY for real Claude.")
