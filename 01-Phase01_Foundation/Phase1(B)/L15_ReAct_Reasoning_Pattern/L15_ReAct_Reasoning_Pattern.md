# Lesson 15: ReAct Reasoning Pattern

**Estimated time: 1 hour**

> **Version note (checked 2026-10-28):** The LangChain agent code in this lesson is LangChain 0.x style (`from langchain.agents import AgentExecutor, create_react_agent`). You will still meet it in older repos. In LangChain 1.x those legacy pieces live in the separate `langchain-classic` package (`from langchain_classic.agents import AgentExecutor, create_react_agent`), and new code builds agents with `from langchain.agents import create_agent`. The loop you are learning to read is the same.

---

## The Detective Theory

Sherlock Holmes never says "I don't know" and immediately guesses. He **observes**, **reasons**, and then **acts** — one step at a time. If his first action gives new information, he reasons again before acting again.

ReAct is Sherlock Holmes as code.

```
ReAct = Reason → Act → Observe (loop until done)

Thought:   "The user asks for today's weather in Tokyo."
           "I don't know today's weather — I need to search."
Action:    web_search("Tokyo weather today")
Observe:   "18°C, cloudy, 80% humidity"

Thought:   "I have the answer."
Final:     "Tokyo is 18°C and cloudy today."
```

The key insight: **the LLM thinks out loud before acting**. The scratchpad (Thought) is where the reasoning happens. Without it, the agent would guess instead of look things up.

---

## Why ReAct Exists

Before ReAct, agents had two problems:

**Problem 1: Acting without thinking** — Agent calls tools randomly, gets confused by results.

**Problem 2: Thinking without acting** — Agent reasons in circles, never uses tools when needed.

ReAct solves both by forcing the pattern: *always reason before acting, always observe before reasoning again.*

---

## The ReAct Loop (Full Anatomy)

```
┌─────────────────────────────────────────────────────────┐
│                    ReAct Agent Loop                      │
│                                                         │
│  User question enters                                   │
│         ↓                                               │
│  ┌─────────────────────────────────────────────┐       │
│  │  THOUGHT                                    │       │
│  │  LLM reasons: "What do I know? What do      │       │
│  │  I need? Which tool should I call?"          │       │
│  └─────────────────┬───────────────────────────┘       │
│                    │                                    │
│          "Need more info" ──────────────────┐           │
│                    │                        │           │
│  ┌─────────────────▼───────────────────┐    │           │
│  │  ACTION                             │    │           │
│  │  LLM calls a tool:                  │    │           │
│  │  web_search("Tokyo weather")        │    │           │
│  └─────────────────┬───────────────────┘    │           │
│                    │                        │           │
│  ┌─────────────────▼───────────────────┐    │           │
│  │  OBSERVATION                        │    │           │
│  │  Tool result comes back:            │    │           │
│  │  "18°C, cloudy"                     │    │           │
│  └─────────────────┬───────────────────┘    │           │
│                    │                        │           │
│            loop ───┘                        │           │
│                    │ "I have enough info"   │           │
│  ┌─────────────────▼───────────────────┐    │           │
│  │  FINAL ANSWER                       │    │           │
│  │  LLM composes answer for user       │    │           │
│  └─────────────────────────────────────┘    │           │
└─────────────────────────────────────────────┘           │
```

---

## ReAct in Raw Text (What the LLM Actually Sees)

When you use a ReAct-style prompt, the LLM produces something like this:

```
Question: What is the capital of France and what is 17 × 23?

Thought: I know the capital of France is Paris from my training data.
         But I should use the calculator for arithmetic to be accurate.

Action: calculator
Action Input: 17 * 23

Observation: 391

Thought: I now have both answers. Paris for the capital, 391 for the math.

Final Answer: The capital of France is Paris. 17 × 23 = 391.
```

This text IS the reasoning. The LLM writes its own scratchpad.

---

## ReAct in Code (Anthropic Direct)

```python
import anthropic, json

SYSTEM_PROMPT = """You are a ReAct agent. Use this format:

Thought: [reason about what to do]
Action: [tool name]
Action Input: [tool arguments as JSON]

Wait for Observation, then reason again.
When done: write "Final Answer: [answer]"
"""

def run_react_agent(question: str) -> str:
    client   = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    max_steps = 5

    for step in range(max_steps):
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        text = response.content[0].text

        # Check if agent is done
        if "Final Answer:" in text:
            return text.split("Final Answer:")[-1].strip()

        # Parse the action the agent wants to take
        if "Action:" in text:
            action     = parse_action(text)       # extract tool name
            action_in  = parse_action_input(text) # extract tool args

            # Execute the tool
            observation = execute_tool(action, action_in)

            # Feed result back to agent as "Observation"
            messages.append({"role": "assistant", "content": text})
            messages.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })

    return "Max steps reached."
```

---

## ReAct in LangChain (Automatic)

LangChain builds the entire ReAct loop for you:

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain import hub

