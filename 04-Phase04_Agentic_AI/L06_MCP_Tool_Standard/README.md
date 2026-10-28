# Lesson 22: MCP — The 2026 Tool Standard
## How Tools Connect to AI Universally

> **2026 Note:** Before MCP, every AI system had its own custom tool integration. LangChain tools, CrewAI tools, OpenAI functions — all different, none compatible. MCP (Model Context Protocol) changed this: tools are now servers that any AI client can discover and call. This lesson teaches you to read and recognize MCP patterns.

## What MCP Actually Is

```
Before MCP (pre-2024):             After MCP (2026):
─────────────────────              ──────────────────
LangChain → custom tool API        Any AI client
CrewAI → custom tool API           → discovers MCP server
OpenAI → custom tool API           → lists available tools
AutoGen → custom tool API          → calls any tool
                                   → same protocol everywhere
```

**MCP = USB for AI tools.** Just as USB lets any device plug into any computer, MCP lets any tool plug into any AI agent.

## Learning Materials
1. **PASS1_RECOGNITION.md** — Learn to read MCP server/client code (START HERE)
2. **PASS_C_VISUAL.md** — See the MCP architecture as a diagram
3. **PASS3_TEMPLATES.md** — Copy-paste MCP client patterns

## Templates
4. **CHEATSHEET_L06.py** — Quick reference (KEEP OPEN while reading MCP code)
5. **template_mcp_client.py** — Runnable demo: connect to MCP server, call tools

## The One Shape to Recognize

```python
# SERVER SIDE (mcp 2.x): expose tools — one decorator per function
from mcp.server import MCPServer
mcp = MCPServer("knowledge-server")

@mcp.tool()
def search(query: str) -> str:
    """Search the knowledge base."""        # ← docstring becomes the tool description
    return lookup(query)

# SERVER SIDE (mcp 1.x, still common in existing code):
# @server.list_tools()  → returns [Tool(name=..., description=..., inputSchema=...)]
# @server.call_tool()   → if name == "search": ...

# CLIENT SIDE: discover and use
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        tools = await session.list_tools()        # ← discover
        result = await session.call_tool(name, args)  # ← call
```

**3-second recognition:** See `@mcp.tool()` or `list_tools()` + `call_tool()` + `ClientSession` → you found MCP code.

> **MCP Python SDK 2.x (checked 2026-10-28):** the `Server` + `@server.list_tools()` / `@server.call_tool()`
> decorator style below is the **mcp 1.x** API. In mcp 2.x (installed here: 2.2.0) those decorators are gone:
> the high-level server is `MCPServer` (formerly `FastMCP`) with one `@mcp.tool()` decorator per function, and the
> low-level `Server` takes `on_list_tools=` / `on_call_tool=` handler functions in its constructor. You will still
> meet the 1.x style in existing code, so keep recognising it. The client calls (`stdio_client`, `ClientSession`,
> `list_tools`, `call_tool`) keep their names, but returned objects use snake_case attributes: `tool.input_schema`,
> not `tool.inputSchema` (verified on the installed 2.2.0). Current spec revision: 2026-07-28.
> Sources: py.sdk.modelcontextprotocol.io/v2/migration/ and modelcontextprotocol.io/specification/latest


## Learning Path
**Step 1:** Read `PASS1_RECOGNITION.md` (30 min)
**Step 2:** Study `PASS_C_VISUAL.md` (15 min)
**Step 3:** Browse `PASS3_TEMPLATES.md` (10 min)
**Step 4:** Run `template_mcp_client.py` to see tool discovery in action
