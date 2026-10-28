"""
TEMPLATE: ReAct Reasoning Patterns
=====================================
3 patterns: manual loop, LangChain agent, Chain of Thought.

pip install: pip install anthropic langchain langchain-anthropic python-dotenv

Simulated demos run without API key.
Real API calls need: ANTHROPIC_API_KEY in .env
"""
import json
from dotenv import load_dotenv

load_dotenv()


# ═══════════════════════════════════════════════════════════
# SIMULATED TOOLS (replace with real implementations)
# ═══════════════════════════════════════════════════════════
def web_search(query: str) -> str:
    """Simulate web search."""
    return f"[Search results for '{query}': Result A, Result B, Result C]"

def calculator(expression: str) -> str:
    """Safe math evaluator."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

TOOL_REGISTRY = {
    "web_search": web_search,
    "calculator": calculator,
}

TOOLS = [
    {
        "name": "web_search",
        "description": (
            "Search the internet for current, real-time information. "
            "Use for: recent news, prices, current events, live data. "
            "Do NOT use for: math, things you know, local files."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Specific search query"}},
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": (
            "Evaluate mathematical expressions accurately. "
            "Always use this for arithmetic — LLMs make calculation errors. "
            "Do NOT use for: non-math questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "Python math expression, e.g. '100 * 0.15'"}},
            "required": ["expression"]
        }
    }
]

REACT_SYSTEM_PROMPT = """You are a ReAct reasoning agent.

Use this format:
Thought: [reason about what you need and which tool to use]
Action: [tool_name]
Action Input: [valid JSON with tool arguments]

After each Observation, think again and act again if needed.
When done: Final Answer: [complete answer to the user]

Available tools: web_search, calculator"""


# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Manual ReAct Loop (Anthropic Direct)
# ═══════════════════════════════════════════════════════════
def run_react_agent(question: str, model: str = "claude-sonnet-5-5",
                    max_steps: int = 6) -> str:
    """
    Manual ReAct loop using Anthropic SDK directly.

    IN:  user question (str)
    OUT: final answer (str)

    The loop:
    1. LLM reasons (Thought)
    2. LLM calls tool (Action) → stop_reason == "tool_use"
    3. We run tool (Observation)
    4. Feed result back → repeat
    5. LLM finishes → stop_reason == "end_turn" → Final Answer
    """
    import anthropic
    client   = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]

    for step in range(max_steps):
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            system=REACT_SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        print(f"\n[Step {step + 1}] stop_reason={response.stop_reason}")

        # LLM has finished reasoning — extract final answer
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    text = block.text
                    if "Final Answer:" in text:
                        return text.split("Final Answer:")[-1].strip()
                    return text
            return "No final answer found."

        # LLM wants to call a tool (Action phase)
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name  = block.name
                    tool_input = block.input
                    print(f"  → Action: {tool_name}({json.dumps(tool_input)[:60]})")

                    # Execute the tool (Observation)
                    if tool_name in TOOL_REGISTRY:
                        result = TOOL_REGISTRY[tool_name](**tool_input)
                    else:
                        result = f"Unknown tool: {tool_name}"

                    print(f"  ← Observation: {str(result)[:80]}")

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": block.id,
                        "content":     str(result)
                    })

            messages.append({"role": "user", "content": tool_results})

    return f"Reached max steps ({max_steps}) without final answer."


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: LangChain ReAct Agent
# ═══════════════════════════════════════════════════════════
def build_langchain_react_agent(verbose: bool = True, max_iterations: int = 5):
    """
    Build a LangChain ReAct agent.

    Uses hub.pull for the standard ReAct prompt.
    @tool decorator auto-converts functions to tool definitions.
    AgentExecutor handles the T/A/O loop + safety limits.

    Returns: (agent_executor, tools) tuple
    """
    # LangChain 1.x moved AgentExecutor, create_react_agent and hub to the
    # langchain-classic package (pip install langchain-classic). 0.x code wrote
    # `from langchain.agents import ...` and `from langchain import hub`.
    # New 1.x code would use `from langchain.agents import create_agent` instead.
    from langchain_classic.agents import create_react_agent, AgentExecutor
    from langchain_anthropic import ChatAnthropic
    from langchain_core.tools import tool
    from langchain_classic import hub

    # Define tools using @tool decorator (L11 pattern — docstring = description!)
    @tool
    def langchain_web_search(query: str) -> str:
        """Search the internet for current information. Use for live data, recent events."""
        return web_search(query)   # calls our simulated function above

    @tool
    def langchain_calculator(expression: str) -> str:
        """Evaluate math expressions. Always use for arithmetic — don't guess."""
        return calculator(expression)

    tools = [langchain_web_search, langchain_calculator]
    llm   = ChatAnthropic(model="claude-sonnet-5-5")

    # Standard ReAct prompt from LangChain Hub
    prompt = hub.pull("hwchase17/react")

    # Build ReAct agent
    agent    = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,              # ← print every T/A/O step
        max_iterations=max_iterations,    # ← safety limit
        handle_parsing_errors=True,   # ← recover from malformed LLM output
        return_intermediate_steps=True  # ← include T/A/O in result
    )

    return executor, tools


