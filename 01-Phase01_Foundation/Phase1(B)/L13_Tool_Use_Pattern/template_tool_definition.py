"""
TEMPLATE: Tool Definitions (JSON Schema)
==========================================
Use: Define tools for LLM function calling (Anthropic direct)

COPY the tool definitions that match your use case.
Great descriptions = great tool selection by the LLM.

2026 NOTE: Tool definitions themselves are dicts (no routing needed here).
  Routing logic (what to do with response.stop_reason) lives in the executor.
  See template_tool_executor.py for the match/case stop_reason routing pattern.
"""

# ═══════════════════════════════════════════════════════════
# THE GOLDEN RULE FOR TOOL DESCRIPTIONS:
# Write as if explaining to a smart person who's never seen this tool.
# Tell them: what it does, when to use it, when NOT to use it.
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
# TOOL 1: Web Search
# ═══════════════════════════════════════════════════════════
WEB_SEARCH_TOOL = {
    "name": "web_search",
    "description": (
        "Search the internet for current, real-time information. "
        "Use this when you need: recent news, current prices, live data, "
        "recent events, or any information that may have changed after "
        "your training cutoff date. "
        "Do NOT use for: mathematical calculations, reading local files, "
        "or information you already know with high confidence."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Specific, targeted search query. Include key terms, "
                    "names, and dates. Good: 'Anthropic Claude 4 release date 2025'. "
                    "Bad: 'tell me about claude'."
                )
            }
        },
        "required": ["query"]
    }
}

# ═══════════════════════════════════════════════════════════
# TOOL 2: Calculator
# ═══════════════════════════════════════════════════════════
CALCULATOR_TOOL = {
    "name": "calculator",
    "description": (
        "Evaluate mathematical expressions accurately. "
        "Use for: arithmetic, percentages, unit conversions, financial calculations. "
        "Always use this instead of doing math in your head — LLMs make arithmetic errors. "
        "Do NOT use for: non-math questions, string operations."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": (
                    "Valid Python math expression. Examples: "
                    "'(45 * 12) / 100', '1000 * 1.15 ** 5', '(850 - 600) / 600 * 100'. "
                    "Use ** for exponents, / for division."
                )
            }
        },
        "required": ["expression"]
    }
}

# ═══════════════════════════════════════════════════════════
# TOOL 3: Document Reader
# ═══════════════════════════════════════════════════════════
DOCUMENT_READER_TOOL = {
    "name": "read_document",
    "description": (
        "Read the contents of a local document file. "
        "Use when the user references a specific file or document by name. "
        "Supports: .txt, .md, .py, .json, .csv files. "
        "Do NOT use for: web content (use web_search instead), "
        "or files that haven't been uploaded."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "Filename with extension, e.g. 'report.txt', 'data.json'"
            },
            "start_line": {
                "type": "integer",
                "description": "Optional: line number to start reading from (1-indexed)"
            },
            "end_line": {
                "type": "integer",
                "description": "Optional: line number to stop reading at (inclusive)"
            }
        },
        "required": ["filename"]
    }
}

# ═══════════════════════════════════════════════════════════
# TOOL 4: Database Query (RAG Search)
# ═══════════════════════════════════════════════════════════
RAG_SEARCH_TOOL = {
    "name": "search_knowledge_base",
    "description": (
        "Search the internal knowledge base for relevant information. "
        "Use this FIRST for any question about company products, policies, "
        "documentation, or internal processes. "
        "Returns the most relevant passages ranked by similarity. "
        "Use web_search only if this returns no relevant results."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language query describing what information is needed"
            },
            "top_k": {
                "type": "integer",
                "description": "Number of results to return (1-10, default 3)"
            }
        },
        "required": ["query"]
    }
}

# ═══════════════════════════════════════════════════════════
# TOOL 5: Code Executor (Sandboxed)
# ═══════════════════════════════════════════════════════════
CODE_EXECUTOR_TOOL = {
    "name": "run_python",
    "description": (
        "Execute Python code in a sandboxed environment and return the output. "
        "Use for: data analysis, complex calculations, generating charts, "
        "processing lists or dicts. "
        "The environment has: pandas, numpy, matplotlib. "
        "Does NOT have: internet access, file write access, or external APIs. "
        "Always prefer this over the calculator for multi-step calculations."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": (
                    "Valid Python code to execute. Must print() the result. "
                    "Example: 'import pandas as pd\\ndf = pd.DataFrame([1,2,3])\\nprint(df.describe())'"
                )
            }
        },
        "required": ["code"]
    }
}

# ═══════════════════════════════════════════════════════════
# TOOL 6: Send Notification
# ═══════════════════════════════════════════════════════════
SEND_NOTIFICATION_TOOL = {
    "name": "send_notification",
    "description": (
        "Send a notification message to a user or team. "
        "Use ONLY when the user explicitly asks to notify someone. "
        "Do NOT use this automatically — always confirm with the user first "
        "unless they specifically requested it. "
        "Supported channels: email, slack, sms."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "recipient": {
                "type": "string",
                "description": "Email address, Slack username (@name), or phone number"
            },
            "channel": {
                "type": "string",
                "enum": ["email", "slack", "sms"],
                "description": "Notification channel to use"
            },
            "message": {
                "type": "string",
                "description": "The notification message content"
            }
        },
        "required": ["recipient", "channel", "message"]
    }
}

# ═══════════════════════════════════════════════════════════
# COMPLETE TOOL SETS (ready to use)
# ═══════════════════════════════════════════════════════════

# General-purpose research agent:
RESEARCH_TOOLS = [WEB_SEARCH_TOOL, CALCULATOR_TOOL, DOCUMENT_READER_TOOL]

# RAG agent with search fallback:
RAG_TOOLS = [RAG_SEARCH_TOOL, WEB_SEARCH_TOOL, CALCULATOR_TOOL]

# Full-featured agent:
ALL_TOOLS = [
    WEB_SEARCH_TOOL,
    CALCULATOR_TOOL,
    DOCUMENT_READER_TOOL,
    RAG_SEARCH_TOOL,
    CODE_EXECUTOR_TOOL,
]


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    import json
    print("=== Tool Definitions ===\n")
    for tool in RESEARCH_TOOLS:
        print(f"Tool: {tool['name']}")
        print(f"  {tool['description'][:80]}...")
        print(f"  Required inputs: {tool['input_schema']['required']}")
        print()
    print(f"Total tools in RESEARCH_TOOLS: {len(RESEARCH_TOOLS)}")
    print(f"Total tools in ALL_TOOLS: {len(ALL_TOOLS)}")
