# Lesson 23 — Pass 1: RECOGNITION
## Learn to READ Design Decisions in Agentic Code

**Goal:** When you look at an agentic system — real or AI-generated — recognize what design decisions were made, why, and whether they were the right ones.

> **This pass is different.** Instead of code patterns to spot, you're reading ARCHITECTURAL DECISIONS embedded in code. The question isn't "what is this code doing?" but "WHY was this designed this way?"

---

## The Six Design Signals

When reading agentic code, look for these six decisions:

### Signal 1: Agent vs. Single Call
```python
# SINGLE CALL (no agent needed):
response = client.messages.create(model="claude-opus-5-5", messages=[...])
answer = response.content[0].text

# AGENT (loop needed):
while True:
    response = client.messages.create(tools=tools, messages=messages)
    if response.stop_reason == "end_turn": return ...
```
**Read:** Does this have a loop? If yes → they decided an agent was needed.
**Ask yourself:** Was a loop actually necessary, or would one call have worked?

---

### Signal 2: How Many Agents
```python
# ONE agent (simple):
answer = run_agent(question, tools=ALL_TOOLS)

# MULTIPLE agents (orchestrator + specialists):
research = research_agent(topic)
article  = writer_agent(research)
```
**Read:** Count the `run_agent()` calls. One = single agent. Multiple = multi-agent design.
**Ask yourself:** Did the task genuinely need specialization, or is one agent doing it fine?

---

### Signal 3: Tool Selection Signals
```python
# MINIMAL tools (good design):
tools = [search_tool]   # only what's needed

# OVER-TOOLED (design smell):
tools = [search, calculate, format, email, calendar, database, api1, api2, ...]
# ↑ Too many — agent will be confused about which to use
```
**Read:** Count the tools. More than 5-7 in one agent is often a design problem.
**Read:** Are the tools named precisely? Vague names = vague behavior.

---

### Signal 4: System Prompt Quality
```python
# GOOD system prompt (tells WHO, WHAT, and HOW):
system = """You are a Research Analyst specializing in AI trends.
Your task: find accurate, current information using the search tool.
Always verify information with at least 2 searches before answering.
Return findings with confidence level."""

# WEAK system prompt (design smell):
system = "Be helpful."
# ↑ Agent has no persona, no focus, no constraints
```
**Read:** Is the system prompt specific about role, task, and constraints?

---

### Signal 5: Guardrails
```python
# WITH guardrails:
if not validate_query(user_input):          # ← input validation
    return {"error": "Invalid input"}

result = run_agent(user_input, max_iterations=15)  # ← loop cap

if not quality_gate(result).passes:         # ← output validation
    return regenerate()

# WITHOUT guardrails:
result = run_agent(user_input)   # ← no input check, no loop cap, no output check
```
**Read:** Are there input validators, loop caps, and output gates?

---

### Signal 6: Memory Strategy
```python
# NO memory (stateless — each call starts fresh):
messages = [{"role": "user", "content": question}]

# SESSION memory (multi-turn — remembers this conversation):
messages = history + [{"role": "user", "content": question}]

# PERSISTENT memory (cross-session — remembers between calls):
long_term = db.load_context(user_id)
messages = long_term + [{"role": "user", "content": question}]
```
**Read:** What does `messages` start with? Dict with just user message = stateless. Something loaded = memory.

---

## Real Design Examples to RECOGNIZE

### Design Pattern 1: Correct — "Don't over-agent"

```python
# User asks: "What is RAG?"
# Design decision: single call, no tools needed
def answer_definition(question: str) -> str:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=512,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

answer = answer_definition("What is RAG?")
```

**READ THE DESIGN:** This uses a single LLM call — no agent loop, no tools.
**WHY CORRECT:** "What is RAG?" is a factual question the model already knows. An agent loop + web search would be slower, more expensive, and unnecessary.
**The Rule:** If the model already knows the answer, don't use an agent.

