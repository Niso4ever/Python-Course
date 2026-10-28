# Lesson 21 - Pass C: VISUAL PATTERNS
## See Vibe Coding as a Communication Protocol

**Goal:** Understand how to architect perfect prompts through visual prompt structure, not just text.

---

## Visual 1: The Failed Prompt (Why Vibe Coding Fails)

### Bad Code Request:
```
"Build me a RAG chatbot"
```

### What the AI "Sees":
```
┌─────────────────────────────────────┐
│   VAGUE REQUEST                     │
│                                     │
│   Input: "Build RAG chatbot"       │
│                                     │
│   AI's Decision Tree:               │
│   ┌─────────────────────┐           │
│   │ Which framework?    │           │
│   │ ┌───┬───┬───┬───┐   │           │
│   │ │LC │LI │DSP│Raw│   │           │
│   │ └───┴───┴───┴───┘   │           │
│   │   ▲                 │           │
│   │   │ Picks most      │           │
│   │   │ common from     │           │
│   │   │ Reddit 2023 → LC│           │
│   └─────────────────────┘           │
│                                     │
│   Output: Messy LangChain code      │
│          (outdated, complex)        │
└─────────────────────────────────────┘
```

**Problem:** No constraints = AI defaults to convoluted, popular solutions

---

## Visual 2: The Perfect Architect Prompt (3-Part Structure)

### Good Code Request:
```
[CONTEXT] You are a senior AI engineer. I need a local RAG system.
[CONSTRAINTS] Use ONLY DSPy. No LangChain. Under 100 lines. Heavily commented.
[EXAMPLE] Follow this exact pattern: [paste template_dspy_rag.py]
```

### What the AI "Sees":
```
┌─────────────────────────────────────────────────────────┐
│   STRUCTURED REQUEST                                    │
│                                                         │
│   ┌──────────────┐                                      │
│   │ 1. CONTEXT   │  "Who am I? Senior AI engineer"     │
│   │ (Identity)   │  "What's the goal? Local RAG"       │
│   └──────┬───────┘                                      │
│          │                                              │
│          ▼                                              │
│   ┌──────────────┐                                      │
│   │ 2. CONSTRAINTS│ ┌──────────────────────────┐        │
│   │ (Rules)      │ │ ✓ DSPy only              │        │
│   │              │ │ ✗ NO LangChain          │        │
│   │              │ │ ✗ NO > 100 lines        │        │
│   │              │ │ ✓ MUST have comments    │        │
│   └──────┬───────┘ └──────────────────────────┘        │
│          │                                              │
│          ▼                                              │
│   ┌──────────────┐                                      │
│   │ 3. EXAMPLE   │  [Full template code]               │
│   │ (Template)   │  "Copy this exact shape"            │
│   └──────┬───────┘                                      │
│          │                                              │
│          ▼                                              │
│   ┌──────────────┐                                      │
│   │   OUTPUT     │  Perfect curriculum-aligned code    │
│   │              │  ✓ DSPy framework                   │
│   │              │  ✓ Under 100 lines                  │
│   │              │  ✓ Heavily commented                │
│   │              │  ✓ Matches template pattern         │
│   └──────────────┘                                      │
└─────────────────────────────────────────────────────────┘
```

**Key Insight:** AI doesn't invent → AI copies. Give it a blueprint.

---

## Visual 3: The "Manic Junior Developer" Mental Model

### Code:
```python
# Without constraints
AI = ManicJuniorDeveloper(
    speed="infinite",
    creativity="high",
    constraints=None  # ⚠️ DANGER
)

# Result: Bathroom built in kitchen
```

### Visual Mental Model:
```
┌─────────────────────────────────────────────────────┐
│     YOU (The Architect)                             │
│                                                     │
│     "Build me a user dashboard"                     │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  AI ASSISTANT (Manic Junior Dev)                    │
│                                                     │
│  Properties:                                        │
│  - Speed: ∞ (infinitely fast)                       │
│  - Intelligence: High                               │
│  - Creativity: High                                 │
│  - Following instructions: LITERAL                  │
│                                                     │
│  Without constraints:                               │
│  ┌─────────────────────────────────────┐            │
│  │ Searches entire internet             │            │
│  │ Finds most popular solution          │            │
│  │ Uses 17 dependencies                 │            │
│  │ Implements async/await everywhere    │            │
│  │ Adds caching, queues, microservices  │            │
│  │ = OVERENGINEERED MESS                │            │
│  └─────────────────────────────────────┘            │
│                                                     │
│  With constraints:                                  │
│  ┌─────────────────────────────────────┐            │
│  │ "Use ONLY Streamlit + Pandas"        │            │
│  │ "No databases, read from CSV"        │            │
│  │ "Keep it under 50 lines"             │            │
│  │ = EXACTLY WHAT YOU NEED              │            │
│  └─────────────────────────────────────┘            │
└─────────────────────────────────────────────────────┘
```

