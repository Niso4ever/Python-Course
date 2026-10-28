"""
CHEATSHEET L02 — SDK Tools
Define tools the LLM can call.
(Corrected 2026-10-28: the SDK has no Tool() class. Custom tools are @tool handlers
on an in-process MCP server. Source: code.claude.com/docs/en/agent-sdk/custom-tools)
"""
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server

# ── 1. DEFINE A TOOL: @tool(name, description, input_schema) on an async handler ──
@tool(
    "calculate",
    "Evaluate a math expression. Use for arithmetic, percentages, conversions.",
    {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "e.g. '15/100 * 240'"}
        },
        "required": ["expression"],
    },
)
async def calculate(args: dict) -> dict:
    result = str(eval(args["expression"]))          # demo only — never eval untrusted input
    return {"content": [{"type": "text", "text": result}]}   # ← required return shape

# Short schema form also works: {"expression": str}  (every key required)

# ── 2. REGISTER TOOLS WITH THE AGENT ─────────────────────────────────────────
server = create_sdk_mcp_server(name="tools", version="1.0.0", tools=[calculate])
options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    mcp_servers={"tools": server},                  # ← key "tools" becomes part of the name
    allowed_tools=["mcp__tools__calculate"],        # ← NAME STRINGS: mcp__<key>__<tool>
)

# ── 3. TOOL DESCRIPTION RULES ────────────────────────────────────────────────
# BAD:  "Does math"
# GOOD: "Evaluate a math expression. Use for arithmetic, percentages, conversions.
#        Input: Python-valid expression string. Output: numeric result."
#
# RULE: If the LLM can't decide WHEN to call from the description alone → rewrite.

# ── 4. MULTIPLE TOOLS ────────────────────────────────────────────────────────
@tool("search_knowledge_base",
      "Search for factual information. Use for 'what is', 'who is', 'how does'.",
      {"query": str})
async def search(args: dict) -> dict:
    return {"content": [{"type": "text", "text": f"results for {args['query']}"}]}

@tool("analyze_text",
      "Count words and sentences in text. Use for text statistics only.",
      {"text": str})
async def analyzer(args: dict) -> dict:
    return {"content": [{"type": "text", "text": str(len(args["text"].split()))}]}

multi_server = create_sdk_mcp_server(name="multi", tools=[calculate, search, analyzer])
multi_options = ClaudeAgentOptions(
    mcp_servers={"multi": multi_server},
    allowed_tools=["mcp__multi__*"],                # wildcard = every tool on that server
)

# ── 5. TOOL SCHEMA SHAPES ────────────────────────────────────────────────────
# Short:  {"q": str}                                  (all keys required)
# Simple: {"type":"object","properties":{"q":{"type":"string",...}},"required":["q"]}
# Enum:   {"type":"string","enum":["fast","advanced"]}   (needs the full JSON Schema form)
# Nested: {"type":"object","properties":{"filters":{"type":"object","properties":{...}}}}
