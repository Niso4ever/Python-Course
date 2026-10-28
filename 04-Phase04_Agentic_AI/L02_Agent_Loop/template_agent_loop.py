"""
Template: Agent Loop — Runnable Demo
======================================
Run this file as-is: python template_agent_loop.py

DEMO MODE (default): Simulates tool calls locally. No API key needed.
REAL MODE:           Set ANTHROPIC_API_KEY in environment and set demo=False.

What this demonstrates:
  - The full agent loop (while True + stop_reason)
  - Tool dispatcher pattern
  - Message accumulation over iterations
  - Max iterations safety guard
  - Logging each step so you can watch the loop execute
"""

import os
import json

# ============================================================
# DEMO MODE: Simulated tool + simulated LLM responses
# (Replaces real API calls so you can run without a key)
# ============================================================

DEMO_MODE = True  # Set to False and add ANTHROPIC_API_KEY for real calls

# Simulated knowledge base (replaces real web search in demo)
DEMO_KNOWLEDGE = {
    "tokyo population":      "Tokyo's population is approximately 13.96 million (city) / 37.4 million (metro, 2026).",
    "rag definition":        "RAG (Retrieval-Augmented Generation) combines a retrieval system with an LLM to ground responses in real documents.",
    "mcp definition":        "MCP (Model Context Protocol) is Anthropic's 2024 open standard for connecting AI models to tools and data sources.",
    "claude opus 4":         "Claude Opus 5.5 is Anthropic's recommended default model as of late 2026, excelling at complex reasoning and agentic tasks.",
    "agent loop":            "The agent loop is the core pattern of agentic AI: LLM decides → tool executes → result feeds back → repeat until done.",
}

# ============================================================
# TOOL DEFINITIONS (schema the LLM sees)
# ============================================================

TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "Search a knowledge base for information on a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic or question to look up."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "combine_answers",
        "description": "Combine multiple pieces of information into a single coherent answer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pieces": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of information pieces to combine."
                },
                "format": {
                    "type": "string",
                    "description": "Output format: 'paragraph' or 'bullet_points'",
                    "enum": ["paragraph", "bullet_points"]
                }
            },
            "required": ["pieces", "format"]
        }
    }
]

# ============================================================
# REAL TOOL FUNCTIONS
# ============================================================

def search_knowledge_base(query: str) -> str:
    """Search our local knowledge base."""
    query_lower = query.lower()
    for key, value in DEMO_KNOWLEDGE.items():
        if key in query_lower or any(word in query_lower for word in key.split()):
            return value
    return f"No information found for: '{query}'. Try a different search term."

def combine_answers(pieces: list, format: str = "paragraph") -> str:
    """Combine information pieces into structured output."""
    if format == "bullet_points":
        return "\n".join(f"• {piece}" for piece in pieces)
    else:
        return " ".join(pieces)

# ============================================================
# TOOL DISPATCHER
# ============================================================

TOOL_MAP = {
    "search_knowledge_base": search_knowledge_base,
    "combine_answers":        combine_answers,
}

def execute_tools(content_blocks: list) -> list:
    """Execute all tool_use blocks in the agent's response."""
    tool_results = []
    for block in content_blocks:
        if hasattr(block, "type") and block.type == "tool_use":
            print(f"    ⚙  Tool: {block.name}({json.dumps(block.input)})")
            fn = TOOL_MAP.get(block.name)
            if fn:
                result = fn(**block.input)
            else:
                result = f"Unknown tool: {block.name}"
            print(f"    ←  Result: {result[:80]}{'...' if len(result) > 80 else ''}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result)
            })
    return tool_results

# ============================================================
# DEMO AGENT (simulated responses, no API key)
# ============================================================

class DemoResponse:
    """Simulates an Anthropic API response for demo purposes."""
    def __init__(self, stop_reason, content):
        self.stop_reason = stop_reason
        self.content = content

class DemoBlock:
    """Simulates a content block."""
    def __init__(self, block_type, **kwargs):
        self.type = block_type
        for k, v in kwargs.items():
            setattr(self, k, v)

class DemoTextBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text

_demo_step = 0