**Metaphor:** Brilliant but needs literal blueprints, or they'll build the bathroom in the kitchen.

---

## Visual 4: System Prompt Structure (Internal Agent Instructions)

### Code:
```python
SYSTEM_PROMPT = """
You are a customer support agent for Acme Corp.
CONSTRAINTS:
- Answer ONLY from the manual
- Do NOT guess
- CANNOT authorize refunds
"""
```

### Visual Flow:
```
User Query → Agent with Constraints → Safe Response

┌─────────────────────────────────────────────────┐
│  USER: "My coffee is cold, give me a refund!"  │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  AGENT (with system prompt constraints)         │
│                                                 │
│  ┌───────────────────────────────┐              │
│  │ Check constraint #1:          │              │
│  │ "Answer ONLY from manual"     │              │
│  │ → Manual found on pg 4        │ ✓            │
│  └───────────────────────────────┘              │
│                                                 │
│  ┌───────────────────────────────┐              │
│  │ Check constraint #2:          │              │
│  │ "Do NOT guess"                │              │
│  │ → Using manual reference      │ ✓            │
│  └───────────────────────────────┘              │
│                                                 │
│  ┌───────────────────────────────┐              │
│  │ Check constraint #3:          │              │
│  │ "CANNOT authorize refunds"    │              │
│  │ → User wants refund           │ ✗ BLOCKED    │
│  └───────────────────────────────┘              │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  RESPONSE:                                      │
│  "I'm sorry! Please check page 4 of the manual │
│   regarding the heating element. I cannot      │
│   authorize refunds."                          │
└─────────────────────────────────────────────────┘
```

**Without constraints:** Agent might say "Sure! Here's a full refund + free month!" 💸

---

## Visual 5: Agent Without Constraints (The Wild Card)

### Code:
```python
# DANGEROUS
SYSTEM_PROMPT = "You are helpful support"
```

### Visual Chaos:
```
┌─────────────────────────────────────────────────┐
│  AGENT WITHOUT CONSTRAINTS (Wild Card)          │
│                                                 │
│  User: "Give me a refund"                       │
│                                                 │
│  Agent's decision tree:                         │
│  ┌─────────────────────────────────┐            │
│  │ Should I give refund?           │            │
│  │                                 │            │
│  │ No constraints...               │            │
│  │ User seems unhappy...           │            │
│  │ Being helpful means yes?        │            │
│  │                                 │            │
│  │ ✓ "Sure! Full refund granted!"  │ 💸💸💸      │
│  └─────────────────────────────────┘            │
│                                                 │
│  User: "Can I get next month free?"             │
│                                                 │
│  Agent:                                         │
│  ┌─────────────────────────────────┐            │
│  │ No one said I can't...          │            │
│  │ ✓ "Absolutely! Free month!"      │ 💸💸💸      │
│  └─────────────────────────────────┘            │
│                                                 │
│  RESULT: Company bankrupt in 3 days             │
└─────────────────────────────────────────────────┘
```

**Key Pattern:** Constraints transform wild cards into deterministic functions.

---

## Visual 6: The 3-Pass Prompt Pattern

### Context → Constraints → Examples

