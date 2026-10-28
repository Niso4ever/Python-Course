"""
TEMPLATE: Tool Use Loop (Anthropic Direct)
==========================================
Complete tool use implementation using Anthropic SDK directly.

pip install: pip install anthropic python-dotenv

4 variations:
1. Basic tool loop (if/elif stop_reason)
1B. Basic tool loop (match/case stop_reason — 2026 preferred)
2. Multi-tool agent with registry (class + tool loop)
3. Parallel tool calls
4. Tool loop with conversation history

2026 NOTE: Two ways to handle stop_reason routing.
  if/elif style: still valid, easier for some to read
  match/case style: preferred in 2026 real agent code (cleaner, less repetition)
  See Template 1B for the match/case version.
"""
import json
from dotenv import load_dotenv

load_dotenv()


# ═══════════════════════════════════════════════════════════
# SIMULATED TOOLS (replace with real implementations)
# ═══════════════════════════════════════════════════════════
def web_search(query: str) -> str:
    """Simulated web search. Replace with real search API."""
    return f"[Search results for '{query}': Example result 1, Example result 2...]"

def calculator(expression: str) -> str:
    """Safe math evaluator."""
    try:
        # eval is safe here: only allow math, no builtins
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def read_document(filename: str, start_line: int = None, end_line: int = None) -> str:
    """Read a local file."""
    import os
    if not os.path.exists(filename):
        return f"File not found: {filename}"
    with open(filename) as f:
        lines = f.readlines()
    if start_line and end_line:
        lines = lines[start_line-1:end_line]
    return "".join(lines[:50])  # cap at 50 lines

# Tool registry: maps tool name → function
TOOL_REGISTRY = {
    "web_search":    web_search,
    "calculator":    calculator,
    "read_document": read_document,
}

# Tool definitions (JSON schema — what the LLM sees):
TOOLS = [
    {
        "name": "web_search",
        "description": "Search the internet for current, real-time information. Use for recent events, prices, or facts you're unsure about.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": "Evaluate mathematical expressions. Always use this for arithmetic — don't calculate in your head.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "Python math expression, e.g. '15 * 47 / 100'"}},
            "required": ["expression"]
        }
    },
    {
        "name": "read_document",
        "description": "Read a local document file. Use when user references a specific file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename":   {"type": "string"},
                "start_line": {"type": "integer"},
                "end_line":   {"type": "integer"}
            },
            "required": ["filename"]
        }
    }
]


# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Basic Tool Loop
# ═══════════════════════════════════════════════════════════
def run_agent(user_message: str, model: str = "claude-sonnet-5-5") -> str:
    """
    Run a tool-use agent loop until the LLM returns a final answer.

    IN:  user_message (str)
    OUT: final answer (str)
    """
    import anthropic
    client   = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            tools=TOOLS,
            messages=messages
        )

        # LLM finished — return text answer
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return "No text response."

        # LLM wants to use tools
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name  = block.name
                    tool_input = block.input

                    print(f"  → Tool: {tool_name}({json.dumps(tool_input)[:60]})")

                    if tool_name in TOOL_REGISTRY:
                        result = TOOL_REGISTRY[tool_name](**tool_input)
                    else:
                        result = f"Unknown tool: {tool_name}"

                    print(f"    Result: {str(result)[:80]}")

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block.id,
                        "content":     str(result)
                    })

            messages.append({"role": "user", "content": tool_results})