---

### Design Pattern 2: Correct — "Minimal tool set"

```python
# Task: Research recent AI news and summarize
# Design decision: one search tool, one agent
news_search_tool = {
    "name": "search_recent_news",           # ← precise name
    "description": "Search for AI news published in the last 7 days. Use this for current events only.",
    "input_schema": {...}
}

def news_agent(topic: str) -> str:
    return run_agent(
        topic,
        tools=[news_search_tool],            # ← ONE tool
        system="You are a news summarizer..."
    )
```

**READ THE DESIGN:** One focused tool with a precise description.
**WHY CORRECT:** The tool description tells the LLM exactly when to use it. One tool = no ambiguity about tool selection.
**The Rule:** Give agents the minimum tools they need. Add more only when you observe them failing.

---

### Design Pattern 3: Correct — "Split agents on different skills"

```python
# Task: Research a topic then write an article
# Design decision: 2 agents — research ≠ writing
def content_pipeline(topic: str) -> str:
    research = run_agent(
        f"Research: {topic}",
        tools=[search_tool, arxiv_tool],         # ← retrieval tools
        system="You are a thorough researcher..."
    )
    article = run_agent(
        f"Write article from:\n{research}",
        tools=[format_tool],                     # ← formatting tool
        system="You are an engaging writer..."
    )
    return article
```

**READ THE DESIGN:** Two agents with genuinely different tools and personas.
**WHY CORRECT:** Research needs search tools. Writing needs formatting tools. Combining them in one agent would confuse tool selection. Separating them gives each focused context.
**The Rule:** Split agents when tasks need different tool sets OR when one task's quality depends on the other completing first.

---

### Design Pattern 4: Design Smell — "Agent when not needed"

```python
# User asks: "Format this list: ['a', 'b', 'c']"
# BAD design:
def format_list_agent(items: list) -> str:
    return run_agent(
        f"Format this as bullet points: {items}",
        tools=[format_tool],
        max_iterations=5
    )
# ↑ UNNECESSARY AGENT — 3-5 API calls for a trivial formatting task

# GOOD design:
def format_list(items: list) -> str:
    return "\n".join(f"• {item}" for item in items)
# ↑ Zero API calls — pure Python
```

**READ THE DESIGN SMELL:** An agent loop for something that doesn't require LLM reasoning.
**THE FIX:** If the output is deterministic and the logic is simple — write Python, not an agent.
**The Rule:** Agents are for tasks that require reasoning, research, or multi-step decisions. Not for formatting.

---

### Design Pattern 5: Design Smell — "Too many agents for simple pipeline"

```python
# BAD design: 5 agents for a task one could handle
preprocessor_agent = run_agent(raw_input, ...)
classifier_agent   = run_agent(preprocessed, ...)
researcher_agent   = run_agent(classified, ...)
synthesizer_agent  = run_agent(researched, ...)
formatter_agent    = run_agent(synthesized, ...)

# GOOD design: 2 agents (research is complex; format+synthesize is simple)
research    = run_agent(raw_input, tools=[search_tool], system="Research...")
final       = run_agent(research, tools=[format_tool], system="Synthesize and format...")
```

**READ THE DESIGN SMELL:** Every step is its own agent even for trivial transforms.
**THE FIX:** Only split into separate agents when the task genuinely needs different tools or context. Preprocessing and formatting rarely need their own agent.
**The Rule:** Start with one agent. Add agents when you observe specific failures that specialization would fix.

---

### Design Pattern 6: Correct — "Guardrails at every boundary"