```
┌─────────────────────────────────────────────────────┐
│  STEP 1: CONTEXT (Who & What)                       │
│  ┌───────────────────────────────────────┐          │
│  │ "You are a senior AI engineer"        │          │
│  │ "I need a weather API tool"           │          │
│  └───────────────────────────────────────┘          │
│                   │                                 │
│                   ▼                                 │
│  STEP 2: CONSTRAINTS (Rules & Limits)               │
│  ┌───────────────────────────────────────┐          │
│  │ ✗ NO async code                       │          │
│  │ ✗ NO external libraries except requests│         │
│  │ ✓ MUST handle network errors          │          │
│  │ ✓ MUST return JSON                    │          │
│  │ ✓ Under 40 lines                      │          │
│  └───────────────────────────────────────┘          │
│                   │                                 │
│                   ▼                                 │
│  STEP 3: EXAMPLE (Template to Copy)                │
│  ┌───────────────────────────────────────┐          │
│  │ def weather_api(city: str) -> dict:   │          │
│  │     try:                               │          │
│  │         response = requests.get(...)   │          │
│  │         return response.json()         │          │
│  │     except RequestException:           │          │
│  │         return {"error": "..."}        │          │
│  └───────────────────────────────────────┘          │
│                   │                                 │
│                   ▼                                 │
│  ┌───────────────────────────────────────┐          │
│  │  OUTPUT: Perfect curriculum code       │          │
│  └───────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

**Pattern Recognition:** This is the same as `INPUT → PROCESSING → OUTPUT` from L03 Logic Gates!

---

## Visual 7: Template-First vs Theory-First (Speed Comparison)

### Theory-First (Slow):
```
┌────────────────────────────────────────┐
│  YOU: "Explain how DSPy works"         │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│  AI: [500 word essay about DSPy]       │
│      [Examples from docs]              │
│      [Conceptual overview]             │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│  YOU: "Now write code for me"          │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│  AI: [Generic code, might not match]   │
└───────────────┬────────────────────────┘
                │
                ▼
        Time: 10-20 minutes
        Quality: Hit or miss
```

### Template-First (Fast):
```
┌────────────────────────────────────────┐
│  YOU: "Copy this template_dspy.py      │
│        Add weather search capability"  │
│        [pastes template]               │
└───────────────┬────────────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│  AI: [Perfect code in 30 seconds]      │
│       [Exact template structure]       │
│       [Weather tool added]             │
└────────────────────────────────────────┘
                │
                ▼
        Time: 1 minute
        Quality: Perfect on first try
```

**Speed Multiplier:** Template-first is 10-20x faster

---

## Visual 8: Copy > Invent (The Core Truth)

### What AI Is Good At:

```
┌─────────────────────────────────────────┐
│  AI CAPABILITIES                        │
│                                         │
│  Copying patterns:     ████████████ 95% │
│  Inventing patterns:   ██          15%  │
│                                         │
│  With template:        ████████████ 95% │
│  Without template:     ████            35% │
└─────────────────────────────────────────┘
```

### The Visual Rule:

```
    GIVE TEMPLATE           AI COPIES PERFECTLY
         │                         │
         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐
│ template_api.py │  →    │ your_weather.py │
│                 │       │                 │
│ def api_call(): │       │ def weather():  │
│   try:          │       │   try:          │
│     ...         │       │     ...         │
│   except:       │       │   except:       │
│     ...         │       │     ...         │
└─────────────────┘       └─────────────────┘
    Shape = Same              Shape = Same
```

**Insight:** AI is a pattern copier, not a pattern inventor. Use this.

---

## Visual 9: The Prompt Builder Class (From Template)

### Code Flow:
```python
builder = PromptBuilder("Summarization Expert")
builder.add_constraint("Exactly 3 bullet points")
builder.add_constraint("No word 'therefore'")
builder.add_example(input="...", output="...")
final_prompt = builder.build_prompt()
```

### Visual Construction:
```
┌────────────────────────────────────────────────┐
│  PROMPT BUILDER MACHINE                        │
│                                                │
│  1. Initialize:                                │
│     ┌────────────────────┐                     │
│     │ Role: "Summarizer" │                     │
│     │ Constraints: []    │                     │
│     │ Examples: []       │                     │
│     └────────────────────┘                     │
│              │                                 │
│              ▼                                 │
│  2. Add Constraint:                            │
│     ┌────────────────────┐                     │
│     │ Constraints:       │                     │
│     │  [1] 3 bullets     │                     │
│     │  [2] No "therefore"│                     │
│     └────────────────────┘                     │
│              │                                 │
│              ▼                                 │
│  3. Add Example:                               │
│     ┌────────────────────┐                     │
│     │ Examples:          │                     │
│     │  [1] Q: ... A: ... │                     │
│     └────────────────────┘                     │
│              │                                 │
│              ▼                                 │
│  4. Build (Assemble):                          │
│     ┌────────────────────────────────┐         │
│     │ [ROLE]                         │         │
│     │ You are a Summarizer           │         │
│     │                                │         │
│     │ [CONSTRAINTS]                  │         │
│     │ - Exactly 3 bullet points      │         │
│     │ - No word "therefore"          │         │
│     │                                │         │
│     │ [EXAMPLES]                     │         │
│     │ Q: ... A: ...                  │         │
│     └────────────────────────────────┘         │
│              │                                 │
│              ▼                                 │
│     Final assembled prompt string              │
└────────────────────────────────────────────────┘
```

**Pattern:** Builder pattern (from L06 Classes) for dynamic prompt construction

---

## Visual 10: Architect Workflow (Why This Matters)

### Traditional Developer:
```
Write code → Debug syntax → Test → Fix bugs → Deploy
│            │               │       │
▼            ▼               ▼       ▼
[Manual]   [Manual]       [Manual] [Manual]

