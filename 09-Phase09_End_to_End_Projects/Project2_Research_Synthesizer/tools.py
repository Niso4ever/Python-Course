import asyncio

# In a real project, this would use duckduckgo-search or requests/BeautifulSoup
# But here we mock it to run cleanly in DEMO_MODE.

async def search_web(query: str) -> str:
    """Mock web search tool."""
    await asyncio.sleep(0.5)
    print(f"    [Tool] Executed search_web for: '{query}'")
    
    if "agent" in query.lower():
        return "Search Results: AI Agents are autonomous systems that use LLMs as their reasoning engine."
    if "sdk" in query.lower():
        return "Search Results: Anthropic provides an official Agent SDK to handle tool dispatch and streaming."
    return "Search Results: No specific findings."

async def fetch_article(url: str) -> str:
    """Mock article fetcher."""
    await asyncio.sleep(0.5)
    print(f"    [Tool] Executed fetch_article for: '{url}'")
    return "Article Content: The future of AI relies on orchestrating multiple specialized agents rather than relying on a single monolith."

# SDK Tool Definitions
TOOLS = [
    {
        "name": "search_web",
        "description": "Searches the internet for information on a specific topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "fetch_article",
        "description": "Downloads the full text of an article given a URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch"}
            },
            "required": ["url"]
        }
    }
]

# Dispatcher mapping for the SDK or loop
TOOL_REGISTRY = {
    "search_web": search_web,
    "fetch_article": fetch_article
}
