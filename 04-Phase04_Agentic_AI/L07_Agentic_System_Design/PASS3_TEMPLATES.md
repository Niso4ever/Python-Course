# Lesson 23 — Pass 3: DESIGN FRAMEWORKS
## Thinking Templates for Agentic System Design

> **These are not code templates.** These are thinking frameworks — structured questions you work through when designing or evaluating an agentic system. Use them when directing AI to build a system, or when reviewing AI-generated agent code.

---

## Framework 1: The System Design Brief
**Use when:** Starting a new agentic system from scratch

Copy this and fill it in before asking AI to write any code.

```
SYSTEM DESIGN BRIEF
===================

TASK:
  What does this system need to accomplish?
  [One sentence: "This system will..."]

USER:
  Who triggers this system and what do they provide as input?
  Input format: [text / structured data / file / API call]

OUTPUT:
  What does the system return and to whom?
  Output format: [text / dict / file / API response / action]

DECISION: Does this need an agent?
  [ ] YES — task requires real-time info, multi-step reasoning, or runtime decisions
  [ ] NO  — use single LLM call or pure Python

IF AGENT:
  Number of agents: [1 / 2 / 3 / explain why more]
  Tools needed (list the minimum):
    1.
    2.
    (max 5-6)

  System prompt (fill in):
    Role: "You are a [specific role]."
    Task: "Your job is to [specific task]."
    Constraints: "Always [constraint]. Never [constraint]."
    Output format: "Return [format description]."

GUARDRAILS:
  Input validation: [what to check before the agent runs]
  Loop cap: max_iterations = [N] (default: 15)
  Output gate: [what counts as an acceptable answer]

MEMORY:
  [ ] Stateless (each call starts fresh)
  [ ] Session (remembers within one conversation)
  [ ] Persistent (remembers across sessions, stored in DB)

EVALUATION:
  How will I know if this is working?
  Success = [measurable criterion]
  Failure = [what would make me re-design]
```

---

## Framework 2: The Tool Design Brief
**Use when:** Designing a tool for an agent

```
TOOL DESIGN BRIEF
=================

Tool name: [verb_noun format, e.g., "search_web", "calculate_cost"]

Description (what you'll write in the schema):
  "Use this tool when [specific trigger condition].
   This tool [what it does].
   Do NOT use this when [when NOT to use it]."

Input parameters:
  Required:
    - [param_name] (type): [what it means]
  Optional:
    - [param_name] (type, default: X): [what it means]

Output: [describe what the tool returns]

Safety check:
  [ ] Could the agent call this at the wrong time and cause damage?
  [ ] If YES: add "Do NOT use this when..." to the description

Python function signature:
  def [tool_name]([params]) -> str:
      ...  # AI will write this

Overlap check:
  [ ] Does this overlap with another tool in the same agent?
  [ ] If YES: merge them or differentiate the descriptions more clearly
```

---

## Framework 3: The Code Review Checklist
**Use when:** AI has written agent code — reviewing it before use

```
AGENTIC CODE REVIEW CHECKLIST
==============================

AGENT LOOP:
  [ ] Is there a loop cap? (max_iterations or for _ in range(N))
  [ ] Is the exit condition correct? (stop_reason == "end_turn")
  [ ] Are messages appended correctly? (assistant + user, in order)

TOOL DESIGN:
  [ ] Are there 7 or fewer tools per agent?
  [ ] Is each tool description specific about WHEN to use it?
  [ ] Are required vs. optional parameters correct?
  [ ] Are tool names clear verbs (search_web not "searcher")?

SYSTEM PROMPT:
  [ ] Does it specify role, task, constraints, and output format?
  [ ] Is it specific enough to be testable?

GUARDRAILS:
  [ ] Is user input validated before the agent runs?
  [ ] Is there a loop cap?
  [ ] Is there output validation or a quality gate?

MEMORY:
  [ ] What does messages start with? (blank / history / persistent context)
  [ ] Is history trimmed before it gets too long?

STRUCTURE:
  [ ] Is the agent doing something that doesn't need a loop? (design smell)
  [ ] Are there more agents than necessary? (complexity smell)
  [ ] Is there pure Python logic pretending to be an agent call? (waste)

COSTS:
  [ ] Is max_tokens set appropriately?
  [ ] Is max_iterations reasonable for the expected task complexity?
```

---

## Framework 4: The Prompt Engineering Brief
**Use when:** Writing a system prompt for a specialist agent

