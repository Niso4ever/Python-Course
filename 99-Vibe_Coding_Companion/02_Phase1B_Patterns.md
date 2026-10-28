# Phase 1B — Architecture Patterns (L11–L21, 13 templates)

Now you summon whole *patterns*, not single functions. This is where the five
Modes start to matter — note the **Mode 4 (Debugging)** and **Mode 5
(Integration)** entries; they read completely differently from the Mode 2 specs.

---

## 21. `template_async_patterns.py` — L11 Async
**Level 2 (Behavior) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: asyncio + async/await. DEMO path runs with no API key. Show timing proof.
REQUEST: Three async patterns — parallel LLM calls (gather), streaming, batch processing.
VALIDATION: Parallel version is measurably faster than sequential (print elapsed time).
```
#### 💻 PRODUCES (essence)
```python
async def ask_all(prompts: list[str]) -> list[str]:
    return await asyncio.gather(*(call_llm(p) for p in prompts))  # parallel
```

---

## 22. `template_debug_toolkit.py` — L12 Debugging
**Level 2 · Mode 4 (Debugging)** — the Evidence Package mindset, as reusable tools.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Drop-in functions, paste at top of any file, remove when done.
REQUEST: Debug helpers — pretty-print any object, time a block, audit a dict's keys,
         and dump the full traceback with context.
VALIDATION: Each helper works on arbitrary input; none raise on None/empty.
```
#### 💻 PRODUCES (essence)
```python
def inspect(obj, label="DEBUG"):
    print(f"[{label}] type={type(obj).__name__} value={json.dumps(obj, default=str)}")
def timed(fn): ...  # prints elapsed ms around any call
```

---

## 23. `template_tool_definition.py` — L13 Tool Schemas
**Level 3 (Contract) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Anthropic tool-schema dicts. Descriptions must be vivid (drives selection).
REQUEST: Define 3 tools (search, calculator, weather) as JSON schemas with typed params.
VALIDATION: Each has name + description + input_schema with required fields listed.
```
#### 💻 PRODUCES (essence)
```python
search_tool = {"name": "search",
    "description": "Search the knowledge base. Use for factual lookups.",
    "input_schema": {"type": "object",
        "properties": {"query": {"type": "string"}}, "required": ["query"]}}
```

---

## 24. `template_tool_executor.py` — L13 Tool Loop
**Level 4 (Test Cases) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Anthropic SDK directly. Route on response.stop_reason with match/case.
REQUEST: The full tool-use loop: call → if stop_reason=="tool_use" run tool → feed result
         back → repeat until "end_turn".
VALIDATION: stop_reason=="tool_use" dispatches; "end_turn" exits; unknown tool is handled.
```
#### 💻 PRODUCES (essence)
```python
while True:
    resp = client.messages.create(...)
    match resp.stop_reason:
        case "tool_use":  messages.append(run_tool(resp))
        case _:           break
```

---

## 25. `template_memory_agent.py` — L14 Memory Stack
**Level 3 · Mode 2** — this is the Field Manual's own Constraint Sandwich example.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Use Pydantic for messages. Enforce a token budget of 4096. Std lib + pydantic.
REQUEST: A memory manager that stores messages and drops the oldest when the budget
         is exceeded (sliding window).
VALIDATION: Pass mypy; handle empty history; never exceed budget; return #messages dropped.
```
#### 💻 PRODUCES (essence)
```python
def trim_to_budget(messages: list, budget: int = 4096) -> tuple[list, int]:
    dropped = 0
    while count_tokens(messages) > budget:
        messages.pop(0); dropped += 1
    return messages, dropped
```

---

## 26. `template_react_patterns.py` — L15 ReAct
**Level 2 · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Thought → Action → Observation loop, printed at each step. DEMO runs dry.
REQUEST: A manual ReAct loop where the agent reasons, picks a tool, observes the result,
         and repeats until it can answer.
VALIDATION: Each iteration prints its Thought/Action/Observation; loop has a max-steps cap.
```
#### 💻 PRODUCES (essence)
```python
for step in range(MAX_STEPS):
    thought = reason(state)            # "I should search for X"
    obs = run_action(thought.action)   # call the tool
    if thought.is_final: return thought.answer
```

---

