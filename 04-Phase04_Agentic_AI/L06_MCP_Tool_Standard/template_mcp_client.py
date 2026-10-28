"""
Template: MCP Client — Runnable Demo
======================================
Run this file as-is: python template_mcp_client.py

DEMO MODE (default): Simulates MCP server interaction locally. No real server needed.
REAL MODE:           Set DEMO_MODE = False. Requires an MCP server running.

What this demonstrates:
  - MCP server structure (for recognition)
  - MCP client: discover tools
  - MCP client: call a tool
  - Bridge: MCP tools → Anthropic format
  - Agent loop using MCP for tool dispatch

To run with a REAL MCP server:
  pip install mcp anthropic
  python template_mcp_client.py  (after setting DEMO_MODE = False and ANTHROPIC_API_KEY)
"""

import asyncio
import json

DEMO_MODE = True  # Set to False for real MCP connection

# ============================================================
# DEMO: Simulated MCP objects (no real MCP import needed)
# ============================================================

class MockTool:
    """Simulates an MCP Tool object."""
    def __init__(self, name, description, input_schema):
        self.name = name
        self.description = description
        self.input_schema = input_schema      # mcp 2.x attribute name (1.x: inputSchema)

class MockTextContent:
    def __init__(self, text):
        self.type = "text"
        self.text = text

class MockToolResult:
    def __init__(self, text):
        self.content = [MockTextContent(text)]

class MockMCPSession:
    """Simulates an MCP ClientSession."""

    DEMO_TOOLS = [
        MockTool(
            name="search_knowledge",
            description="Search the AI knowledge base for information on any topic.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Topic to search"}
                },
                "required": ["query"]
            }
        ),
        MockTool(
            name="get_definition",
            description="Get a precise definition of an AI term.",
            input_schema={
                "type": "object",
                "properties": {
                    "term": {"type": "string", "description": "AI term to define"},
                    "brief": {"type": "boolean", "description": "Return brief version", "default": False}
                },
                "required": ["term"]
            }
        ),
        MockTool(
            name="compare_concepts",
            description="Compare two AI concepts side by side.",
            input_schema={
                "type": "object",
                "properties": {
                    "concept_a": {"type": "string"},
                    "concept_b": {"type": "string"}
                },
                "required": ["concept_a", "concept_b"]
            }
        )
    ]

    KNOWLEDGE = {
        "mcp":            "Model Context Protocol — the universal open standard for connecting AI models to tools.",
        "agent loop":     "The fundamental pattern: LLM decides → tool executes → observe results → repeat.",
        "structured output": "Making LLMs return typed data via Pydantic + client.messages.parse(output_format=...).",
        "rag":            "Retrieval-Augmented Generation: combine document retrieval with LLM generation.",
        "tool use":       "Registering tool schemas with the LLM API so the model can call functions.",
    }

    DEFINITIONS = {
        "mcp":       "Model Context Protocol: An open standard (2024) enabling any AI client to connect to any tool server using a unified protocol.",
        "agent":     "An LLM system that runs in a loop, calling tools to gather information or take actions until a goal is achieved.",
        "tool":      "A function registered with the LLM as a callable schema — the model decides when and how to invoke it.",
        "orchestrator": "An agent or function that classifies requests and routes them to appropriate specialist agents.",
    }

    class MockToolList:
        def __init__(self, tools):
            self.tools = tools

    async def initialize(self):
        pass   # handshake simulation

    async def list_tools(self):
        print("[MCP Server] → list_tools() called")
        return self.MockToolList(self.DEMO_TOOLS)

    async def call_tool(self, name: str, arguments: dict) -> MockToolResult:
        print(f"[MCP Server] → call_tool('{name}', {arguments})")

        if name == "search_knowledge":
            query = arguments.get("query", "").lower()
            for key, val in self.KNOWLEDGE.items():
                if key in query or any(w in query for w in key.split()):
                    return MockToolResult(val)
            return MockToolResult(f"No entry found for '{query}'. Available: {list(self.KNOWLEDGE.keys())}")

        elif name == "get_definition":
            term = arguments.get("term", "").lower()
            brief = arguments.get("brief", False)
            definition = self.DEFINITIONS.get(term, f"No definition found for '{term}'.")
            if brief:
                definition = definition[:80] + "..."
            return MockToolResult(definition)

        elif name == "compare_concepts":
            a = arguments.get("concept_a", "A")
            b = arguments.get("concept_b", "B")
            return MockToolResult(
                f"Comparison: {a} vs {b}\n"
                f"• {a}: {self.KNOWLEDGE.get(a.lower(), 'concept in AI')}\n"
                f"• {b}: {self.KNOWLEDGE.get(b.lower(), 'concept in AI')}"
            )

        return MockToolResult(f"Unknown tool: {name}")

# ============================================================
# DEMO 1: Discover Tools
# ============================================================

