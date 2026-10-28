# Lesson 18 — Pass C: VISUAL PATTERNS
## See the Agent Loop as a Machine

**Goal:** Burn the loop shape into memory through diagrams. When you later read framework code, you'll recognize the loop even when it's hidden.

---

## Visual 1: The Core Loop Machine

### Code:
```python
def run_agent(question):
    messages = [{"role": "user", "content": question}]
    while True:
        response = client.messages.create(tools=tools, messages=messages)
        if response.stop_reason == "end_turn":
            return response.content[0].text
        messages.append({"role": "assistant", "content": response.content})
        results = execute_tools(response.content)
        messages.append({"role": "user", "content": results})
```

**Example call:**
```python
answer = run_agent("What is the capital of France?")
print(answer)  # "The capital of France is Paris."
# → 1 iteration: no tools needed → end_turn immediately
```

### Visual:
```
User Question
      │
      ▼
┌─────────────────┐
│   THINK (LLM)   │ ← client.messages.create(...)
└─────────────────┘
      │
  stop_reason?
      │
   ┌──┴──┐
   │     │
"end_  "tool_
 turn"  use"
   │     │
   ▼     ▼
RETURN  ACT  ← execute_tools(response.content)
answer   │
         ▼
       OBSERVE ← messages.append(tool_results)
         │
         └──────────────────────────┐
                                    ▼
                             back to THINK
```

**Pattern:** One entry point (question), one exit (answer), loop in between.

---

## Visual 2: The Message List Growing

Each iteration adds two rows to the conversation list.

### After iteration 1 (tool call):
```
messages = [
  {"role": "user",      "content": "What is the weather in Tokyo?"}   ← original question
  {"role": "assistant", "content": [tool_use block]}                  ← agent's request
  {"role": "user",      "content": [tool_result block]}               ← tool answer
]
```

### After iteration 2 (another tool call):
```
messages = [
  {"role": "user",      "content": "What is the weather in Tokyo?"}
  {"role": "assistant", "content": [tool_use block]}
  {"role": "user",      "content": [tool_result block]}
  {"role": "assistant", "content": [tool_use block]}                  ← new agent request
  {"role": "user",      "content": [tool_result block]}               ← new tool answer
]
```

### After iteration 3 (done):
```
messages = [
  {"role": "user",      "content": "What is the weather in Tokyo?"}
  {"role": "assistant", "content": [tool_use block]}
  {"role": "user",      "content": [tool_result block]}
  {"role": "assistant", "content": [tool_use block]}
  {"role": "user",      "content": [tool_result block]}
  {"role": "assistant", "content": "It is 22°C and sunny in Tokyo."}  ← final answer
]
```

**Visual:**
```
Iteration 0:  [Q]
Iteration 1:  [Q] [A:tool] [U:result]
Iteration 2:  [Q] [A:tool] [U:result] [A:tool] [U:result]
Iteration 3:  [Q] [A:tool] [U:result] [A:tool] [U:result] [A:DONE]
                                                                  ↑
                                                             exit here
```

**Pattern:** The list is the agent's memory. It grows by +2 every tool call.

---

## Visual 3: The Two Exit Paths

```
                    LLM Response
                         │
           ┌─────────────┴─────────────┐
           │                           │
    stop_reason =              stop_reason =
     "end_turn"                  "tool_use"
           │                           │
           ▼                           ▼
   ┌───────────────┐         ┌────────────────────┐
   │  Return text  │         │  Execute tools     │
   │  to the user  │         │  (dispatch fn)     │
   └───────────────┘         └────────────────────┘
        (EXIT)                         │
                                       ▼
                              ┌────────────────────┐
                              │  Append to messages│
                              └────────────────────┘
                                       │
                                       ▼
                                  Loop again
                                  (THINK again)
```

**Pattern:** Left path = done. Right path = keep going.

---

## Visual 4: The Tool Dispatcher

### Code:
```python
def execute_tools(blocks):
    results = []
    for block in blocks:
        if block.type == "tool_use":
            result = dispatch(block.name, block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result)
            })
    return results
```

**Example call:**
```python
# Simulating response.content with a tool_use block
results = execute_tools([
    MockBlock(type="tool_use", id="tu_001", name="search_web", input={"query": "Tokyo weather"})
])
print(results)
# [{"type": "tool_result", "tool_use_id": "tu_001", "content": "22°C, sunny"}]
```