# ═══════════════════════════════════════════════════════════
# TEMPLATE 1B: match/case stop_reason loop (2026 preferred)
# Same logic as Template 1 — cleaner routing syntax
# ═══════════════════════════════════════════════════════════
def run_agent_match(user_message: str, model: str = "claude-sonnet-5-5") -> str:
    """
    Tool-use agent loop using match/case for stop_reason routing.
    Python 3.10+, 2026 preferred style.

    IN:  user_message (str)
    OUT: final answer (str)
    """
    import anthropic
    client   = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            tools=TOOLS,
            messages=messages
        )

        match response.stop_reason:                # ← match/case routing by NAME
            case "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        return block.text
                return "No text response."

            case "tool_use":
                messages.append({"role": "assistant", "content": response.content})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name  = block.name
                        tool_input = block.input

                        print(f"  → Tool: {tool_name}({json.dumps(tool_input)[:60]})")

                        if tool_name in TOOL_REGISTRY:
                            result = TOOL_REGISTRY[tool_name](**tool_input)
                        else:
                            result = f"Unknown tool: {tool_name}"

                        print(f"    Result: {str(result)[:80]}")

                        tool_results.append({
                            "type":        "tool_result",
                            "tool_use_id": block.id,
                            "content":     str(result)
                        })

                messages.append({"role": "user", "content": tool_results})

            case "max_tokens":
                return "[Response truncated — max tokens reached]"

            case _:
                return f"[Unexpected stop reason: {response.stop_reason}]"


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: Agent Class with Tool Registry (L06 + L13)
# ═══════════════════════════════════════════════════════════
class ToolAgent:
    """
    Stateful tool-use agent.
    Combines L06 (class with state) + L13 (tool use loop).
    """
    def __init__(self, tools: list, tool_registry: dict,
                 model: str = "claude-sonnet-5-5",
                 system: str = "You are a helpful assistant with access to tools."):
        import anthropic
        self.client   = anthropic.Anthropic()
        self.tools    = tools
        self.registry = tool_registry
        self.model    = model
        self.system   = system
        self.history  = []         # conversation history
        self.tool_log = []         # log of all tool calls

    def ask(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=self.system,
                tools=self.tools,
                messages=self.history
            )

            match response.stop_reason:              # ← 2026 match/case routing
                case "end_turn":
                    text = next((b.text for b in response.content if hasattr(b, "text")), "")
                    self.history.append({"role": "assistant", "content": text})
                    return text

                case "tool_use":
                    self.history.append({"role": "assistant", "content": response.content})

                    results = []
                    for block in response.content:
                        if block.type == "tool_use":
                            result = self._execute_tool(block.name, block.input)
                            self.tool_log.append({
                                "tool":   block.name,
                                "input":  block.input,
                                "result": result[:200]
                            })
                            results.append({
                                "type":        "tool_result",
                                "tool_use_id": block.id,
                                "content":     str(result)
                            })

                    self.history.append({"role": "user", "content": results})

                case _:
                    return f"[Unexpected stop reason: {response.stop_reason}]"

    def _execute_tool(self, name: str, inputs: dict) -> str:
        if name in self.registry:
            try:
                return str(self.registry[name](**inputs))
            except Exception as e:
                return f"Tool error: {e}"
        return f"Unknown tool: {name}"

    def get_tool_log(self) -> list:
        return self.tool_log

    def reset(self):
        self.history  = []
        self.tool_log = []


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("Tool Use Loop Templates — Demo")
    print("=" * 60)
    print()
    print("TEMPLATE 1: Basic tool loop")
    print("  run_agent('What is 15% of 638.23 billion?')")
    print("  → Agent uses calculator tool automatically")
    print()
    print("TEMPLATE 2: ToolAgent class")
    print("  agent = ToolAgent(TOOLS, TOOL_REGISTRY)")
    print("  agent.ask('Search for latest AI news and summarize')")
    print("  agent.get_tool_log()  # see all tool calls")
    print()
    print("To run with real API: set ANTHROPIC_API_KEY in .env")
    print("Uncomment: run_agent('your question here')")

    # Simulated demo (no API needed):
    print("\n--- Simulated tool execution ---")
    print(f"web_search('AI news 2025'): {web_search('AI news 2025')[:60]}")
    print(f"calculator('638.23 * 0.15'): {calculator('638.23 * 0.15')}")
