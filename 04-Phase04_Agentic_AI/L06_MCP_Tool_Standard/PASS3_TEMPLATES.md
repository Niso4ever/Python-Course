# Lesson 22 — Pass 3: TEMPLATES
## Your MCP Copy-Paste Library

---

## Template 1: Connect and Discover Tools
**Use when:** You want to see what tools an MCP server offers

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def discover_mcp_tools(server_command: str, server_args: list) -> list[dict]:
    """Connect to an MCP server and return its tools in Anthropic format."""
    server_params = StdioServerParameters(command=server_command, args=server_args)

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = await session.list_tools()

            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in mcp_tools.tools
            ]
```

**Example calls:**
```python
# Discover tools from a Python server
tools = asyncio.run(discover_mcp_tools("python", ["my_server.py"]))
for t in tools:
    print(f"  {t['name']}: {t['description']}")

# Discover tools from an npm server
tools = asyncio.run(discover_mcp_tools("npx", ["-y", "@modelcontextprotocol/server-fetch"]))
print(f"Found {len(tools)} tools")  # e.g., "Found 2 tools"
```

---

## Template 2: Call a Single MCP Tool
**Use when:** You want to call a specific tool once (not in an agent loop)

```python
async def call_mcp_tool(
    server_command: str,
    server_args: list,
    tool_name: str,
    tool_args: dict
) -> str:
    """Connect to MCP server, call one tool, return result as string."""
    server_params = StdioServerParameters(command=server_command, args=server_args)

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)
            return result.content[0].text
```

**Example calls:**
```python
result = asyncio.run(call_mcp_tool(
    "python", ["knowledge_server.py"],
    "lookup", {"topic": "mcp"}
))
print(result)  # "Model Context Protocol — universal standard for AI tool connections."

result = asyncio.run(call_mcp_tool(
    "npx", ["-y", "@modelcontextprotocol/server-fetch"],
    "fetch", {"url": "https://example.com"}
))
print(result[:200])  # fetched page content
```

---

## Template 3: Agent Loop with MCP Tools (Full Bridge)
**Use when:** Running a full agent that uses MCP server tools

```python
import asyncio
import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_agent_with_mcp(
    question: str,
    server_command: str,
    server_args: list,
    system: str = "You are a helpful assistant.",
    max_iterations: int = 10
) -> str:
    """Full agent loop where tool calls go through MCP."""
    client = anthropic.Anthropic()
    server_params = StdioServerParameters(command=server_command, args=server_args)

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover and convert tools once
            mcp_tools = await session.list_tools()
            anthropic_tools = [
                {"name": t.name, "description": t.description, "input_schema": t.inputSchema}
                for t in mcp_tools.tools
            ]
            print(f"[MCP] Loaded {len(anthropic_tools)} tools: {[t['name'] for t in anthropic_tools]}")

            # Run agent loop
            messages = [{"role": "user", "content": question}]
            iterations = 0

            while iterations < max_iterations:
                iterations += 1
                response = client.messages.create(
                    model="claude-opus-5-5",
                    max_tokens=4096,
                    system=system,
                    tools=anthropic_tools,
                    messages=messages
                )

                if response.stop_reason == "end_turn":
                    return response.content[0].text

                messages.append({"role": "assistant", "content": response.content})
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        print(f"[MCP] Calling tool: {block.name}({block.input})")
                        result = await session.call_tool(block.name, block.input)
                        content = result.content[0].text if result.content else "No result"
                        print(f"[MCP] Result: {content[:80]}...")
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": content
                        })

                messages.append({"role": "user", "content": tool_results})

            return "Max iterations reached."
```

**Example call:**
```python
answer = asyncio.run(run_agent_with_mcp(
    question="What is MCP and why does it matter?",
    server_command="python",
    server_args=["knowledge_server.py"]
))
print(answer)
# [MCP] Loaded 1 tools: ["lookup"]
# [MCP] Calling tool: lookup({"topic": "mcp"})
# [MCP] Result: Model Context Protocol — universal standard...
# → Agent composes final answer using MCP result
```

---

## Template 4: Multi-Server Agent
**Use when:** Agent needs tools from multiple MCP servers simultaneously

```python
from contextlib import AsyncExitStack

