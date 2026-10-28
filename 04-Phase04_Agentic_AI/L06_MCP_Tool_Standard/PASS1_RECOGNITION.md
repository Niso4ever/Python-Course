# Lesson 22 — Pass 1: RECOGNITION
## Learn to SEE MCP Patterns

**Goal:** Recognize the MCP server, client, and tool discovery/call patterns — so you can read and use any MCP integration without memorizing the full protocol.

> **2026 Note:** MCP is now built into Claude.ai, the Anthropic API, and most major AI clients. Understanding MCP means understanding the future of tool integration. You don't need to BUILD MCP servers in this lesson — just RECOGNIZE them.


> **MCP Python SDK 2.x (checked 2026-10-28):** the `Server` + `@server.list_tools()` / `@server.call_tool()`
> decorator style below is the **mcp 1.x** API. In mcp 2.x (installed here: 2.2.0) those decorators are gone:
> the high-level server is `MCPServer` (formerly `FastMCP`) with one `@mcp.tool()` decorator per function, and the
> low-level `Server` takes `on_list_tools=` / `on_call_tool=` handler functions in its constructor. You will still
> meet the 1.x style in existing code, so keep recognising it. The client calls (`stdio_client`, `ClientSession`,
> `list_tools`, `call_tool`) keep their names, but returned objects use snake_case attributes: `tool.input_schema`,
> not `tool.inputSchema` (verified on the installed 2.2.0). Current spec revision: 2026-07-28.
> Sources: py.sdk.modelcontextprotocol.io/v2/migration/ and modelcontextprotocol.io/specification/latest

---

## The Four MCP Shapes

### Shape 1: MCP Server (tool definition side)
```python
from mcp.server import Server
from mcp.types import Tool

server = Server("my-tool-server")

@server.list_tools()
async def list_tools():
    return [Tool(name="tool_name", description="...", inputSchema={...})]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "tool_name":
        return [TextContent(type="text", text=str(my_function(**arguments)))]
```
**Recognize:** `Server(...)` + `@server.list_tools()` + `@server.call_tool()`.

---

### Shape 2: MCP Client (tool consumer side)
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="python", args=["my_server.py"])

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()           # ← discover
        result = await session.call_tool(name, args) # ← call
```
**Recognize:** `StdioServerParameters` + `ClientSession` + `list_tools()` + `call_tool()`.

---

### Shape 3: Converting MCP Tools to Anthropic Tool Schemas
```python
# MCP tools → Anthropic format (bridge)
def mcp_to_anthropic_tools(mcp_tools) -> list:
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        }
        for tool in mcp_tools
    ]
```
**Recognize:** A conversion function that maps `tool.name`, `tool.description`, `tool.inputSchema`.

---

### Shape 4: Calling MCP Tools from an Agent Loop
```python
# In the tool dispatch:
if block.type == "tool_use":
    result = await session.call_tool(block.name, block.input)  # ← MCP call
    tool_results.append({"type": "tool_result", "tool_use_id": block.id,
                         "content": result.content[0].text})
```
**Recognize:** `session.call_tool(block.name, block.input)` inside a tool dispatcher.

---

## Real Examples to RECOGNIZE (Don't Write, Just Read)

### Example 1: A Simple MCP Server

```python
# server.py — runs as a separate process, exposes tools
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("knowledge-server")

KNOWLEDGE = {
    "rag": "Retrieval-Augmented Generation combines retrieval with LLM generation.",
    "mcp": "Model Context Protocol — universal standard for AI tool connections.",
}