def run_langchain_react(question: str) -> dict:
    """
    Run a LangChain ReAct agent on a question.

    Returns dict with:
    - "output": final answer
    - "intermediate_steps": list of (action, observation) tuples
    """
    executor, tools = build_langchain_react_agent()
    result = executor.invoke({"input": question})

    print(f"\nFinal Answer: {result['output']}")

    print("\nFull Trace:")
    for i, (action, observation) in enumerate(result.get("intermediate_steps", [])):
        print(f"  Step {i+1}:")
        print(f"    Action: {action.tool}({str(action.tool_input)[:60]})")
        print(f"    Observation: {str(observation)[:80]}")

    return result


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: Chain of Thought (No Tools)
# ═══════════════════════════════════════════════════════════
def chain_of_thought(question: str, model: str = "claude-sonnet-5-5") -> str:
    """
    Chain of Thought: LLM reasons step-by-step without external tools.
    Use for: math, logic, multi-step reasoning with known facts.
    Do NOT use for: current data, files, real-time information.
    """
    import anthropic
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=model,
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"{question}\n\nLet's think step by step."   # ← CoT trigger
        }]
    )
    return response.content[0].text


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("ReAct Pattern Templates — Demo")
    print("=" * 60)
    print()

    print("TEMPLATE 1: Manual ReAct Loop")
    print("  run_react_agent('What is 15% of 8432 and what is Bitcoin?')")
    print("  → T: need calculator + web_search")
    print("  → A: calculator(8432 * 0.15) → 1264.8")
    print("  → A: web_search('Bitcoin current price') → [results]")
    print("  → Final Answer: combined response")
    print()

    print("TEMPLATE 2: LangChain ReAct Agent")
    print("  executor, tools = build_langchain_react_agent(verbose=True)")
    print("  result = executor.invoke({'input': 'Calculate 45 * 78'})")
    print("  # verbose=True prints every Thought/Action/Observation")
    print()

    print("TEMPLATE 3: Chain of Thought")
    print("  chain_of_thought('A train travels 60mph for 2.5 hours. Distance?')")
    print("  → Step 1: Speed = 60 mph")
    print("  → Step 2: Time = 2.5 hours")
    print("  → Step 3: Distance = 60 × 2.5 = 150 miles")
    print()

    # Simulated demo (no API needed):
    print("--- Simulated Tool Execution ---")
    print(f"web_search('AI news 2025'): {web_search('AI news 2025')[:70]}")
    print(f"calculator('8432 * 0.15'): {calculator('8432 * 0.15')}")
    print(f"calculator('(15 + 27) * 4'): {calculator('(15 + 27) * 4')}")

    print()
    print("To run with real API: set ANTHROPIC_API_KEY in .env")
    print("Then call: run_react_agent('your question here')")