Time: Days
```

### Vibe-Coding Architect:
```
Design system → Give AI template → Review → Deploy
│               │                   │
▼               ▼                   ▼
[Think]      [AI writes]         [Quick check]

Time: Hours (10x faster)
```

### Visual Comparison:
```
┌────────────────────────────────────────┐
│  TRADITIONAL DEV                       │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐             │
│  │ 1│→│ 2│→│ 3│→│ 4│→│ 5│             │
│  └──┘ └──┘ └──┘ └──┘ └──┘             │
│  Write Debug Test Fix Deploy           │
│                                        │
│  Time: ████████████████████ (100%)     │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│  VIBE-CODING ARCHITECT                 │
│  ┌──┐ ┌────────┐ ┌──┐ ┌──┐             │
│  │ 1│→│ AI CODE│→│ 3│→│ 4│             │
│  └──┘ └────────┘ └──┘ └──┘             │
│  Design  (AI)   Review Deploy          │
│                                        │
│  Time: ██████ (10% of traditional)     │
└────────────────────────────────────────┘
```

**Why It Matters:** 10x speed boost when you master architect prompts

---

## Visual 11: The Copy-Paste Prompts (From CHEATSHEET_L21.py)

### Four Prompt Patterns:

```
┌─────────────────────────────────────────────────┐
│  PATTERN 1: Scaffold (Starting new script)      │
│  ┌───────────────────────────────────┐          │
│  │ [CONTEXT] Senior AI engineer...   │          │
│  │ [CONSTRAINTS] Use ONLY X, NO Y... │          │
│  │ [EXAMPLE] Structure like this...  │          │
│  └───────────────────────────────────┘          │
│  Use when: Starting from scratch                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  PATTERN 2: Clone Template                      │
│  ┌───────────────────────────────────┐          │
│  │ [CONTEXT] Need weather tool...    │          │
│  │ [CONSTRAINTS] Catch errors...     │          │
│  │ [EXAMPLE] <paste template_api.py> │          │
│  └───────────────────────────────────┘          │
│  Use when: Copying existing patterns            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  PATTERN 3: Debugging                           │
│  ┌───────────────────────────────────┐          │
│  │ [CONTEXT] Script crashing...      │          │
│  │ [CONSTRAINTS] Simplest fix...     │          │
│  │ [EXAMPLE] <paste error + code>    │          │
│  └───────────────────────────────────┘          │
│  Use when: Fixing errors                        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  PATTERN 4: Internal Agent System Prompt        │
│  ┌───────────────────────────────────┐          │
│  │ You are [role]                    │          │
│  │ CONSTRAINTS: [rules]              │          │
│  │ EXAMPLE INPUT: [...]              │          │
│  │ EXAMPLE OUTPUT: [...]             │          │
│  └───────────────────────────────────┘          │
│  Use when: Writing agent instructions           │
└─────────────────────────────────────────────────┘
```

---

## Visual 12: Deterministic Agent (With Constraints)

### Agent Behavior Transformation:

```
WITHOUT CONSTRAINTS:                 WITH CONSTRAINTS:
───────────────────                 ──────────────────

User Query                          User Query
    │                                   │
    ▼                                   ▼
┌──────────┐                        ┌──────────┐
│  Agent   │                        │  Agent   │
│          │                        │          │
│ Random   │                        │ Checks:  │
│ creative │                        │  ✓ Rule 1│
│ guessing │                        │  ✓ Rule 2│
│          │                        │  ✓ Rule 3│
└────┬─────┘                        └────┬─────┘
     │                                   │
     ▼                                   ▼
Unpredictable                       Predictable
output                              output
(hallucinations)                    (deterministic)