async def demo_discover():
    print("\n" + "="*60)
    print("DEMO 1: Discover MCP Tools")
    print("="*60)

    if DEMO_MODE:
        session = MockMCPSession()
        await session.initialize()
    else:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        params = StdioServerParameters(command="python", args=["knowledge_server.py"])
        # (would use async with in real code)

    tool_list = await session.list_tools()

    print(f"\nFound {len(tool_list.tools)} tools from MCP server:\n")
    for tool in tool_list.tools:
        print(f"  Tool: {tool.name}")
        print(f"  Desc: {tool.description}")
        required = tool.input_schema.get("required", [])
        print(f"  Required params: {required}\n")

    # Convert to Anthropic format
    anthropic_tools = [
        {"name": t.name, "description": t.description, "input_schema": t.input_schema}
        for t in tool_list.tools
    ]
    print(f"Converted to Anthropic format: {len(anthropic_tools)} tools ready for agent.")
    return session, anthropic_tools

# ============================================================
# DEMO 2: Call MCP Tools Directly
# ============================================================

async def demo_call_tools(session):
    print("\n" + "="*60)
    print("DEMO 2: Call MCP Tools Directly")
    print("="*60)

    calls = [
        ("search_knowledge", {"query": "agent loop"}),
        ("get_definition",   {"term": "mcp", "brief": False}),
        ("compare_concepts", {"concept_a": "mcp", "concept_b": "rag"}),
    ]

    for tool_name, args in calls:
        print(f"\nCalling: {tool_name}({args})")
        result = await session.call_tool(tool_name, args)
        print(f"Result:  {result.content[0].text[:120]}...")

# ============================================================
# DEMO 3: Agent Loop Using MCP Dispatch
# ============================================================

class MockBlock:
    def __init__(self, btype, **kwargs):
        self.type = btype
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockLLMResponse:
    def __init__(self, stop_reason, content):
        self.stop_reason = stop_reason
        self.content = content

_agent_step = [0]

def simulate_agent_decision(messages, step):
    """Simulate LLM decisions for demo agent loop."""
    if step == 1:
        return MockLLMResponse("tool_use", [
            MockBlock("text", text="Let me look up the agent loop pattern."),
            MockBlock("tool_use", id="tu_01", name="search_knowledge", input={"query": "agent loop"})
        ])
    elif step == 2:
        return MockLLMResponse("tool_use", [
            MockBlock("text", text="Now let me get the definition of MCP."),
            MockBlock("tool_use", id="tu_02", name="get_definition", input={"term": "mcp"})
        ])
    else:
        return MockLLMResponse("end_turn", [
            MockBlock("text", text="Based on my research:\n\n• Agent Loop: The fundamental AI pattern — LLM decides → tool executes → observe → repeat.\n• MCP: Model Context Protocol — the universal open standard for connecting AI models to tools.\n\nThese two concepts work together: the agent loop runs tools, and MCP is how tools are connected universally in 2026.")
        ])

async def demo_agent_loop(session, anthropic_tools):
    print("\n" + "="*60)
    print("DEMO 3: Agent Loop Using MCP for Tool Dispatch")
    print("="*60)

    question = "Explain the agent loop and MCP — how do they work together?"
    print(f"Question: {question}\n")

    messages = [{"role": "user", "content": question}]
    iteration = 0

    while True:
        iteration += 1
        _agent_step[0] = iteration
        print(f"[Iteration {iteration}] THINK → LLM deciding...")

        # Simulate LLM response (or use real API)
        if DEMO_MODE:
            response = simulate_agent_decision(messages, iteration)
        else:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-opus-5-5", max_tokens=2048,
                tools=anthropic_tools, messages=messages
            )

        print(f"[Iteration {iteration}] stop_reason = '{response.stop_reason}'")

        if response.stop_reason == "end_turn":
            final = response.content[0].text
            print(f"\n[Done in {iteration} iteration(s)]")
            print("\nFINAL ANSWER:")
            print("-"*40)
            print(final)
            return final

        # ACT: dispatch through MCP
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if hasattr(block, "type") and block.type == "tool_use":
                print(f"  ACT → MCP dispatch: {block.name}({block.input})")
                # ← This is the key: calling MCP session, not a local function
                result = await session.call_tool(block.name, block.input)
                content = result.content[0].text
                print(f"  OBSERVE ← {content[:80]}...")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": content
                })

        messages.append({"role": "user", "content": tool_results})

# ============================================================
# RUN ALL DEMOS
# ============================================================

async def main():
    session, anthropic_tools = await demo_discover()
    await demo_call_tools(session)
    await demo_agent_loop(session, anthropic_tools)

    if DEMO_MODE:
        print("\n" + "="*60)
        print("[DEMO MODE] Set DEMO_MODE = False + install 'mcp' package for real MCP.")
        print("  pip install mcp anthropic")

if __name__ == "__main__":
    asyncio.run(main())
