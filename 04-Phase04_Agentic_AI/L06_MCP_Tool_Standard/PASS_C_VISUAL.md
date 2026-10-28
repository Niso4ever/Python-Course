# Lesson 22 — Pass C: VISUAL PATTERNS
## See the MCP Architecture as a Diagram

---

## Visual 1: What MCP Replaces

```
BEFORE MCP (pre-2024):                AFTER MCP (2026):
────────────────────────              ──────────────────────────
LangChain agent                       Any AI agent
    │                                     │
    ├── LangChain tool A                  └── MCP client
    ├── LangChain tool B                         │
    └── (can't use CrewAI tools)           ┌────┴────┬────────┐
                                           │         │        │
CrewAI agent                          MCP server  MCP server  MCP server
    │                                 (Python)    (Node.js)   (Rust)
    ├── CrewAI tool A                  search      browser     database
    └── (can't use LangChain tools)    tool        tool        tool

OpenAI agent                          ANY client can use ANY server.
    └── OpenAI-format tools only       Same protocol everywhere.
```

**Pattern:** MCP = USB. Plug any tool into any agent.

---

## Visual 2: MCP Architecture — Server ↔ Client

```
                    STDIO PIPE
    ┌─────────────┐     ←→     ┌──────────────────────┐
    │  MCP SERVER │            │     MCP CLIENT        │
    │  (tool.py)  │            │ (your agent code)     │
    │             │            │                       │
    │ list_tools  │◄──────────┤ session.list_tools()  │
    │     → Tool  │──────────►│   → [Tool, Tool, ...]  │
    │             │            │                       │
    │ call_tool   │◄──────────┤ session.call_tool()   │
    │   → result  │──────────►│   → result.content    │
    └─────────────┘            └──────────────────────┘

Two messages between them:
  1. list_tools request → Tool schema list (discovery)
  2. call_tool request  → Tool result (execution)
```

**Example call sequence:**
```python
# Client side:
tools = await session.list_tools()       # → discovers: ["lookup", "search", "calculate"]
result = await session.call_tool("lookup", {"topic": "mcp"})  # → "Model Context Protocol..."
```

---

## Visual 3: The Discovery → Bridge → Agent Loop Flow

```
STEP 1: Start server + connect
  StdioServerParameters(command="python", args=["server.py"])
          │
          ▼
  stdio_client(params) → (read, write) pipe
          │
          ▼
  ClientSession(read, write)
          │
          ▼
  session.initialize()    ← handshake

STEP 2: Discover tools
  session.list_tools()    ← "what can you do?"
          │
          ▼
  [Tool(name="lookup", description="...", inputSchema={...}), ...]

STEP 3: Convert to Anthropic format
  [{"name": "lookup", "description": "...", "input_schema": {...}}, ...]

STEP 4: Register in agent loop
  client.messages.create(tools=anthropic_format_tools, messages=messages)
          │
          ▼
  block.type == "tool_use"  (LLM called a tool)

STEP 5: Dispatch via MCP (not local function)
  result = await session.call_tool(block.name, block.input)
          │
          ▼
  tool_results.append({..., "content": result.content[0].text})
```

**Pattern:** Discover once → loop calls MCP for every tool execution.

---

## Visual 4: Multiple Servers

```
Your Agent
     │
     │ anthropic_tools = []  ← collecting from all servers
     │
  ┌──┼──────────────────────┐
  │  │         │            │
  ▼  ▼         ▼            ▼
server_1    server_2     server_3
(Python)    (Node.js)    (Rust)
  search      browser    database
  tool        tool       query_tool
  summarize   screenshot calculate
     │           │            │
     └──────┬────┘────────────┘
            ▼
   anthropic_tools = [
     {"name": "search", ...},
     {"name": "summarize", ...},
     {"name": "browser", ...},
     {"name": "screenshot", ...},
     {"name": "database", ...},
     {"name": "calculate", ...},
   ]
```

**Example call:**
```python
# Agent loop sees 6 tools, from 3 different servers (Python/Node/Rust)
# When "search" is called → dispatched to server_1 session
# When "browser" is called → dispatched to server_2 session
# Unified experience — agent doesn't care which server each tool lives on
```

---

## Visual 5: MCP vs Direct Tool (Side by Side)

```
DIRECT TOOL DISPATCH:                  MCP TOOL DISPATCH:
──────────────────────                 ──────────────────
for block in response.content:         for block in response.content:
    if block.type == "tool_use":           if block.type == "tool_use":
        fn = TOOL_MAP[block.name]              result = await session.call_tool(
        result = fn(**block.input)                 block.name, block.input
                                               )
        tool_results.append({                  tool_results.append({
            "type": "tool_result",                 "type": "tool_result",
            "tool_use_id": block.id,               "tool_use_id": block.id,
            "content": str(result)                 "content": result.content[0].text
        })                                     })

Calls local Python function             Calls remote server via protocol
Works only in this codebase             Works with any MCP server anywhere
You write the functions                 You connect to existing servers
```

**Pattern:** Same agent loop. Same tool schema. Different dispatch: local function vs. MCP session.

---

## Visual 6: MCP Ecosystem Map (2026)

```
MCP SERVERS AVAILABLE (npm/pip packages):
┌─────────────────────────────────────────────────┐
│ Web & Search:                                    │
│   @modelcontextprotocol/server-brave-search      │
│   @modelcontextprotocol/server-fetch             │
│                                                  │
│ Files & System:                                  │
│   @modelcontextprotocol/server-filesystem        │
│   @modelcontextprotocol/server-git               │
│                                                  │
│ Data & APIs:                                     │
│   @modelcontextprotocol/server-postgres          │
│   @modelcontextprotocol/server-sqlite            │
│   @modelcontextprotocol/server-github            │
│                                                  │
│ AI Services:                                     │
│   @modelcontextprotocol/server-everything        │
│   (community: hundreds more at mcp.so)           │
└─────────────────────────────────────────────────┘

COMPATIBLE MCP CLIENTS:
  Claude.ai (Anthropic)    → built-in MCP support
  Claude API               → via your code (this lesson)
  OpenAI Agents SDK        → MCPServerStdio class
  Any custom agent         → ClientSession + stdio_client
```

---

## Visual 7: Why MCP Matters for You

```
OLD WAY (2024):
  To use a new tool:
  1. Find the LangChain wrapper for it
  2. Install the LangChain integration package
  3. Learn the LangChain tool API
  4. Hope it's compatible with your framework version
  Time: hours to days

NEW WAY (2026 with MCP):
  To use a new tool:
  1. npx -y @modelcontextprotocol/server-newservice
  2. Connect: StdioServerParameters(command="npx", args=[...])
  3. session.list_tools() → auto-discover everything
  4. session.call_tool(name, args) → use immediately
  Time: minutes
```

---

## You've Completed Pass C!

You can now:
✓ **See** MCP as a protocol, not a framework
✓ **Visualize** the discovery → bridge → agent loop flow
✓ **Understand** why multiple server connections work
✓ **Compare** direct dispatch vs MCP dispatch (same loop!)
✓ **Map** the MCP ecosystem (servers available, clients compatible)
✓ **See** why MCP makes tool integration framework-independent

**Next:** Pass 3 — Copy MCP client connection and bridge patterns.
