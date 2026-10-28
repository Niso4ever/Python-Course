"""
CHEATSHEET L06 — MCP (Model Context Protocol)
===============================================
Keep this open while reading MCP code.

SECTION 1: MCP SERVER SHAPES
SECTION 2: MCP CLIENT SHAPES
SECTION 3: BRIDGE (MCP → Anthropic format)
SECTION 4: DISPATCH IN AGENT LOOP
SECTION 5: 3-SECOND RECOGNITION
"""

# ============================================================
# SECTION 1: MCP SERVER SHAPES
# ============================================================

# Server = a running process that exposes tools
# mcp 2.x (current; installed 2.2.0, checked 2026-10-28):
from mcp.server import MCPServer          # was FastMCP in mcp 1.x

mcp = MCPServer("server-name")

@mcp.tool()                    # ← one decorator per tool; listing + calling handled for you
def search(query: str) -> str:
    """Search the knowledge base."""   # ← becomes the tool description
    return "..."

# mcp.run(transport="stdio")   # or "streamable-http"

# mcp 1.x style (removed in 2.x, still common in existing code):
# server = Server("server-name")
# @server.list_tools()  async def list_tools(): return [Tool(name=..., description=..., inputSchema=...)]
# @server.call_tool()   async def call_tool(name, args): return [TextContent(type="text", text=...)]

# ============================================================
# SECTION 2: MCP CLIENT SHAPES
# ============================================================

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# How to start the server:
server_params = StdioServerParameters(
    command="python",          # or "npx", "node"
    args=["server.py"]         # or ["-y", "@mcp/server-name"]
)

# Connect pattern (always async context managers):
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()               # ← required handshake

        tools = await session.list_tools()       # ← discover
        # tools.tools = list of Tool objects

        result = await session.call_tool(        # ← execute
            "tool_name",
            {"param": "value"}
        )
        # result.content[0].text = the result string

# ============================================================
# SECTION 3: BRIDGE (MCP → Anthropic format)
# ============================================================

# MCP Tool → Anthropic tool schema
anthropic_tools = [
    {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.input_schema     # ← (mcp 1.x: tool.inputSchema) same structure as Anthropic's input_schema!
    }
    for tool in mcp_tools.tools
]

# ============================================================
# SECTION 4: DISPATCH IN AGENT LOOP
# ============================================================

# DIRECT dispatch (L03):
#   fn = TOOL_MAP[block.name]
#   result = fn(**block.input)
#   "content": str(result)

# MCP dispatch (L06):
#   result = await session.call_tool(block.name, block.input)
#   "content": result.content[0].text

# Same agent loop (L02). Only the dispatch line changes.

# ============================================================
# SECTION 5: 3-SECOND RECOGNITION
# ============================================================

# Spot MCP code by looking for:
#
# SERVER:  @mcp.tool() (mcp 2.x)  or  @server.list_tools() + @server.call_tool() (mcp 1.x)
# CLIENT:  StdioServerParameters + ClientSession + session.list_tools()
# BRIDGE:  tool.input_schema (1.x: inputSchema) → "input_schema"
# LOOP:    session.call_tool(block.name, block.input)
#
# See any 2 of these → you found MCP code.
"""
MINIMAL MCP CLIENT EXAMPLE:

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_mcp():
    params = StdioServerParameters(command="python", args=["server.py"])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = await session.list_tools()        # discover
            result = await session.call_tool("tool_name", {"param": "value"})  # call
            return result.content[0].text

print(asyncio.run(use_mcp()))
"""