@server.list_tools()
async def list_tools():
    """Tell clients what tools are available."""
    return [
        Tool(
            name="lookup",
            description="Look up a topic in the knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic to look up"}
                },
                "required": ["topic"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool call from any MCP client."""
    if name == "lookup":
        topic = arguments.get("topic", "").lower()
        result = KNOWLEDGE.get(topic, f"No entry for: {topic}")
        return [TextContent(type="text", text=result)]
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

**RECOGNIZE THIS:**
- `Server("knowledge-server")` ← server has a name
- `@server.list_tools()` ← decorator: runs when client asks "what tools do you have?"
- `@server.call_tool()` ← decorator: runs when client asks to call a tool
- `Tool(name=..., description=..., inputSchema=...)` ← same structure as Anthropic tool schema
- `TextContent(type="text", text=...)` ← how results are returned

**What it does:** "A running process that exposes a `lookup` tool via MCP. Any AI client can discover and call it."

---

### Example 2: MCP Client — Discover and List Tools

```python
# client_discover.py — what YOU write to connect to an MCP server
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def discover_tools():
    """Connect to MCP server and list available tools."""
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]                    # ← starts the server process
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()        # ← handshake with server

            tools = await session.list_tools()   # ← ask: what tools do you have?

            print(f"Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
                print(f"    Schema: {tool.inputSchema}")

asyncio.run(discover_tools())

# Output:
# Found 1 tools:
#   - lookup: Look up a topic in the knowledge base.
#     Schema: {"type": "object", "properties": {"topic": {...}}, "required": ["topic"]}
```

**RECOGNIZE THIS:**
- `StdioServerParameters(command="python", args=["server.py"])` ← how to start the server
- `stdio_client(server_params)` ← establishes the connection pipe
- `session.initialize()` ← required handshake before any calls
- `session.list_tools()` ← discovery call — returns list of Tool objects
- `.tools` ← the list is inside `.tools` attribute

**What it does:** "Connect to a running MCP server and print all available tools."

---

### Example 3: MCP Client — Call a Tool

```python
async def call_mcp_tool():
    server_params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call a specific tool with arguments
            result = await session.call_tool(
                "lookup",                          # ← tool name
                {"topic": "mcp"}                   # ← arguments dict
            )

            # Result comes back as a list of content blocks
            for block in result.content:
                print(block.text)

asyncio.run(call_mcp_tool())
# Output:
# Model Context Protocol — universal standard for AI tool connections.
```

**RECOGNIZE THIS:**
- `session.call_tool(name, args)` ← call by name with dict of args
- `result.content` ← list of content blocks (same pattern as Anthropic API)
- `block.text` ← the actual result text

**What it does:** "Connect to server, call the 'lookup' tool with 'mcp' as the topic, print result."

---

### Example 4: Bridge — MCP Tools Inside an Agent Loop

```python
# The full bridge: MCP server → Anthropic agent loop
async def agent_with_mcp_tools(question: str) -> str:
    import anthropic
    client = anthropic.Anthropic()

    server_params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 1: Discover MCP tools
            mcp_tools = await session.list_tools()

            # Step 2: Convert to Anthropic format
            anthropic_tools = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema
                }
                for t in mcp_tools.tools
            ]

            # Step 3: Run agent loop with MCP tools registered
            messages = [{"role": "user", "content": question}]

            while True:
                response = client.messages.create(
                    model="claude-opus-5-5", max_tokens=1024,
                    tools=anthropic_tools,
                    messages=messages
                )

                if response.stop_reason == "end_turn":
                    return response.content[0].text

                messages.append({"role": "assistant", "content": response.content})
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        # Step 4: Execute via MCP (not direct Python call!)
                        result = await session.call_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result.content[0].text
                        })

                messages.append({"role": "user", "content": tool_results})

# Example call:
answer = asyncio.run(agent_with_mcp_tools("What is MCP?"))
print(answer)
# → Agent used MCP lookup tool → got explanation → returned answer
```

**RECOGNIZE THIS:**
- Steps 1-2: discovery + conversion ← happens once at startup
- Step 3: same agent loop (L02) ← not changed
- Step 4: `session.call_tool(block.name, block.input)` ← MCP dispatch instead of Python function

**What it does:** "Normal agent loop — but tool dispatch goes through MCP instead of local functions."

---

### Example 5: Multiple MCP Servers (2026 Style)

```python
# Connect to multiple MCP servers and combine their tools
async def agent_with_multiple_mcp_servers(question: str) -> str:
    servers = [
        StdioServerParameters(command="python", args=["search_server.py"]),
        StdioServerParameters(command="python", args=["database_server.py"]),
        StdioServerParameters(command="node",   args=["browser_server.js"]),   # JS server
    ]

    all_tools = []
    all_sessions = {}

    # Connect to each server and collect tools
    for server_params in servers:
        async with stdio_client(server_params) as (r, w):
            async with ClientSession(r, w) as session:
                await session.initialize()
                mcp_tools = await session.list_tools()
                for tool in mcp_tools.tools:
                    all_tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    })
                    all_sessions[tool.name] = session   # map tool → session
    # Now run agent with all tools combined...
```

**RECOGNIZE THIS:**
- Multiple `StdioServerParameters` ← multiple servers
- One server can be Python (`command="python"`), another JavaScript (`command="node"`)
- Tools from all servers combined into one `all_tools` list
- `all_sessions[tool.name]` ← maps each tool back to the right server

**What it does:** "Aggregate tools from many servers. Agent sees them all as one toolkit."

---

### Example 6: MCP in Claude.ai (Built-In)

```python
# In Claude.ai, MCP servers are configured via settings.
# Claude connects to them automatically.
# When you ask Claude "search the web" — if a web search MCP server is connected,
# Claude discovers that tool automatically and calls it.

# What you CONFIGURE (once, in settings):
mcp_config = {
    "mcpServers": {
        "web-search": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-brave-search"],
            "env": {"BRAVE_API_KEY": "your_key"}
        },
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"]
        }
    }
}

# What happens automatically when Claude runs:
# 1. Claude starts the MCP server processes
# 2. Discovers tools via session.list_tools()
# 3. Converts to internal tool format
# 4. Agent loop uses session.call_tool() for dispatch
# This is the SAME code you've been reading — just automated.
```

**RECOGNIZE THIS:**
- `"mcpServers"` ← JSON config key for MCP servers
- `"command"` + `"args"` ← how to start the server (matches `StdioServerParameters`)
- Tools are `npx` packages ← MCP servers distributed as npm packages
- Claude does steps 1-4 for you behind the scenes

**What it does:** "Claude.ai runs the same MCP code internally. Config = the same server parameters you've been reading."

---

### Example 7: Reading MCP from the agents/ Folder

```python
# From agents/6_mcp/1_lab1.ipynb — the OpenAI Agents SDK + MCP pattern:
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    # MCP server via OpenAI Agents SDK
    async with MCPServerStdio(
        params={"command": "npx", "args": ["-y", "@modelcontextprotocol/server-fetch"]}
    ) as mcp_server:

        # Discover and register tools automatically
        agent = Agent(
            name="Research Agent",
            instructions="You are a helpful research assistant.",
            mcp_servers=[mcp_server]    # ← pass MCP server to agent
        )

        result = await Runner.run(agent, "Fetch the latest AI news.")
        print(result.final_output)

# DIRECT API EQUIVALENT:
# async with stdio_client(StdioServerParameters(command="npx", args=[...])) as (r,w):
#     async with ClientSession(r, w) as session:
#         await session.initialize()
#         tools = mcp_to_anthropic_tools(await session.list_tools())
#         # run_agent(question, tools=tools, session=session)
```

**RECOGNIZE THIS:**
- `MCPServerStdio(params={"command": ...})` ← same as `StdioServerParameters`
- `mcp_servers=[mcp_server]` ← OpenAI SDK takes the server object
- `Runner.run(agent, input)` ← the agent loop, with MCP dispatch inside

**What it does:** "OpenAI Agents SDK wraps MCP connection + agent loop. Direct API is the unwrapped version."

---

### Example 8: Building a Simple MCP-Compatible Tool (Recognition Only)

```python
# You don't need to BUILD this — just recognize the structure.
# MCP servers can be in Python OR JavaScript.

# Python MCP server structure:
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-service")

@server.list_tools()           # ← required: what tools does this server offer?
async def list_tools():
    return [Tool(...), Tool(...)]   # ← list of Tool objects

@server.call_tool()            # ← required: execute a tool when called
async def call_tool(name, args):
    ...
    return [TextContent(type="text", text=result)]

# JavaScript MCP server structure (recognition):
# server.setRequestHandler(ListToolsRequestSchema, async () => ({tools: [...]}))
# server.setRequestHandler(CallToolRequestSchema, async (request) => {...})
```

**RECOGNIZE THIS:**
- Two required handlers: `list_tools` + `call_tool` ← the MCP contract
- Python uses `@server.list_tools()` decorator
- JavaScript uses `server.setRequestHandler(ListToolsRequestSchema, ...)`
- **Same contract, different language** — MCP is language-agnostic

**What it does:** "MCP server = any code that implements list_tools + call_tool. Language doesn't matter."

---

## MCP Anatomy Reference

| Part | What it looks like | Role |
|:-----|:------------------|:-----|
| Server | `Server("name")` | The tool provider process |
| List tools | `@server.list_tools()` | "Here's what I offer" |
| Call tool | `@server.call_tool()` | "Execute this tool call" |
| Server params | `StdioServerParameters(command, args)` | How to start the server |
| Client session | `ClientSession(read, write)` | Connection to the server |
| Discover | `await session.list_tools()` | "What tools are available?" |
| Call | `await session.call_tool(name, args)` | "Run this tool" |
| Bridge | `mcp_to_anthropic_tools(mcp_tools)` | Convert for Anthropic API |

---

## You've Completed Pass 1!

You can now:
✓ **Read** MCP server code (server + list_tools + call_tool)
✓ **Recognize** MCP client code (StdioServerParameters + ClientSession)
✓ **Spot** the bridge pattern (MCP tools → Anthropic format)
✓ **See** MCP dispatch inside an agent loop
✓ **Understand** why MCP matters (language-agnostic, universal)
✓ **Read** OpenAI Agents SDK MCP usage as the same pattern

**Next:**
- **Pass C (Visual):** See the MCP architecture as a diagram
- **Pass 3 (Templates):** Copy MCP client connection patterns
