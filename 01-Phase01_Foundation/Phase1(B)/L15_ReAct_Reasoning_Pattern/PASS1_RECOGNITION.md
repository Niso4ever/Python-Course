# PASS 1: ReAct Pattern Recognition

**Rule:** Read each example. Identify the Thought / Action / Observation structure.

---

## Example 1: ReAct in Plain Text (What the LLM Produces)

```
Question: What is 17% of 8,432, and what is the capital of France?

Thought: I need two things:
         1. A calculation (17% of 8,432) — use calculator tool
         2. Capital of France — I know this: Paris

         Let me do the calculation first.

Action: calculator
Action Input: {"expression": "8432 * 0.17"}

Observation: 1433.44

Thought: I have the calculation result (1433.44) and I know Paris.
         I now have everything I need.

Final Answer: 17% of 8,432 is 1,433.44. The capital of France is Paris.
```

**Identify:** Where is each Thought? Action? Observation? Final Answer?
**Notice:** The LLM *knows* Paris without a tool. It only calls the calculator for the math.

---

## Example 2: ReAct Loop in Python (Anthropic Direct)

```python
def run_react_agent(question: str, tools: list, tool_registry: dict) -> str:
    messages = [{"role": "user", "content": question}]
    max_steps = 6

    for step in range(max_steps):                # ← LOOP (the "React" in ReAct)
        response = client.messages.create(
            model="claude-sonnet-5-5",
            system=REACT_SYSTEM_PROMPT,          # ← prompt enforces T/A/O format
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return extract_final_answer(response)   # ← done

        if response.stop_reason == "tool_use":      # ← Action occurred
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = tool_registry[block.name](**block.input)  # ← execute
                    tool_results.append({                              # ← Observation
                        "type":        "tool_result",
                        "tool_use_id": block.id,
                        "content":     str(result)
                    })

            messages.append({"role": "user", "content": tool_results})  # ← feed back

    return "Max steps reached."
```

**Identify:** What is the LOOP? What triggers ACTION? What is the OBSERVATION?
**Key pattern:** `stop_reason == "tool_use"` → execute → feed back → loop again

---

## Example 3: LangChain ReAct (One-Line Setup)

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain import hub

@tool
def calculator(expression: str) -> str:
    """Evaluate math expressions. Use for all arithmetic."""
    return str(eval(expression, {"__builtins__": {}}, {}))

@tool
def web_search(query: str) -> str:
    """Search the internet for current information."""
    return f"[Search results for: {query}]"

llm   = ChatAnthropic(model="claude-sonnet-5-5")
tools = [calculator, web_search]

prompt   = hub.pull("hwchase17/react")        # ← ReAct prompt template
agent    = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

result = executor.invoke({"input": "What is 15% of 8,432?"})
print(result["output"])

# With verbose=True, you see:
# Thought: I need to calculate 15% of 8432.
# Action: calculator
# Action Input: 8432 * 0.15
# Observation: 1264.8
# Thought: I have the answer.
# Final Answer: 15% of 8,432 is 1,264.80.
```

**Identify:** What is `hub.pull`? What does `verbose=True` show? What is `max_iterations`?
**Key pattern:** `create_react_agent` + `AgentExecutor` = full ReAct loop in 5 lines

---

## Example 4: Multi-Step ReAct (Chained Tool Calls)

```
Question: Compare the populations of Tokyo and New York, then tell me the ratio.

Thought: I need Tokyo's population. Search for it.
Action: web_search
Action Input: "Tokyo population 2025"
Observation: Tokyo population: approximately 13.96 million (city), 37.4M (metro)

Thought: I have Tokyo. Now I need New York.
Action: web_search
Action Input: "New York City population 2025"
Observation: New York City population: approximately 8.3 million

Thought: I have both. Now calculate the ratio.
Action: calculator
Action Input: 13.96 / 8.3
Observation: 1.6819...