def demo_llm_call(messages: list) -> DemoResponse:
    """Simulate LLM decisions for the demo. Runs a 3-step plan."""
    global _demo_step
    _demo_step += 1

    if _demo_step == 1:
        # Step 1: Agent decides to search for RAG
        return DemoResponse("tool_use", [
            DemoTextBlock("Let me search for information on RAG."),
            DemoBlock("tool_use", id="tu_001", name="search_knowledge_base",
                      input={"query": "rag definition"})
        ])
    elif _demo_step == 2:
        # Step 2: Agent decides to search for Agent Loop
        return DemoResponse("tool_use", [
            DemoTextBlock("Now let me look up the agent loop."),
            DemoBlock("tool_use", id="tu_002", name="search_knowledge_base",
                      input={"query": "agent loop"})
        ])
    elif _demo_step == 3:
        # Step 3: Agent combines and finishes
        return DemoResponse("tool_use", [
            DemoTextBlock("Let me combine these into a clear answer."),
            DemoBlock("tool_use", id="tu_003", name="combine_answers",
                      input={
                          "pieces": [
                              "RAG (Retrieval-Augmented Generation) combines retrieval with LLMs.",
                              "The agent loop is the core pattern: decide → act → observe → repeat."
                          ],
                          "format": "bullet_points"
                      })
        ])
    else:
        # Step 4: Done
        return DemoResponse("end_turn", [
            DemoTextBlock(
                "Here is what I found:\n\n"
                "• RAG (Retrieval-Augmented Generation) combines retrieval with LLMs.\n"
                "• The agent loop is the core pattern: decide → act → observe → repeat.\n\n"
                "Both are fundamental building blocks of modern AI systems in 2026."
            )
        ])

# ============================================================
# THE AGENT LOOP (REAL VERSION — used in both demo and real mode)
# ============================================================

def run_agent(question: str, max_iterations: int = 10) -> dict:
    """
    The agent loop.
    Works in demo mode (no key) or real mode (with ANTHROPIC_API_KEY).
    """
    messages = [{"role": "user", "content": question}]
    iteration = 0

    print(f"\n{'='*60}")
    print(f"AGENT LOOP STARTING")
    print(f"Question: {question}")
    print(f"{'='*60}")

    while iteration < max_iterations:
        iteration += 1
        print(f"\n[Iteration {iteration}] THINK → calling LLM...")

        # --- LLM CALL (demo or real) ---
        if DEMO_MODE:
            response = demo_llm_call(messages)
        else:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-opus-5-5",
                max_tokens=4096,
                tools=TOOLS,
                messages=messages
            )

        print(f"[Iteration {iteration}] stop_reason = '{response.stop_reason}'")

        # --- DECISION POINT ---
        if response.stop_reason == "end_turn":
            final_answer = response.content[0].text
            print(f"\n{'='*60}")
            print(f"AGENT DONE in {iteration} iteration(s)")
            print(f"{'='*60}")
            return {
                "answer": final_answer,
                "iterations": iteration,
                "status": "complete"
            }

        # --- ACT: execute tools ---
        print(f"[Iteration {iteration}] ACT → executing tools...")
        messages.append({"role": "assistant", "content": response.content})
        tool_results = execute_tools(response.content)

        # --- OBSERVE: feed results back ---
        print(f"[Iteration {iteration}] OBSERVE → feeding results back...")
        messages.append({"role": "user", "content": tool_results})
        print(f"  Messages in context: {len(messages)}")

    return {
        "answer": "Max iterations reached.",
        "iterations": max_iterations,
        "status": "limit_reached"
    }

# ============================================================
# RUN THE DEMO
# ============================================================

if __name__ == "__main__":
    question = "Explain RAG and the agent loop — how do they relate to each other?"

    result = run_agent(question, max_iterations=10)

    print(f"\n{'='*60}")
    print("FINAL ANSWER:")
    print(f"{'='*60}")
    print(result["answer"])
    print(f"\nIterations used: {result['iterations']}")
    print(f"Status: {result['status']}")

    if DEMO_MODE:
        print("\n[DEMO MODE] Set DEMO_MODE = False and add ANTHROPIC_API_KEY to use real Claude.")