async def run_agent_multi_mcp(question: str, servers: list[dict]) -> str:
    """
    Connect to multiple MCP servers, combine their tools, run agent.
    servers = [{"command": "python", "args": ["server.py"]}, ...]
    """
    client = anthropic.Anthropic()
    all_tools = []
    tool_to_session = {}     # map tool name → the right session

    async with AsyncExitStack() as stack:
        for server_config in servers:
            params = StdioServerParameters(
                command=server_config["command"],
                args=server_config["args"]
            )
            read, write = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            mcp_tools = await session.list_tools()
            for tool in mcp_tools.tools:
                all_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                })
                tool_to_session[tool.name] = session    # track which session owns each tool

        print(f"[Multi-MCP] {len(all_tools)} tools from {len(servers)} servers")

        messages = [{"role": "user", "content": question}]

        while True:
            response = client.messages.create(
                model="claude-opus-5-5", max_tokens=4096,
                tools=all_tools, messages=messages
            )
            if response.stop_reason == "end_turn":
                return response.content[0].text

            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    session = tool_to_session[block.name]   # ← right server for this tool
                    result = await session.call_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result.content[0].text
                    })

            messages.append({"role": "user", "content": tool_results})
```

**Example call:**
```python
servers = [
    {"command": "python", "args": ["knowledge_server.py"]},
    {"command": "python", "args": ["calculator_server.py"]},
]
answer = asyncio.run(run_agent_multi_mcp("Research RAG and calculate token cost for 5000 tokens.", servers))
print(answer)  # agent used knowledge + calculator tools from different servers
```

---

## Template 5: MCP Server Skeleton (for recognition)
**Use when:** Reading MCP server code — this is the standard structure

> **MCP Python SDK 2.x (checked 2026-10-28):** the `Server` + `@server.list_tools()` / `@server.call_tool()`
> decorator style below is the **mcp 1.x** API. In mcp 2.x (installed here: 2.2.0) those decorators are gone:
> the high-level server is `MCPServer` (formerly `FastMCP`) with one `@mcp.tool()` decorator per function, and the
> low-level `Server` takes `on_list_tools=` / `on_call_tool=` handler functions in its constructor. You will still
> meet the 1.x style in existing code, so keep recognising it. The client calls (`stdio_client`, `ClientSession`,
> `list_tools`, `call_tool`) keep their names, but returned objects use snake_case attributes: `tool.input_schema`,
> not `tool.inputSchema` (verified on the installed 2.2.0). Current spec revision: 2026-07-28.
> Sources: py.sdk.modelcontextprotocol.io/v2/migration/ and modelcontextprotocol.io/specification/latest

```python
# server_skeleton.py — standard MCP server structure
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-server-name")           # ← give it a name

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Declare what tools this server provides."""
    return [
        Tool(
            name="my_tool",
            description="What this tool does and when to use it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "..."}
                },
                "required": ["param1"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool calls from MCP clients."""
    if name == "my_tool":
        result = do_something(arguments["param1"])
        return [TextContent(type="text", text=str(result))]
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

**Example call (from client):**
```python
tools = asyncio.run(discover_mcp_tools("python", ["server_skeleton.py"]))
print(tools[0]["name"])  # "my_tool"

result = asyncio.run(call_mcp_tool("python", ["server_skeleton.py"], "my_tool", {"param1": "test"}))
print(result)  # whatever do_something("test") returns
```

---

## Quick Selection Guide

| Need | Template |
|:-----|:---------|
| See what tools a server has | Template 1: Discover Tools |
| Call one tool, get result | Template 2: Single Tool Call |
| Full agent using MCP server | Template 3: Agent + MCP |
| Agent using multiple servers | Template 4: Multi-Server |
| Understand MCP server structure | Template 5: Server Skeleton |