Thought: Tokyo's city population is ~1.68× New York's.
Final Answer: Tokyo (13.96M) is about 1.68× the size of New York City (8.3M).
```

**Identify:** How many loops before Final Answer?
**Notice:** Each Thought decides WHAT to do next and WHY.

---

## Example 5: Chain of Thought (ReAct Without Tools)

```python
# No tools — just the LLM reasoning step by step
response = client.messages.create(
    model="claude-sonnet-5-5",
    messages=[{
        "role": "user",
        "content": (
            "A store had 500 items. They sold 30% on Monday, "
            "then received 80 new items Tuesday. How many do they have now? "
            "Let's think step by step."    # ← triggers Chain of Thought
        )
    }]
)

# LLM output:
# Step 1: Initial inventory = 500 items
# Step 2: Sold on Monday = 500 × 0.30 = 150 items
# Step 3: Remaining after Monday = 500 - 150 = 350 items
# Step 4: Received Tuesday = 80 new items
# Step 5: Final inventory = 350 + 80 = 430 items
# Answer: 430 items
```

**Identify:** What phrase triggers CoT? Does this use any tools?
**Difference from ReAct:** CoT = reasoning only. ReAct = reasoning + external tools.

---

## Example 6: `intermediate_steps` — Reading Agent History

```python
result = executor.invoke({"input": "Research and summarize AI news"})

# The agent's full work history:
for action, observation in result["intermediate_steps"]:
    print(f"Tool used: {action.tool}")
    print(f"Tool input: {action.tool_input}")
    print(f"Observation: {observation[:100]}")
    print("---")

# Output:
# Tool used: web_search
# Tool input: AI news 2025
# Observation: [Claude 4 released, GPT-5 rumors...]
# ---
# Tool used: web_search
# Tool input: latest AI research papers
# Observation: [Attention mechanism improvements...]
# ---
```

**What is `intermediate_steps`?** The complete (Action, Observation) history
**When to use?** Debugging — see exactly what the agent searched and what it found

---

## Example 7: `handle_parsing_errors` — Graceful Recovery

```python
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,   # ← RECOVERY MODE
    # Without this, if LLM produces malformed T/A/O output → crash
    # With this, LangChain automatically retries with error message
)
```

**Why it matters:** LLMs sometimes produce imperfect ReAct format:
```
Thought: I should search
web_search("query")     ← MALFORMED: no "Action:" prefix
```
Without `handle_parsing_errors=True` → crash.
With it → LangChain tells LLM "invalid format, try again."

---

## Example 8: `return_intermediate_steps` — Full Audit

```python
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True,   # ← AUDIT MODE
)

result = executor.invoke({"input": "What is AI investment in 2025?"})
print("Final answer:", result["output"])
print("\nFull trace:")
for step in result["intermediate_steps"]:
    action, observation = step
    print(f"  → Called: {action.tool}({action.tool_input})")
    print(f"  ← Got: {observation[:80]}...")
```

**When to use?** Debugging wrong answers — see exactly what data the agent found
**Connects to L10:** This is the "print audit" from debugging lesson applied to ReAct

---

## Pattern Summary Table

| Code signal | Meaning |
|:-----------|:--------|
| `"Thought:" / "Action:" / "Observation:"` | ReAct text format |
| `stop_reason == "tool_use"` | LLM selected an Action |
| `stop_reason == "end_turn"` | LLM has Final Answer |
| `"Final Answer:"` in output | ReAct termination signal |
| `"Let's think step by step"` | Chain of Thought trigger |
| `hub.pull("hwchase17/react")` | Standard ReAct prompt template |
| `create_react_agent(llm, tools, prompt)` | LangChain ReAct builder |
| `AgentExecutor(agent, tools)` | The loop runner |
| `max_iterations=5` | Anti-infinite-loop guard |
| `verbose=True` | Print every T/A/O step |
| `handle_parsing_errors=True` | Auto-retry on bad format |
| `intermediate_steps` | Full (action, observation) history |
