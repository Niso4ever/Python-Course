"""
tools.py — Tool definitions and execution functions for the Research Agent.

In 2026, agents use 10-50 tools. This project has 4 core tools
that cover 90% of research workflows. Each tool has:
  1. A JSON schema definition (tells the LLM what inputs to provide)
  2. An execution function (actually runs the tool)

The agent NEVER calls execution functions directly — it calls the LLM,
which returns a tool_use block, then your code calls the right function.
"""

import os
import json
import math
from datetime import datetime
from pathlib import Path

REPORTS_DIR = os.getenv("REPORTS_DIR", "./reports")

# ═══════════════════════════════════════════════════════════
# TOOL DEFINITIONS (what the LLM sees)
# ═══════════════════════════════════════════════════════════

TOOL_DEFINITIONS = [
    {
        "name": "web_search",
        "description": (
            "Search the internet for current information, news, statistics, and data. "
            "Use this when you need: recent events, current prices, latest reports, "
            "industry statistics, company information, or anything that may have changed "
            "since your training cutoff. "
            "Do NOT use for: pure math, things you know confidently, local files. "
            "In 2026, this searches the live web — results are from today."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Specific, targeted search query. "
                                   "Be precise: 'AI agent market size 2025 billion dollars' "
                                   "is better than 'AI market'."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Number of results to return (1-5). Default: 3.",
                    "default": 3
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": (
            "Evaluate mathematical expressions with full precision. "
            "ALWAYS use this for any arithmetic — LLMs make calculation errors. "
            "Supports: basic arithmetic (+, -, *, /), exponents (**), "
            "percentages (use decimals: 15% = 0.15), "
            "math functions (sqrt, log, abs, round), "
            "and scientific notation (1.5e9). "
            "Example: '245000 * 1.42' or 'round(8432 * 0.15, 2)' or 'math.sqrt(144)'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Valid Python math expression. "
                                   "Use math.sqrt(), math.log(), etc. for functions."
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "read_document",
        "description": (
            "Read the contents of a local file. "
            "Use when: the user provides a file path for background reading, "
            "you need to reference previously saved reports, "
            "or context documents are available on disk. "
            "Supports: .txt, .md, .json, .csv files."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Relative or absolute path to the file to read."
                }
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "write_report",
        "description": (
            "Save the final research report to disk as a Markdown file. "
            "Always use this as the LAST action to persist your research. "
            "The report will be saved with a timestamp and returned to the user."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Report title (used as filename)"
                },
                "content": {
                    "type": "string",
                    "description": "Full report content in Markdown format. "
                                   "Include: executive summary, key findings, data, "
                                   "analysis, and conclusions."
                }
            },
            "required": ["title", "content"]
        }
    }
]


# ═══════════════════════════════════════════════════════════
# TOOL EXECUTION FUNCTIONS
# ═══════════════════════════════════════════════════════════

