# The Vibe Coder's Field Manual
## The Missing Layer: How to Actually Work WITH AI Every Day

**What the curriculum teaches:** How to READ code and ARCHITECT systems.
**What this document teaches:** How to DIRECT AI to produce what you designed.

This is the craft nobody taught you — because until 2025, it didn't exist.

---

## The Core Insight Most People Miss

Vibe coding is NOT "prompting." Prompting is a single message.
Vibe coding is **session architecture** — you're designing a CONVERSATION
that produces a SYSTEM.

Think about the difference:

```
Prompting:     One message  → One output
Vibe Coding:   Designed session → Evolving system
```

Your conversation with the AI is itself a system you're engineering.
The messages you send, the order, what context you include, when you
reset — these are ARCHITECTURAL DECISIONS, just like choosing between
a sequential pipeline and a parallel one (L17).

---

## THE SPECIFICATION SPECTRUM

Most people think vibe coding has two modes: vague vibes or precise specs.
Actually there are five levels, and the skill is knowing WHERE to operate.

```
Level 0: VIBES
  "Make me a nice dashboard"
  → When to use: NEVER in production. Only for initial exploration.
  → Problem: AI fills in every decision. You get generic output.

Level 1: FEATURES
  "Make a dashboard with a sidebar, search bar, and three chart panels"
  → When to use: Early design phase. Exploring layout and structure.
  → Problem: You specified WHAT, not HOW it should behave.

Level 2: BEHAVIOR
  "The search bar filters results as the user types. Show autocomplete
   suggestions after 300ms. Charts update when a date range is selected."
  → When to use: Building interactive components. Refining UX.
  → Strength: AI knows enough to make good implementation choices.

Level 3: CONTRACT
  "Input: user_query (str), filters (dict with keys 'date_range',
   'category'). Output: list of dicts with keys 'title', 'score',
   'source'. Max 10 items. Score is float 0.0-1.0."
  → When to use: Building tool interfaces, API contracts, data pipelines.
  → This is YOUR SWEET SPOT as an AI Architect.
  → Connects directly to: L05, Phase 3 L01-L02, L16 (DSPy signatures)

Level 4: TEST CASES
  "Given query='python loops', return items where score > 0.8.
   Given query='nonexistent_topic', return empty list.
   Given query='' (empty), raise ValueError."
  → When to use: Critical logic, edge cases, validation code.
  → Connects to: L03 (logic gates), L13 (tool schemas)
```

### THE RULE:

**Start at the HIGHEST level that matches your certainty.**

Don't know what you want? → Level 1 (features)
Know what it should do? → Level 2 (behavior)
Know the interface? → Level 3 (contract)  ← default here most of the time
Know the edge cases? → Level 4 (test cases)

**Never stay at Level 0.** Every Level 0 prompt is architectural debt.

---

## THE FIVE MODES OF VIBE CODING

Every vibe coding session falls into one of five modes.
Recognizing which mode you're in determines your technique.

### MODE 1: EXPLORATION
> "I don't know what I want yet"

**When:** Starting a new project, researching possibilities, brainstorming.

**Technique: The Scaffold Request**
```
"Show me 3 different approaches to [problem].
For each approach:
- Show the high-level architecture (components only, no code)
- List the trade-offs
- Tell me when I'd choose this over the others"
```

**Why this works:** You're NOT asking for code. You're asking for
ARCHITECTURAL OPTIONS. You make the decision, then go deeper.

**Anti-pattern:**
```
"Build me a RAG system"  ← Level 0, you'll get generic output
```

**Template (steal this):**
```
"I need to [goal]. My constraints are [X, Y, Z].
Show me the architectural options before writing any code.
For each, explain what I'd gain and what I'd lose."
```

---

### MODE 2: SPECIFICATION
> "I know exactly what I want"

**When:** You've made your architectural decisions, time to build.

**Technique: The Constraint Sandwich**

This is the most powerful pattern in vibe coding. Structure every
request in three layers:

```
LAYER 1 — CONSTRAINTS (before the request)
"Use Pydantic for all data models. Follow the conversation_history
template pattern from my curriculum. No external dependencies beyond
the standard library and pydantic."

LAYER 2 — THE REQUEST
"Build a conversation memory manager that stores messages,
enforces a token budget of 4096, and drops oldest messages
when the budget is exceeded."

LAYER 3 — VALIDATION (after the request)
"The output should:
- Pass mypy type checking
- Handle empty conversation history
- Never exceed the token budget
- Return the number of messages dropped"
```