# Step 1: Define tools (the "Act" part)
@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression. Use for arithmetic."""
    return str(eval(expression, {"__builtins__": {}}, {}))

@tool
def web_search(query: str) -> str:
    """Search the internet for current information."""
    return f"[Results for: {query}]"   # replace with real API

# Step 2: Get a ReAct prompt template from LangChain Hub
# (This is the system prompt that enforces Thought/Action/Observation)
prompt = hub.pull("hwchase17/react")

# Step 3: Create the ReAct agent
llm   = ChatAnthropic(model="claude-sonnet-5-5")
tools = [calculator, web_search]
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# Step 4: Wrap in executor (adds the loop + safety limits)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,          # ← prints Thought/Action/Observation at each step
    max_iterations=5,      # ← safety: stop if loop doesn't end
    handle_parsing_errors=True   # ← don't crash on malformed output
)

# Step 5: Run
result = executor.invoke({"input": "What is 15% of 8,432?"})
print(result["output"])

# verbose=True output looks like:
# > Entering new AgentExecutor chain...
# Thought: I need to calculate 15% of 8432. Use calculator.
# Action: calculator
# Action Input: 8432 * 0.15
# Observation: 1264.8
# Thought: I have the answer.
# Final Answer: 15% of 8,432 is 1,264.80.
```

---

## Chain of Thought (ReAct's Cousin)

Chain of Thought (CoT) is ReAct *without* tool calls. The LLM reasons step-by-step in text, then gives a final answer — no external tool calls.

```python
# Chain of Thought: just add "Let's think step by step" to prompt
response = client.messages.create(
    model="claude-sonnet-5-5",
    messages=[{
        "role": "user",
        "content": "A train travels 60mph for 2.5 hours. How far? Let's think step by step."
    }]
)
# LLM output:
# Step 1: Speed = 60 mph
# Step 2: Time = 2.5 hours
# Step 3: Distance = Speed × Time = 60 × 2.5 = 150 miles
# Final Answer: 150 miles

# vs. no CoT:
# "150 miles" (correct but no reasoning shown)
# or: "125 miles" (incorrect — LLM skipped reasoning)
```

**When to use CoT:** Math, logical reasoning, multi-step problems where you want to see the work.
**When to use ReAct:** Problems that need external information (web, databases, files).

---

## Reading ReAct Code in the Wild

```
You see this                              You understand
────────────────────────────────────────  ────────────────────────────────────
"Thought:"/"Action:"/"Observation:"       ReAct prompt format
hub.pull("hwchase17/react")               Standard ReAct prompt from LangChain
create_react_agent(llm, tools, prompt)    LangChain ReAct agent builder
AgentExecutor(agent, tools)               The loop runner + safety wrapper
max_iterations=5                          Safety limit on tool call loop
handle_parsing_errors=True                Don't crash if LLM format is wrong
verbose=True                              Print every T/A/O step
intermediate_steps                        Raw (action, observation) tuples
"Final Answer:"                           ReAct termination signal
"I now know the answer"                   CoT-style termination signal
```

---

## Common ReAct Patterns

### Pattern 1: Research + Calculate

```
Question: "If AI investment grew 45% from $50B, what is the new total?"

Thought: I need to calculate 50B × 1.45. Use calculator.
Action: calculator
Action Input: 50 * 1.45
Observation: 72.5
Final Answer: $72.5 billion.
```

### Pattern 2: Search + Summarize

```
Question: "Summarize recent news about Anthropic."

Thought: I need current news. Use web_search.
Action: web_search
Action Input: "Anthropic news 2025"
Observation: [Claude 4 released, funding round, safety research...]
Final Answer: [Summary of news]
```

### Pattern 3: Multi-step Research

```
Thought: I need two things: current price + historical price.
Action: web_search → current price
Observe → got current price
Thought: Now get historical price.
Action: web_search → historical price
Observe → got historical price
Thought: Calculate the change.
Action: calculator
Final Answer: [Price change analysis]
```

---

## The Critical Insight: Thought Is Not Optional

You might ask: "Why not skip the Thought and just call the tool?"

Without Thought, the agent:
- Calls random tools without understanding what it needs
- Gets confused by tool results that don't match expectations
- Loops endlessly without knowing when to stop
- Misses when it already has the answer and doesn't need a tool

The Thought step is where the LLM converts the user's vague question into a concrete plan. It's the difference between a detective who investigates and a detective who guesses.

---

## Pattern Recognition Summary

| Pattern | Meaning |
|:--------|:--------|
| `Thought:` prefix in LLM output | ReAct reasoning step |
| `Action:` + `Action Input:` | ReAct tool selection |
| `Observation:` | Tool result fed back to LLM |
| `Final Answer:` | Agent is done |
| `create_react_agent` | LangChain ReAct setup |
| `AgentExecutor` | The while-loop wrapper |
| `max_iterations=5` | Anti-infinite-loop guard |
| `verbose=True` | Show all T/A/O steps in terminal |
| `hub.pull("hwchase17/react")` | ReAct prompt template from web |

**Next: L14 — DSPy Signature Paradigm**
What if you never wrote a prompt again? DSPy replaces hand-written prompts with learnable programs.