┌─────────────┐                     ┌─────────────┐
│ Could say   │                     │ Always says │
│ anything    │                     │ X when Y    │
└─────────────┘                     └─────────────┘
```

**Key Insight:** Constraints transform agents into deterministic functions

---

## Visual 13: The Context Triangle (Complete Prompt Ecosystem)

### Three Components Working Together:

```
┌─────────────────────────────────────────────────┐
│     PERFECT AI PROMPT ECOSYSTEM                 │
│                                                 │
│              1. CONTEXT                         │
│               (Identity)                        │
│                  ▲                              │
│                 ╱ ╲                             │
│                ╱   ╲                            │
│               ╱     ╲                           │
│              ╱       ╲                          │
│             ╱         ╲                         │
│            ╱           ╲                        │
│           ╱             ╲                       │
│          ╱               ╲                      │
│         ╱                 ╲                     │
│        ╱                   ╲                    │
│       ╱                     ╲                   │
│      ╱                       ╲                  │
│     ╱                         ╲                 │
│    ╱                           ╲                │
│   ╱                             ╲               │
│  ╱_______________________________╲              │
│ 2. CONSTRAINTS ←────────→ 3. EXAMPLES           │
│   (Rules)                  (Templates)          │
│                                                 │
│  All three required for perfect output          │
└─────────────────────────────────────────────────┘

Missing any corner = degraded output:
- No context = confused AI
- No constraints = messy code
- No example = wrong patterns
```

---

## Shape Comparison Chart

### Prompt Structures You'll See:

#### Bad Prompt (No Structure):
```
"Build me a chatbot"

Shape: ○
Single blob, no detail
Result: Garbage
```

---

#### Template-First Prompt:
```
[CONTEXT]
You are...

[CONSTRAINTS]
- Rule 1
- Rule 2
- Rule 3

[EXAMPLE]
<paste template>

Shape: ▭ → ≡ → ▭
Layers stacked
Result: Perfect
```

---

#### System Prompt:
```
You are [role]
CONSTRAINTS:
- Don't X
- Must Y
EXAMPLE:
Input → Output

Shape: ▭
       ≡
       ═
Constrained layers
Result: Deterministic
```

---

## Visual Recognition Exercise

Look at this prompt and identify the structure:

```
[CONTEXT] You are a Python expert helping with DSPy agents.
[CONSTRAINTS]
- Use ONLY DSPy framework
- No LangChain
- Keep under 50 lines
[EXAMPLE] Follow this pattern:
class Agent:
    def __init__(self):
        self.signature = dspy.Signature(...)
```

**Mental Image:**
```
Context box
    │
Constraint checklist
    │
Example template
    │
= Perfect 3-part prompt
```

---

## Color Coding Method (For Your Practice)

When reading prompts, mentally color them:

- **🔵 Blue** = Context (who/what)
- **🔴 Red** = Constraints (rules/limits)
- **🟢 Green** = Examples (templates)

```
🔵 [CONTEXT] You are a senior AI engineer.
🔴 [CONSTRAINTS] Do NOT use LangChain.
🟢 [EXAMPLE] Copy this: <template code>
```

---

## You've Completed Pass C!

You can now:
✓ **Visualize** the 3-part prompt structure (Context → Constraints → Examples)
✓ **See** why vibe coding fails (no constraints = AI defaults to Reddit 2023)
✓ **Understand** the "manic junior developer" mental model
✓ **Recognize** template-first vs theory-first (10x speed difference)
✓ **Build** deterministic agents with constrained system prompts

**Next:**
- **Practice:** Use the 4 copy-paste prompts from [CHEATSHEET_L21.py](CHEATSHEET_L21.py)
- **Build:** Create your own PromptBuilder for custom agents

**Remember:** When prompting AI — think Context (who), Constraints (rules), Examples (copy this).

---

## Pro Tip: The Architect's Speed Secret

Whenever you need AI to write code:
1. **Paste a template** from this curriculum (don't describe it)
2. **Forbid frameworks** you don't want (LangChain, async, etc.)
3. **Set line limits** (forces simplicity)

You don't need to explain everything. Just give the blueprint. The AI will copy it perfectly in seconds.

---

## The Hidden Truth

**AI coding assistants are not search engines.**

They are infinitely fast, brilliant developers who:
- ✓ Copy patterns perfectly
- ✗ Invent patterns poorly
- ✓ Follow constraints literally
- ✗ Make good decisions without rules

Treat them like junior developers who need blueprints, and you'll architect systems 10x faster than writing code manually.