**Why this works:** Layer 1 prevents AI from making decisions you've
already made. Layer 3 gives you a checklist to evaluate the output.
The AI is boxed in to doing exactly what you need.

**Connects to curriculum:**
- Layer 1 = your templates (L01-L02 patterns)
- Layer 2 = your architecture (L14 memory, L05 functions)
- Layer 3 = your quality gates (L03 logic, Phase 3 L02 Pydantic)

---

### MODE 3: ITERATION
> "It's close, let me refine"

**When:** AI produced something 70-80% right. Needs adjustment.

**Technique: The Surgical Edit**

Most people make this mistake:
```
BAD:  "That's not quite right, can you fix it?"
      → AI rewrites EVERYTHING, often losing what was good
```

Instead, be surgical:
```
GOOD: "Keep everything the same, but change ONLY the
       filter_documents function to use .get('score', 0.0)
       instead of ['score'] for missing key safety."
```

**The Rule of Surgical Edits:**
1. Name the EXACT function/section to change
2. Describe WHAT to change and WHAT to keep
3. Explain WHY (so AI doesn't "helpfully" change related things)

**Advanced technique: The Diff Request**
```
"Show me ONLY the lines that changed, with 2 lines of
context above and below. Don't regenerate the full file."
```

This forces AI to think about minimal changes instead of rewriting.

---

### MODE 4: DEBUGGING
> "Something's wrong"

**When:** Code runs but produces wrong results, or errors occur.

**Technique: The Evidence Package**

Never send just the error. Send the full diagnostic:

```
"I'm running [file name] and getting this error:

[paste the FULL traceback — see L09]

Here's what I expected to happen:
[describe expected behavior]

Here's what actually happened:
[describe actual behavior]

Here's the relevant code section:
[paste ONLY the relevant function, not the whole file]"
```

**Why this works:** You're doing Pass 2 (Evaluation) from the
3-Pass Method in real time. You identified the gap between
expected and actual. AI can target the fix precisely.

**Connects to curriculum:**
- L09: Error Reading (read the traceback yourself FIRST)
- L12: Advanced Debugging (silent failures, print audits)
- L03: Logic Gates (check if conditions are wrong)

**Anti-pattern:**
```
"It's broken, fix it" ← AI will guess what's wrong and often guess wrong
```

---

### MODE 5: INTEGRATION
> "Combine these pieces into a system"

**When:** You have individual components, need to wire them together.

**Technique: The Assembly Spec**

```
"I have three components:
1. search_tool (takes query: str, returns list of docs)
2. memory_manager (takes messages: list, returns trimmed messages)
3. response_generator (takes context: str, query: str, returns answer)

Wire them together so that:
- User query goes to search_tool AND memory_manager
- Results from both feed into response_generator
- The response is added to memory_manager for next turn

Use the pipeline pattern (sequential with merge).
Each component is already built — just write the orchestration."
```

**Connects to curriculum:**
- L17: Multi-Agent Patterns (sequential, parallel, conditional)
- L05: Functions as Tools (each component is a function)
- L15: ReAct (if the integration needs a reasoning loop)

---

## NOVEL CONCEPT: PROMPT DEBT

Like technical debt, but for vibe coding.

**Prompt debt** accumulates when you accept vague, "good enough" outputs
without specifying contracts. Each vague acceptance is a debt:

```
Turn 1: "Build me a search function"
  → AI picks parameter names, return format, error handling
  → You say "looks good" without reviewing
  → DEBT: You don't know the contract

Turn 5: "Now connect search to the memory manager"
  → AI's search returns dicts with "text" key
  → Memory manager expects "content" key
  → CRASH — debt comes due

Turn 8: "Why doesn't anything work together?"
  → Because you never specified the contracts
  → Now you're refactoring everything
  → INTEREST on the debt
```

**How to stay debt-free:**
After every AI output, do a 30-second contract check:
1. What are the input types?
2. What are the output types?
3. What happens on error?

If you can't answer all three, you've taken on debt.

---

## NOVEL CONCEPT: THE THREE AUDIENCES

When you write a vibe coding prompt, you're writing for three audiences:

**Audience 1: The AI (right now)**
→ Needs: Clear constraints, specific request, validation criteria
→ This is what most people optimize for

**Audience 2: You (in 10 minutes)**
→ Needs: To be able to REVIEW what the AI produced
→ So include: "Add comments explaining each section"
→ And: "Use descriptive variable names from AI domain"

**Audience 3: The next session (tomorrow)**
→ Needs: To understand the CONTEXT of what was built
→ So include: "Add a docstring at the top explaining what this
   module does and how it connects to the rest of the system"
→ And: Keep a running ARCHITECTURE.md file

**Most people only write for Audience 1.** That's why they lose track
of their own projects after three sessions.

---

## NOVEL CONCEPT: SESSION ARCHITECTURE

A vibe coding session is a system with its own architecture.
Design it intentionally.

### The Session Blueprint

```
PHASE 1: ORIENT (2 min)
  "Here's what I'm building: [one paragraph context]
   Here's what's already done: [list components]
   Here's what I need today: [specific goal]
   Here are my constraints: [patterns, templates, rules]"

PHASE 2: BUILD (variable)
  Alternate between Mode 2 (specification) and Mode 3 (iteration)
  Use the Constraint Sandwich for each request

PHASE 3: CHECKPOINT (5 min, every 30 min of building)
  "Show me the current state of the system.
   List all functions/classes with their input → output contracts.
   Flag anything that doesn't connect cleanly."

PHASE 4: CLOSE (3 min)
  "Summarize what we built today.
   List any unfinished items or known issues.
   Write an ARCHITECTURE.md entry I can use to resume tomorrow."
```

### Why Checkpoints Matter

Without checkpoints, here's what happens:

```
Minute 0:   Clear mental model
Minute 30:  "I think I remember what each part does"
Minute 60:  "Wait, which function handles the filtering?"
Minute 90:  "I've lost track of the whole system"
Minute 120: "Let me start over" ← catastrophic reset
```

With checkpoints every 30 minutes:

```
Minute 0:   Clear mental model
Minute 30:  CHECKPOINT → mental model refreshed
Minute 60:  CHECKPOINT → mental model refreshed
Minute 90:  CHECKPOINT → still in control
Minute 120: Shipping, not resetting
```

**The checkpoint prompt:**
```
"Pause. Give me a system map:
 - Every function/class we've built
 - What each takes in and returns
 - How they connect
 - What's left to build"
```

---

## NOVEL CONCEPT: TEMPLATE INJECTION

This is the bridge between your curriculum templates and vibe coding.

Instead of letting AI generate code in its own style, INJECT your templates:

```
"Generate a function to filter RAG search results.
Follow this EXACT pattern:

[paste template_filter_collection.py from your curriculum]

Modify it to:
- Add a 'recency' filter (documents from last 7 days only)
- Add a 'source_type' filter (only 'arxiv' and 'pubmed')
- Keep the same function signature and return format"
```

**Why this is powerful:**
1. AI matches YOUR style, not generic style
2. Output is recognizable — you can review it using patterns you know
3. Consistency across your whole project
4. Connects to curriculum: the Directory.md "Method 3: Template-First Approach"

**The Template Injection Workflow:**
```
1. Find closest template in your curriculum
2. Paste it into your prompt as the pattern to follow
3. Specify ONLY what to change
4. Review output against original template for drift
```

---

## NOVEL CONCEPT: THE GOOD ENOUGH THRESHOLD

Perfection is the enemy of shipping. But "good enough" is dangerous
without a definition.

**Define "good enough" BEFORE you start building:**

```
For a prototype:
  ✅ It runs without errors
  ✅ It handles the happy path
  ✅ It has clear function names
  ❌ Don't need: error handling, edge cases, optimization

For a working system:
  ✅ Everything above
  ✅ Handles common errors gracefully
  ✅ Has Pydantic validation on inputs
  ✅ Has basic logging
  ❌ Don't need: 100% test coverage, performance optimization

For production:
  ✅ Everything above
  ✅ Handles ALL edge cases
  ✅ Has monitoring and alerting
  ✅ Has documentation
  ✅ Passes security review
```

**The anti-pattern:** Spending 2 hours perfecting error handling
on a prototype you might throw away tomorrow.

**The rule:** Decide the tier BEFORE you start. Tell the AI:
```
"This is a prototype. Handle the happy path only.
Skip error handling except for API call failures.
Use print() for debugging, not logging."
```

---

## THE VIBE CODER'S DAILY PRACTICE

### Before You Start (2 minutes)

1. **State your goal** in one sentence (write it down)
2. **Identify the mode** you'll be in (exploration/specification/iteration/debugging/integration)
3. **Choose your specification level** (1-4)
4. **Open your templates** folder for injection

### While You Work

1. **Constraint Sandwich** every request
2. **Surgical edits** over full rewrites
3. **Checkpoint** every 30 minutes
4. **Contract check** every AI output (input types? output types? error behavior?)
5. **Template inject** when starting new components

### Before You Close (3 minutes)

1. Ask AI to generate a **session summary**
2. Update your **ARCHITECTURE.md**
3. Note any **prompt debt** you've taken on
4. List **tomorrow's first task** (so you can Orient fast)

---

## HOW THIS CONNECTS TO THE REVISED CURRICULUM MAP

The Vibe Coder's Field Manual is the PRACTICE layer that sits on top
of the four tiers:

```
┌─────────────────────────────────────────────┐
│     VIBE CODING PRACTICE (this document)     │
│  Session architecture, specification levels,  │
│  constraint sandwiches, template injection    │
├─────────────────────────────────────────────┤
│  TIER 1: Permanent Skills                     │
│  Data contracts, tool interfaces, quality     │
│  gates, declarative thinking                  │
│  → These power your SPECIFICATION MODE        │
├─────────────────────────────────────────────┤
│  TIER 2: Architectural Concepts               │
│  Memory, ReAct, multi-agent, RAG             │
│  → These power your EXPLORATION MODE          │
├─────────────────────────────────────────────┤
│  TIER 3: Reading Literacy                     │
│  Loops, classes, imports, debugging           │
│  → These power your DEBUGGING MODE            │
├─────────────────────────────────────────────┤
│  TIER 4: Reference Shelf                      │
│  Framework-specific patterns                  │
│  → These power your INTEGRATION MODE          │
└─────────────────────────────────────────────┘
```

**The curriculum gives you the KNOWLEDGE.**
**This manual gives you the PRACTICE.**
**Together they make you an AI Architect who ships.**

### 2026 Addition: Phase 5 in the Map

```
┌─────────────────────────────────────────────┐
│     VIBE CODING PRACTICE (this document)     │
├─────────────────────────────────────────────┤
│  PHASE 6: Anthropic Agent SDK               │
│  claude_agent_sdk, Managed Agents, sessions │
│  → Powers: SPECIFICATION + INTEGRATION modes│
│  → Key skill: Tool description as interface │
├─────────────────────────────────────────────┤
│  PHASE 5: Agentic AI (Ph4-L02–L08)              │
│  Raw loop anatomy, MCP, multi-agent         │
│  → Powers: DEBUGGING + EXPLORATION modes    │
├─────────────────────────────────────────────┤
│  PHASE 4: Tool Use & Schemas                │
│  Type hints, Pydantic, function calling     │
│  → Powers: SPECIFICATION mode (contracts)   │
├─────────────────────────────────────────────┤
│  PHASE 1: Foundation (L01–L21)              │
│  Data, logic, loops, functions, classes     │
│  → Powers: reading and reviewing ALL code   │
└─────────────────────────────────────────────┘
```

The tree now also has Phases 6–9 (`06-Phase06_Async`, `07-Phase07_Evals`, `08-Phase08_Debugging`, `09-Phase09_End_to_End_Projects`) and the `99-Vibe_Coding_Companion/` folder, which turns every template in the course into a worked vibe-coding prompt using the techniques in this manual. Start at `99-Vibe_Coding_Companion/README.md` for worked examples.

---

## PHASE 6 VIBE CODING GUIDE — Agent SDK Specific Patterns

The Agent SDK introduces new surfaces where prompt quality matters most.
Apply the Field Manual techniques to each of them.

### Constraint Sandwich for Tool Definitions (Ph5-L02)

The tool description is your highest-leverage vibe coding output.
A bad description wastes every token the LLM spends guessing.

```
CONSTRAINTS:
"Write a Tool() object following the Ph5-L02 pattern.
Description must answer three questions in 1-3 sentences:
(1) What does it do? (2) When should the LLM call it?
(3) When should it NOT call it?"

REQUEST:
"Build a tool that searches a knowledge base for AI/ML concepts."

VALIDATION:
"The description should allow the LLM to correctly decide:
- Call it for: 'What is RAG?', 'Explain MCP'
- Don't call it for: 'Calculate 15% of 240', 'Count words in this text'
If the LLM would be confused — rewrite the description."
```

**Prompt Debt signal:** If you accept a tool description that says only
"searches things" → you've taken on debt. The LLM WILL call it wrong.

---

### Surgical Edit for Session Memory (Ph5-L04)

When iterating on a multi-turn agent, don't regenerate the whole agent.

```
SURGICAL EDIT PROMPT:
"Keep the entire agent exactly as written.
Change ONLY the chat() function to accept a ConversationState object
instead of a raw session_id string.
The state should hold: session_id, turn_count, and last_intent.
Don't change any other function signatures."
```

---

### Assembly Spec for Two-Agent Pipelines (Ph5-L05)

When wiring a pipeline, give AI the full contract before asking it to build.

```
ASSEMBLY SPEC:
"I have two agents already built:
1. run_researcher(topic: str) → ResearchResult (topic, findings, sources)
2. run_writer(research: ResearchResult) → str (summary)

Wire them into a pipeline function research_and_write(topic: str) → str.
Rules:
- Researcher runs first, output goes directly to writer
- Print progress: '[1/2] Researching...' and '[2/2] Writing...'
- Return the writer's output string
- Do NOT change the signatures of either agent"
```

**Key discipline:** Specify the EXISTING contracts before asking AI to wire.
If you let AI guess the contracts, it will invent incompatible interfaces.

---

### Scaffold Request for Managed Agents (Ph5-L06)

When starting a Managed Agents integration, explore before committing.

```
SCAFFOLD REQUEST:
"I need to build a research assistant using Anthropic Managed Agents.
Show me 3 approaches — not code, just architecture:
1. Single agent, stateless sessions
2. Single agent, with memory_stores for user preferences
3. Two agents: planner and executor

For each:
- What are the setup steps?
- What runs per request?
- When would I choose this over the others?"
```

This prevents you from committing to the wrong tier (L06 vs L01-L05).

---

### Evidence Package for Agent Debugging

When an agent produces wrong answers or loops:

```
EVIDENCE PACKAGE:
"My agent is [describe wrong behavior].

Here is what I expected:
[expected output or behavior]

Here is what actually happened:
[actual output — paste the full response]

Here is the relevant code:
[paste ONLY the agent config and system prompt]

SPECIFIC QUESTION: Is the system prompt causing the LLM to [X]
when it should [Y]? If so, suggest the minimal change."
```

**Never say:** "My agent is broken, fix it."
**Always say:** "Here is expected vs actual. Here is the specific question."

---

## THE UPDATED 8-WEEK PLAN (with Vibe Coding Practice)

```
WEEK 1: Data Contracts + Mode 2 Practice
  Study: L01, L02
  Practice: Build 3 data schemas using Constraint Sandwich
  Vibe skill: Learn to specify at Level 3 (contract)

WEEK 2: Tool Interfaces + Template Injection
  Study: L05, L06 (core pattern), Phase 3 L01-L02
  Practice: Build 2 tool functions + 1 agent class using Template Injection
  Vibe skill: Inject curriculum templates into every prompt

WEEK 3: Quality Gates + Surgical Editing
  Study: L03, L13
  Practice: Add guardrails to Week 2's tools using Surgical Edits
  Vibe skill: Never rewrite what you can surgically edit

WEEK 4: Declarative Thinking + Session Architecture
  Study: L16, AI_Architect_Reading_Guide.md
  Practice: Build a complete DSPy-style pipeline in one session
  Vibe skill: Full session with Orient → Build → Checkpoint → Close

WEEK 5: System Design + Integration Mode
  Study: L14, L15
  Practice: Wire 3 components together using Assembly Spec
  Vibe skill: Integration mode with contract checking

WEEK 6: Multi-Agent + Exploration Mode
  Study: L17, RAG Pipeline files
  Practice: Design a 3-agent system using Scaffold Requests
  Vibe skill: Explore options before committing to architecture

WEEK 7: Reading Sprint + Debugging Mode
  Study: L04, L08, L09, OOP Advanced
  Practice: Debug 3 AI-generated code samples using Evidence Packages
  Vibe skill: Full debugging mode workflow

WEEK 8: Capstone Session
  Build: A complete system from scratch using ALL five modes
  Apply: Specification Spectrum, Constraint Sandwich, Session Architecture
  Deliver: Working system + ARCHITECTURE.md + template library additions

WEEK 9: Agent SDK — Specification Mode (Phase 5, L01–L03)
  Study: Ph5-L01 (SDK vs raw loop), Ph5-L02 (Tool definitions), Ph5-L03 (Streaming)
  Templates: template_first_sdk_agent.py, template_sdk_tools.py
  Practice: Build 2 Tool() objects using the Constraint Sandwich
  Vibe skill: Write tool descriptions that pass the LLM-decision test
  Outcome: You can direct AI to build correct SDK agents with well-defined tools

WEEK 10: Agent SDK — Integration Mode (Phase 5, L04–L06)
  Study: Ph5-L04 (Sessions), Ph5-L05 (Subagents), Ph5-L06 (Managed Agents)
  Templates: template_session_memory.py, template_subagent_pipeline.py
  Practice: Wire a two-agent pipeline using the Assembly Spec technique
  Vibe skill: Assembly Spec — specify contracts of existing components before wiring
  Capstone: Build a Managed Agent using the Scaffold Request technique to choose the right tier
  Outcome: You can architect and direct multi-agent SDK systems
```

---

## QUICK REFERENCE CARD

```
BEFORE EVERY PROMPT:
  □ What mode am I in? (explore/specify/iterate/debug/integrate)
  □ What specification level? (1-4)
  □ Do I have a template to inject?

THE CONSTRAINT SANDWICH:
  1. Constraints (what to follow, what to avoid)
  2. Request (what to build)
  3. Validation (how to verify)

THE 30-MIN CHECKPOINT:
  "Show me: every component, its contract, how they connect,
   what's left to build"

AFTER EVERY AI OUTPUT:
  □ What goes in? (input types)
  □ What comes out? (output types)
  □ What happens on error?
  □ Have I taken on prompt debt?

BEFORE CLOSING SESSION:
  □ Session summary generated
  □ ARCHITECTURE.md updated
  □ Tomorrow's first task noted

PHASE 6 ADDITIONS — Agent SDK specific:
  □ Tool description test: "Would the LLM know WHEN and WHEN NOT to call this?"
  □ Session contract: "Does each turn's output feed cleanly into the next turn's input?"
  □ Pipeline contract: "Does agent 1's output type match agent 2's expected input type?"
  □ Tier decision: "Is this agent loop, orchestration, or Managed Agents?" (Ph4-L07 + Ph5-L06)
  □ Failure path: "What does the agent do when a tool returns is_error=True?" (Ph4-L03 S8)
```

---

*This is Lesson 0.5 of the AI Architect curriculum.*
*It goes between "setup" and "data contracts."*
*Because the tool you'll use every day deserves its own lesson.*

---

## CROSS-REFERENCE MAP — Field Manual technique → Curriculum lesson

| When you're building... | Use technique | Study first |
|-------------------------|--------------|-------------|
| Data schemas (inputs/outputs) | Constraint Sandwich (Level 3) | L01, L02, Ph3-L02 |
| Tool functions | Template Injection + Constraint Sandwich | L05, Ph3-L01, Ph3-L02 |
| Logic gates / routing | Surgical Edit | L03, L13 |
| Agent with memory | Assembly Spec | L14, Ph5-L04 |
| Two-agent pipeline | Assembly Spec + Scaffold Request | L17, Ph5-L05 |
| SDK Tool() objects | Constraint Sandwich (description focus) | Ph5-L02 |
| Managed Agent | Scaffold Request → pick tier | Ph5-L06, Ph4-L07 |
| Anything broken | Evidence Package | L09, L12 |
| Starting something new | Scaffold Request | Ph4-L07 |

**The rule in one sentence:**  
Scaffold to explore → Constraint Sandwich to specify → Surgical Edit to refine → Evidence Package to debug → Assembly Spec to integrate.