### Visual:
```
response.content = [
    TextBlock(type="text",     text="I'll search for that..."),
    ToolUseBlock(type="tool_use", name="search_web", id="tu_001",
                 input={"query": "Tokyo weather"})
]
        │
        ▼
for block in blocks:
        │
   type == "tool_use"?
        │
    YES │              NO
        ▼              ▼
  dispatch(           skip
   name, input)
        │
        ▼
 {"type": "tool_result",
  "tool_use_id": "tu_001",   ← MUST match the block.id
  "content": "22°C, sunny"}
```

**Pattern:** Filter → dispatch → wrap result with matching id.

---

## Visual 5: Safety Guard (Max Iterations)

```python
for step in range(10):          # ← safe: will stop after 10
    response = client.messages.create(...)
    if response.stop_reason == "end_turn":
        return response.content[0].text
    # handle tools...
return "Limit reached"           # ← guaranteed exit
```

**Example call:**
```python
answer = run_agent_safe("Plan a 20-step marketing campaign.", max_iterations=5)
print(answer)
# → Ran 5 steps → returned partial answer with notice
```

### Visual:
```
step=0 → THINK → tool_use → ACT → OBSERVE
step=1 → THINK → tool_use → ACT → OBSERVE
step=2 → THINK → tool_use → ACT → OBSERVE
step=3 → THINK → tool_use → ACT → OBSERVE
step=4 → THINK → tool_use → ACT → OBSERVE
step=5 → LIMIT HIT → return fallback
              ↑
         no matter what, exits here
```

**Pattern:** `range(N)` replaces `while True`. Safer for production.

---

## Visual 6: Framework Comparison — All the Same Loop

```
CrewAI:
  crew.kickoff()
    → crew._run_tasks()
      → agent.execute_task()
        → while not done:        ← THE LOOP
            llm.predict(...)
            if tool_call: run_tool(...)

LangGraph:
  graph.invoke(state)
    → node runs
      → edge decides next node
        → while not END:         ← THE LOOP (as graph traversal)
            run_node(state)
            if tool_node: execute_tools(state)

OpenAI Agents SDK:
  Runner.run(agent, input)
    → while True:                ← THE LOOP
        response = model.get_response(...)
        if stop: break
        run_tools(response.tool_calls)

Raw Anthropic (THIS LESSON):
  while True:                    ← THE LOOP, no disguise
      response = client.messages.create(...)
      if stop_reason == "end_turn": return
      execute_tools(response.content)
```

**Pattern:** Different names, different decorators — one loop.

---

## Visual 7: The Agent as a State Machine

```
STATES:
  ┌──────────┐     call LLM     ┌──────────────┐
  │  START   │────────────────► │   THINKING   │
  └──────────┘                  └──────────────┘
                                       │
                         ┌─────────────┴──────────┐
                         │                        │
                  "end_turn"                 "tool_use"
                         │                        │
                         ▼                        ▼
                  ┌──────────┐         ┌──────────────────┐
                  │   DONE   │         │    EXECUTING     │
                  └──────────┘         └──────────────────┘
                       │                        │
                   return                 append results
                   answer                       │
                                                ▼
                                        ┌──────────────┐
                                        │  OBSERVING   │
                                        └──────────────┘
                                                │
                                                └──► back to THINKING
```

**Pattern:** Three states — THINKING, EXECUTING, OBSERVING — cycling until DONE.

---

## Color Coding Method

When reading agent loop code, mentally color:

- **Blue** = Loop structure (`while`, `for`, `if stop_reason`)
- **Green** = LLM calls (`client.messages.create`)
- **Yellow** = Message accumulation (`messages.append`)
- **Orange** = Tool dispatch (`execute_tools`, `dispatch`)

```python
🔵while True:
    🟢response = client.messages.create(
        model="claude-opus-5-5",
        tools=tools,
        messages=messages
    )
    🔵if response.stop_reason == "end_turn":
        return response.content[0].text
    🟡messages.append({"role": "assistant", "content": response.content})
    🟠results = execute_tools(response.content)
    🟡messages.append({"role": "user", "content": results})
```

---

## You've Completed Pass C!

You can now:
✓ **See** the loop as a flowchart — entry → think → decide → act → observe → repeat
✓ **Visualize** the message list growing
✓ **Recognize** the two exit paths instantly
✓ **Map** framework code back to the raw loop
✓ **Understand** why safety guards (max iterations) matter

**Next:** Pass 3 — Copy agent loop templates and use them.
