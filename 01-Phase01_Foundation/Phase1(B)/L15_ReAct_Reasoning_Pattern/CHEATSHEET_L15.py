"""
═══════════════════════════════════════════════════════════════════
LESSON 13 CHEATSHEET: ReAct Reasoning Pattern
═══════════════════════════════════════════════════════════════════
Thought → Action → Observation → repeat until Final Answer.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. REACT LOOP (3 PHASES)
# ═══════════════════════════════════════════════════════════
"""
PHASE 1: THOUGHT
  LLM reasons: what do I know? what do I need? which tool?

PHASE 2: ACTION
  LLM calls a tool (stop_reason == "tool_use")
  Your code executes the tool
  Result becomes OBSERVATION

PHASE 3: OBSERVE
  Tool result fed back to LLM
  LLM reasons again (THOUGHT)
  Loop continues until FINAL ANSWER
"""

# ═══════════════════════════════════════════════════════════
# 2. PATTERN RECOGNITION GUIDE
# ═══════════════════════════════════════════════════════════
"""
You see                              You understand
──────────────────────────────────   ──────────────────────────────────────
"Thought:" / "Action:" / "Observe:"  ReAct text format in LLM output
stop_reason == "tool_use"            LLM selected an Action
stop_reason == "end_turn"            LLM has Final Answer
"Final Answer:" in LLM output        ReAct termination signal
"Let's think step by step"           Chain of Thought trigger (no tools)
hub.pull("hwchase17/react")          Standard ReAct prompt from LangChain Hub
create_react_agent(llm, tools, p)    LangChain ReAct agent builder
AgentExecutor(agent, tools)          The loop runner + safety wrapper
max_iterations=5                     Anti-infinite-loop guard
verbose=True                         Print every T/A/O step to terminal
handle_parsing_errors=True           Auto-retry on malformed LLM output
intermediate_steps                   Full (action, observation) history
return_intermediate_steps=True       Include history in result dict
"""

# ═══════════════════════════════════════════════════════════
# 3. MINIMAL REACT SETUP (LangChain)
# ═══════════════════════════════════════════════════════════
"""
from langchain.agents import create_react_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain import hub

@tool
def my_tool(input: str) -> str:
    \"\"\"What it does + when to use it.\"\"\"
    return f"Result for: {input}"

llm      = ChatAnthropic(model="claude-sonnet-5-5")
tools    = [my_tool]
prompt   = hub.pull("hwchase17/react")
agent    = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools,
                         verbose=True, max_iterations=5,
                         handle_parsing_errors=True)

result = executor.invoke({"input": "Your question"})
print(result["output"])
"""

# ═══════════════════════════════════════════════════════════
# 4. CHAIN OF THOUGHT TRIGGER
# ═══════════════════════════════════════════════════════════
"""
# Add to any prompt to activate step-by-step reasoning:
"Let's think step by step."
"Think through this carefully."
"Show your work."

# CoT does NOT call tools — reasoning only.
# Use when: math, logic, multi-step reasoning with known facts.
# Use ReAct when: current data, files, databases needed.
"""

# ═══════════════════════════════════════════════════════════
# 5. REACT SYSTEM PROMPT SKELETON (Anthropic Direct)
# ═══════════════════════════════════════════════════════════
REACT_SYSTEM_PROMPT = """You are a ReAct agent. Follow this format exactly:

Thought: [reason about what you need and which tool to use]
Action: [tool_name]
Action Input: [tool arguments as JSON]

You will receive an Observation after each Action.
Continue Thought → Action → Observation until you have the answer.
Then write: Final Answer: [your complete answer]"""

# ═══════════════════════════════════════════════════════════
# 6. STOP REASONS IN REACT LOOP
# ═══════════════════════════════════════════════════════════
"""
response.stop_reason == "end_turn"  → LLM wrote Final Answer → exit loop
response.stop_reason == "tool_use"  → LLM wants to act → execute → loop back
response.stop_reason == "max_tokens"→ Hit token limit → increase max_tokens

In AgentExecutor (LangChain):
  max_iterations reached             → force stop, return best answer so far
"""

# ═══════════════════════════════════════════════════════════
# 7. COMMON REACT MISTAKES
# ═══════════════════════════════════════════════════════════
"""
MISTAKE 1: No max_iterations → infinite loop
  FIX: AgentExecutor(..., max_iterations=5)

MISTAKE 2: Forgetting handle_parsing_errors
  LLM produces bad format → agent crashes
  FIX: AgentExecutor(..., handle_parsing_errors=True)

MISTAKE 3: Vague tool descriptions → wrong tool selected
  FIX: Write excellent tool descriptions (L11 rule applies here)

MISTAKE 4: Not reading intermediate_steps when debugging
  FIX: result["intermediate_steps"] shows every T/A/O step

MISTAKE 5: Using CoT when live data needed
  "Let's think step by step about current Bitcoin price" → LLM guesses
  FIX: Use ReAct with web_search tool instead
"""

# ═══════════════════════════════════════════════════════════
# 8. REACT VS COT QUICK DECISION
# ═══════════════════════════════════════════════════════════
"""
Use Chain of Thought when:
  ✓ Pure math or logic
  ✓ Information is in LLM training data
  ✓ No external data needed
  ✓ Speed matters (no tool round-trips)

Use ReAct when:
  ✓ Need current / live information
  ✓ Need to read files or databases
  ✓ Need verified calculations
  ✓ Multiple types of information needed
"""

print("ReAct cheatsheet loaded!")
print("Key: Thought → Action → Observe → repeat → Final Answer.")
print("     max_iterations + handle_parsing_errors = production-safe agent.")