def execute_web_search(query: str, max_results: int = 3) -> str:
    """
    Execute a web search.
    In production: use Tavily, Exa.ai, or Brave Search API.
    In demo: returns simulated results based on the query topic.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")

    if tavily_key and tavily_key != "tvly-your-key-here":
        try:
            import requests
            response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": tavily_key,
                    "query":   query,
                    "max_results": max_results,
                    "search_depth": "advanced"
                },
                timeout=10
            )
            data    = response.json()
            results = data.get("results", [])
            if results:
                formatted = []
                for r in results[:max_results]:
                    formatted.append(
                        f"Title: {r.get('title', 'N/A')}\n"
                        f"URL: {r.get('url', 'N/A')}\n"
                        f"Content: {r.get('content', '')[:400]}"
                    )
                return "\n\n---\n\n".join(formatted)
        except Exception as e:
            return f"Search API error: {e}. Using simulated results."

    # Simulated results (realistic 2026 AI market data)
    simulated = {
        "AI agent market": (
            "Title: AI Agent Market Size Report 2025-2026\n"
            "The global AI agent market reached $8.2B in 2025, growing 180% YoY. "
            "Key players: Anthropic, OpenAI, Google DeepMind, xAI. "
            "Enterprise adoption: 67% of Fortune 500 companies have deployed at least "
            "one autonomous AI agent as of Q4 2025. Projected 2026 market: $18.5B."
        ),
        "AI investment 2025": (
            "Title: Global AI Investment Trends 2025\n"
            "Total global AI investment in 2025 reached $420B, up 65% from $254B in 2024. "
            "US leads with $180B (43%), followed by China at $95B (23%). "
            "Foundation model companies raised $42B in 2025. "
            "Enterprise AI software grew to $85B market."
        ),
        "Claude": (
            "Title: Anthropic Claude 2026 — Model Capabilities\n"
            "Anthropic's Claude family in late 2026: Fable 5.1 (demanding reasoning), Opus 5.5 (recommended default), "
            "Sonnet 5.5 (speed and intelligence), Haiku 5.5 (fastest). "
            "Context window: 200K tokens across all models. "
            "Claude powers over 60% of enterprise AI assistants deployed in 2026."
        ),
    }

    # Match query to simulated data
    for keyword, result in simulated.items():
        if keyword.lower() in query.lower():
            return result

    # Generic simulated result
    return (
        f"Search results for: '{query}' (simulated)\n\n"
        f"Result 1: Industry analysts project continued growth in AI adoption. "
        f"Key metrics for {query}: market size growing 40-80% annually in 2026. "
        f"Enterprise deployments accelerating. Cost per AI task down 70% vs 2024.\n\n"
        f"Result 2: Leading organizations report 3-5x productivity gains from AI automation. "
        f"Key challenge: governance, security, and AI literacy remain priorities.\n\n"
        f"[Note: Set TAVILY_API_KEY in .env for real web search results]"
    )


def execute_calculator(expression: str) -> str:
    """
    Safely evaluate a math expression.
    Allows: arithmetic, math module functions, basic Python math.
    Blocks: dangerous builtins, file operations, etc.
    """
    # Allowed names for safe evaluation
    safe_globals = {
        "__builtins__": {},
        "math": math,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "len": len,
        "int": int,
        "float": float,
    }

    try:
        result = eval(expression, safe_globals, {})
        # Format nicely: avoid scientific notation for large numbers
        if isinstance(result, float):
            if result == int(result):
                return str(int(result))
            return f"{result:,.4f}".rstrip("0").rstrip(".")
        if isinstance(result, int):
            return f"{result:,}"
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


def execute_read_document(filepath: str) -> str:
    """Read a local file and return its contents."""
    path = Path(filepath)
    if not path.exists():
        return f"File not found: {filepath}"
    if not path.is_file():
        return f"Not a file: {filepath}"

    try:
        content = path.read_text(encoding="utf-8")
        if len(content) > 8000:
            return content[:8000] + f"\n\n[File truncated — showing first 8000 of {len(content)} chars]"
        return content
    except Exception as e:
        return f"Error reading {filepath}: {e}"


def execute_write_report(title: str, content: str) -> str:
    """Save a research report as a Markdown file."""
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Create safe filename from title
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    safe_title = safe_title.replace(" ", "_")[:60]
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename   = f"{safe_title}_{timestamp}.md"
    filepath   = os.path.join(REPORTS_DIR, filename)

    # Add metadata header
    full_content = (
        f"# {title}\n\n"
        f"*Generated by Nexus AI Research Agent — {datetime.now().strftime('%B %d, %Y %H:%M')}*\n\n"
        f"---\n\n"
        f"{content}"
    )

    Path(filepath).write_text(full_content, encoding="utf-8")
    return f"Report saved to: {filepath}"


# ═══════════════════════════════════════════════════════════
# TOOL REGISTRY (maps tool name → execution function)
# ═══════════════════════════════════════════════════════════

TOOL_REGISTRY = {
    "web_search":    execute_web_search,
    "calculator":    execute_calculator,
    "read_document": execute_read_document,
    "write_report":  execute_write_report,
}


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    Route a tool call to the correct execution function.
    Returns the result as a string (tool results must be strings).
    """
    if tool_name not in TOOL_REGISTRY:
        return f"Unknown tool: {tool_name}. Available: {list(TOOL_REGISTRY.keys())}"

    try:
        result = TOOL_REGISTRY[tool_name](**tool_input)
        return str(result)
    except TypeError as e:
        return f"Tool input error for '{tool_name}': {e}"
    except Exception as e:
        return f"Tool execution error for '{tool_name}': {e}"