```python
def safe_agent_pipeline(user_input: str) -> dict:

    # GUARDRAIL 1: Input validation (before any LLM call)
    if not validate_query(user_input):
        return {"error": "Invalid query", "status": "rejected"}

    # GUARDRAIL 2: Agent with loop cap (prevent infinite loops)
    result = run_agent_safe(user_input, max_iterations=15)
    if result["status"] == "limit_reached":
        return {"error": "Processing limit reached", "status": "timeout"}

    # GUARDRAIL 3: Output validation (quality gate before returning)
    gate = quality_gate(user_input, result["answer"])
    if not gate.passes:
        if gate.action == "retry":
            result = run_agent_safe(user_input, max_iterations=10)
        else:
            return {"error": "Quality gate failed", "status": "escalate"}

    return {"answer": result["answer"], "status": "complete"}
```

**READ THE DESIGN:** Three guardrail points — input, loop cap, output.
**WHY CORRECT:** Agents can fail at three points: invalid input, infinite loop, bad output. This design handles all three.
**The Rule:** Every production agent needs all three guardrails.

---

### Design Pattern 7: Correct — "System prompt as design document"

```python
SYSTEM_PROMPT = """
You are a Customer Research Specialist for an enterprise software company.

YOUR ROLE:
- Gather accurate information about customer needs and market trends
- Synthesize findings into actionable insights

YOUR TOOLS:
- search_web: Use for finding current market data and news
- search_crm: Use for finding existing customer data

CONSTRAINTS:
- Never fabricate statistics or data
- If confidence is below 0.7, always state your uncertainty
- Limit searches to 5 per session to control costs

OUTPUT FORMAT:
Return findings as a structured report with:
  1. Executive Summary (2-3 sentences)
  2. Key Findings (bullet points)
  3. Confidence Level (0.0-1.0)
  4. Data Sources
"""
```

**READ THE DESIGN:** Role + tools + constraints + output format all specified.
**WHY CORRECT:** A well-designed system prompt is a specification. The agent's behavior is predictable and testable.
**The Rule:** Your system prompt should be good enough that a human could follow it. If it's vague, your agent will be vague.

---

### Design Pattern 8: The "When to Use Agents" Checklist

```python
# SHOULD this be an agent? Check each question:

task = "What is RAG?"                   # Pure knowledge → NO agent needed
task = "Search for today's AI news"     # Needs current info → YES (search tool)
task = "Format this JSON"               # Deterministic → NO agent needed
task = "Research and write a report"    # Multi-step reasoning → YES (agent)
task = "Translate this text"            # Model already knows → NO agent needed
task = "Plan a 10-step project"         # Complex reasoning → YES (agent)
task = "Extract name from this text"    # Single extraction → Maybe (structured output, no loop)
task = "Monitor API and alert on issues"# Ongoing decision loop → YES (agent)

# THE TEST: Does this task require:
#   a) Information the model doesn't have? → needs tools → needs loop
#   b) Multi-step reasoning where each step depends on the last? → needs loop
#   c) Decisions that change based on runtime conditions? → needs loop
# If none of the above → single LLM call is enough.
```

---

## Design Decision Reference

| Decision | Bad (design smell) | Good (right design) |
|:---------|:-------------------|:--------------------|
| Use agent | Agent for formatting | Agent for research + decisions |
| Tool count | 10+ tools in one agent | 3-5 focused tools |
| System prompt | "Be helpful" | Role + tools + constraints + format |
| Agent count | 6 agents for simple pipeline | 1-2 agents, split by skill |
| Guardrails | No input/output checks | Validate input + cap loop + gate output |
| Memory | Same history for all users | Per-user session history |
| Loop cap | `while True` with no limit | `while iteration < max_iter` |

---

## You've Completed Pass 1!

You can now:
✓ **Spot** when an agent loop is unnecessary (overkill)
✓ **Count** tools and identify over-tooled agents
✓ **Read** system prompts as design documents
✓ **Recognize** guardrail placement (input + loop cap + output)
✓ **See** when specialization is warranted vs. premature
✓ **Evaluate** whether a task needs an agent at all

**Next:**
- **Pass C (Visual):** Decision trees for agentic system design
- **Pass 3 (Templates):** Thinking frameworks and design checklists