## 27. `template_dspy_signatures.py` — L16 DSPy
**Level 3 (Contract) · Mode 2** — signatures *are* contracts.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: DSPy. Declare input/output FIELDS, never write the prompt by hand.
REQUEST: A signature for question→answer, wrapped in ChainOfThought, used in a RAG module.
VALIDATION: Swapping the signature changes behavior without touching prompt strings.
```
#### 💻 PRODUCES (essence)
```python
class AnswerQ(dspy.Signature):
    """Answer the question from the context."""
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()
qa = dspy.ChainOfThought(AnswerQ)
```

---

## 28. `template_multi_agent.py` — L17 Multi-Agent
**Mode 5 (Integration)** — the Assembly Spec.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Each agent is already a callable. I'm wiring them, not building them.
REQUEST: Show 4 topologies — sequential pipeline, hierarchical, parallel fan-out,
         critic-actor — over the same set of specialist agents.
VALIDATION: Pipeline passes output→input; fan-out merges results; critic can reject + retry.
```
#### 💻 PRODUCES (essence)
```python
draft = writer(topic)                 # sequential
critique = critic(draft)              # critic-actor
final = writer(topic, critique) if critique.rejected else draft
```

---

## 29. `template_json_persistence.py` — L18 Persistence
**Level 3 · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Save/load conversation to a JSON file on disk. Survive process restarts.
REQUEST: A PersistentAgent that loads its history on init and writes it after each turn.
VALIDATION: Re-running the script remembers the previous session; missing file → fresh start.
```
#### 💻 PRODUCES (essence)
```python
class PersistentAgent:
    def __init__(self, name):
        self.path = f"{name}.json"
        self.history = json.load(open(self.path)) if os.path.exists(self.path) else []
    def save(self): json.dump(self.history, open(self.path, "w"))
```

---

## 30. `template_api_tool.py` — L19 Network/APIs
**Level 3 · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: requests library. One standalone tool function. Handle network errors.
REQUEST: A get_joke(topic) tool that hits a real public API — the shape you'd give an
         LLM to "look up live information."
VALIDATION: Timeout/4xx returns a friendly string, not a traceback; returns parsed JSON.
```
#### 💻 PRODUCES (essence)
```python
def get_joke(topic: str = "") -> str:
    try:    r = requests.get(API_URL, params={"q": topic}, timeout=5)
    except requests.RequestException: return "Joke service unavailable."
    return r.json()["joke"]
```

---

## 31. `template_evaluator.py` — L24 Evaluation
**Level 4 (Test Cases) · Mode 2**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Pydantic for results, @dataclass for config. Measure quality, cost, latency.
REQUEST: An evaluator that runs an AI system over test cases and scores accuracy + $ + ms.
VALIDATION: Returns a typed report; a failing case is recorded, not fatal; averages computed.
```
#### 💻 PRODUCES (essence)
```python
class EvalResult(BaseModel):
    accuracy: float = Field(description="0.0-1.0 correctness")
    avg_latency_ms: float = Field(description="mean response time")
    total_cost_usd: float = Field(description="summed call cost")
```

---

## 32. `template_streamlit_chat.py` — L20 Serving
**Level 1 (Features) · Mode 1 (Exploration)**

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Streamlit. Wrap ANY object that has a .chat(str)->str method. No agent logic.
REQUEST: A web chat UI — input box, message history, typing delay — over a pluggable agent.
VALIDATION: Swapping the agent class changes behavior without touching UI code.
```
#### 💻 PRODUCES (essence)
```python
if prompt := st.chat_input("Ask..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    reply = agent.chat(prompt)
    st.chat_message("assistant").write(reply)
```

---

## 33. `template_system_prompt.py` — L21 Vibe Coding
**Level 4 (Test Cases) · Mode 2** — building the constraints *into* the prompt itself.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: A builder class. Separate role / constraints / examples sections.
REQUEST: A PromptBuilder that assembles a constraint-heavy system prompt — add_constraint(),
         add_example(), build_prompt().
VALIDATION: Output has [ROLE]/[CONSTRAINTS]/[EXAMPLES] sections; constraints render as bullets.
```
#### 💻 PRODUCES (essence)
```python
class PromptBuilder:
    def add_constraint(self, rule): self.constraints.append(f"- {rule}")
    def build_prompt(self) -> str:
        return f"[ROLE]\n{self.role}\n\n[CONSTRAINTS]\n" + "\n".join(self.constraints)
```
> This template is itself a vibe-coding tool — it bakes Layer 1 (constraints) into code.