```
SYSTEM PROMPT STRUCTURE (fill in each section):

YOU ARE:
  "You are a [specific role] at [company type if relevant].
   You specialize in [specific domain]."

YOUR TASK:
  "Your job is to [specific task with clear scope]."

YOUR TOOLS:
  "You have access to:
   - [tool_name]: Use this when [specific trigger]
   - [tool_name]: Use this when [specific trigger]
   Do NOT use [tool_name] when [anti-use case]."

YOUR CONSTRAINTS:
  "Always [positive constraint].
   Never [negative constraint].
   If [edge case], then [fallback behavior]."

YOUR OUTPUT:
  "Return [specific format description].
   Include [required fields].
   Your response length should be [short/medium/detailed]."

EXAMPLE (for complex tasks):
  "For example, if asked [X], you should [Y]."
```

**Example filled-in:**
```
You are a Research Analyst specializing in AI technology trends.

Your task: Find accurate, current information using search tools and synthesize findings into actionable insights.

Your tools:
  - search_recent_news: Use this when the question asks about events in the last 30 days
  - search_papers: Use this when the question involves research, benchmarks, or technical details
  Do NOT use search tools for definitions the model already knows.

Your constraints:
  Always cite your search results. Never fabricate statistics.
  If confidence is below 0.7, state your uncertainty explicitly.

Your output: Return a 3-5 sentence summary followed by 3-5 bullet point key findings.
Include a confidence score (0.0-1.0) at the end.
```

---

## Framework 5: The Escalation Strategy
**Use when:** Deciding what the system does when it fails

```
ESCALATION LADDER
=================

Level 1: SELF-RETRY
  Trigger: Output quality gate score < threshold
  Action: Rerun the agent (max 2 retries)
  Code signal: if not gate.passes and gate.action == "retry": rerun()

Level 2: FALLBACK RESPONSE
  Trigger: Max retries reached OR max iterations hit
  Action: Return a partial answer + "I need more information to complete this"
  Code signal: return {"answer": partial, "status": "incomplete"}

Level 3: HUMAN ESCALATION
  Trigger: Harmful/sensitive content detected OR confidence < 0.3
  Action: Flag for human review, don't return to user
  Code signal: if gate.action == "escalate": return to_human_queue(request)

Level 4: SYSTEM HALT
  Trigger: Tool errors, API failures, unexpected exceptions
  Action: Log the error, return safe fallback message
  Code signal: except Exception as e: log(e); return SAFE_DEFAULT

DESIGN THIS BEFORE BUILDING — agents WILL fail. The question is how they fail.
```

---

## Framework 6: Pre-Prompt for Directing AI to Build Your Agent

Copy and fill this in when asking AI to build an agentic system for you.

```
Build an agentic AI system with the following specification:

TASK: [one sentence what it does]

INPUT: [what the user provides — text / dict / etc.]

OUTPUT: [what it returns — text / dict / etc.]

AGENTS:
  [Number] agent(s). If more than one:
  - Agent 1: [role] + [tools] + [system prompt intent]
  - Agent 2: [role] + [tools] + [system prompt intent]

TOOLS NEEDED:
  - [tool_name]: [description of what it does]
  - [tool_name]: [description of what it does]
  (provide real tool functions if you have them, or ask AI to write stubs)

GUARDRAILS:
  - Validate input: [what to check]
  - Max iterations: [N]
  - Output gate: [what passes]

MEMORY: [stateless / session / persistent]

DEMO MODE: Include a demo mode that runs without an API key.

STYLE: Use Anthropic SDK directly (import anthropic). No framework imports.
       Follow the Phase 4 patterns (while loop + stop_reason + execute_tools).
```

---

## Quick Reference: Design Rules for 2026

| Situation | Rule |
|:----------|:-----|
| Simple factual question | Single LLM call — no agent |
| Need real-time data | Agent + search tool |
| Deterministic transform | Pure Python — no LLM |
| Multi-step research | Agent loop |
| Different skill sets needed | Separate specialist agents |
| One agent, many tasks | Probably fine — don't over-split |
| More than 7 tools in one agent | Redesign — split tools across agents |
| System prompt is vague | Rewrite — role + task + constraints + format |
| No loop cap | Always add max_iterations |
| No output validation | Always add quality gate for production |
| Multi-turn chat | Session history — pass history each call |
| Cross-session memory | Persistent DB — load/save per user_id |
