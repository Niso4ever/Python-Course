# Lesson 18 — Pass 3: TEMPLATES
## Your Agent Loop Copy-Paste Library

**Goal:** Five production-ready agent loop patterns. Copy, rename, modify, use.

> **2026 Note:** All templates use `import anthropic` directly. No framework dependency. When frameworks change (again), these still work.

---

## How to Use These Templates

1. **Identify** what kind of loop you need (one-shot, safe, verbose, async)
2. **Copy** the matching template
3. **Replace** the tool list with your actual tools
4. **Call** it with your user's question

---

## Template 1: Minimal Agent Loop
**Use when:** Simple tasks, learning, prototyping

```python
import anthropic

client = anthropic.Anthropic()

def run_agent(question: str, tools: list) -> str:
    messages = [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        messages.append({"role": "assistant", "content": response.content})
        results = execute_tools(response.content)       # ← your dispatcher here
        messages.append({"role": "user", "content": results})
```

**Example call:**
```python
answer = run_agent("What is the capital of Japan?", tools=[search_tool])
print(answer)
# → "The capital of Japan is Tokyo."
```

---

## Template 2: Safe Agent Loop (Production)
**Use when:** Any production system — always cap your loops

```python
import anthropic

client = anthropic.Anthropic()

def run_agent_safe(
    question: str,
    tools: list,
    system: str = "You are a helpful assistant.",
    max_iterations: int = 15
) -> dict:
    messages = [{"role": "user", "content": question}]
    iterations = 0

    while iterations < max_iterations:
        iterations += 1

        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return {
                "answer": response.content[0].text,
                "iterations": iterations,
                "status": "complete"
            }

        messages.append({"role": "assistant", "content": response.content})
        results = execute_tools(response.content)
        messages.append({"role": "user", "content": results})

    return {
        "answer": "Reached iteration limit without completing.",
        "iterations": iterations,
        "status": "limit_reached"
    }
```

**Example calls:**
```python
result = run_agent_safe("Research and summarize AI news from this week.", tools=[search_tool])
print(result["answer"])      # the answer
print(result["iterations"])  # 4  (took 4 tool calls)
print(result["status"])      # "complete"

# If agent gets stuck:
result = run_agent_safe("Do 50 things.", tools=[search_tool], max_iterations=5)
print(result["status"])  # "limit_reached"
```

---

## Template 3: Agent Loop with Tracing
**Use when:** Debugging, observability, understanding what the agent is doing

```python
import anthropic

client = anthropic.Anthropic()

def run_agent_traced(question: str, tools: list, verbose: bool = True) -> str:
    messages = [{"role": "user", "content": question}]
    step = 0

    while True:
        step += 1
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if verbose:
            print(f"\n[Step {step}] stop_reason = {response.stop_reason}")

        if response.stop_reason == "end_turn":
            if verbose:
                print(f"[Done] Completed in {step} step(s).")
            return response.content[0].text

        for block in response.content:
            if block.type == "tool_use" and verbose:
                print(f"  → Tool: {block.name}")
                print(f"  → Input: {block.input}")

        messages.append({"role": "assistant", "content": response.content})
        results = execute_tools(response.content)

        if verbose:
            for r in results:
                print(f"  ← Result: {r['content'][:100]}...")

        messages.append({"role": "user", "content": results})
```

**Example call:**
```python
answer = run_agent_traced("Who won the FIFA World Cup in 2026?", tools=[search_tool])
# Output:
# [Step 1] stop_reason = tool_use
#   → Tool: search_web
#   → Input: {"query": "FIFA World Cup 2026 winner"}
#   ← Result: "The 2026 FIFA World Cup was won by..."
# [Step 2] stop_reason = end_turn
# [Done] Completed in 2 step(s).
```

---

## Template 4: Agent Loop with System Prompt + History
**Use when:** Chatbot — multi-turn conversation with persistent context

```python
import anthropic

client = anthropic.Anthropic()

def run_agent_chat(
    user_message: str,
    history: list,
    tools: list,
    system: str
) -> tuple[str, list]:
    """
    Returns (answer, updated_history).
    Pass the returned history back on the next turn.
    """
    messages = history + [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            answer = response.content[0].text
            # Append this full exchange to history
            messages.append({"role": "assistant", "content": answer})
            return answer, messages           # ← return updated history

        messages.append({"role": "assistant", "content": response.content})
        results = execute_tools(response.content)
        messages.append({"role": "user", "content": results})
```

**Example calls:**
```python
system = "You are a research assistant. Use search to answer questions accurately."
history = []

# Turn 1
answer, history = run_agent_chat("What is RAG?", history, tools=[search_tool], system=system)
print(answer)         # "RAG stands for Retrieval-Augmented Generation..."
print(len(history))   # 2 messages in history now

# Turn 2 — agent remembers the conversation
answer, history = run_agent_chat("Give me an example.", history, tools=[search_tool], system=system)
print(answer)         # "Here's an example of RAG in action..."
print(len(history))   # 4 messages now
```

---

## Template 5: Async Agent Loop (Production Scale)
**Use when:** Handling multiple users simultaneously, FastAPI backend, production APIs

```python
import anthropic
import asyncio

client = anthropic.AsyncAnthropic()

async def run_agent_async(
    question: str,
    tools: list,
    system: str = "You are a helpful assistant.",
    max_iterations: int = 15
) -> str:
    messages = [{"role": "user", "content": question}]
    iterations = 0

    while iterations < max_iterations:
        iterations += 1

        response = await client.messages.create(
            model="claude-opus-5-5",
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        messages.append({"role": "assistant", "content": response.content})
        results = await execute_tools_async(response.content)   # ← async dispatcher
        messages.append({"role": "user", "content": results})

    return "Max iterations reached."

# Example call (in an async context):
async def main():
    # Run two agents simultaneously
    results = await asyncio.gather(
        run_agent_async("What is RAG?",  tools=[search_tool]),
        run_agent_async("What is MCP?",  tools=[search_tool])
    )
    for r in results:
        print(r[:100])

asyncio.run(main())
# → Both agents run in parallel, return together
```

---

## Quick Selection Guide

| Need | Template |
|:-----|:---------|
| Learning / prototyping | Template 1: Minimal |
| Any production system | Template 2: Safe (with limit) |
| Debugging agent behavior | Template 3: Traced |
| Multi-turn chatbot | Template 4: Chat with history |
| Multiple users / API backend | Template 5: Async |

---

## The execute_tools Dispatcher (Required by all templates)

```python
def execute_tools(content_blocks: list) -> list:
    """Dispatch tool calls from agent response. Attach to any template above."""
    tool_results = []
    for block in content_blocks:
        if block.type == "tool_use":
            result = dispatch(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result)
            })
    return tool_results

def dispatch(tool_name: str, tool_input: dict) -> str:
    """Map tool names to Python functions. Add your tools here."""
    tool_map = {
        "search_web":   search_web,     # ← replace with real functions
        "read_file":    read_file,
        "run_python":   run_python,
    }
    fn = tool_map.get(tool_name)
    if fn:
        return fn(**tool_input)
    return f"Unknown tool: {tool_name}"
```

**Example call:**
```python
# With a simulated tool_use block:
results = execute_tools([
    MockBlock(type="tool_use", id="tu_01", name="search_web", input={"query": "RAG"})
])
print(results)
# [{"type": "tool_result", "tool_use_id": "tu_01", "content": "RAG is..."}]
```
