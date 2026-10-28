# Vibe Coding — Best Practices & Guidelines (2026)

> **Who this is for:** the AI Architect who directs code instead of typing it.
> This is the *rulebook* that sits behind the answer-key in this folder. The
> templates show you the finished dishes; this file is how a 2026 kitchen runs.

---

## The metaphor for the whole job

> You are not the cook anymore. You are the **head chef**.
> You don't chop the onions — you taste the dish, send it back when it's wrong,
> and you are the one who answers to the customer when it's served.

The AI writes the code. **You own the outcome.** Every rule below comes from
that one shift in role.

---

## The 2026 landscape (what changed)

The models you're directing are not the ones the old blog posts assumed:

| Model | Use it for |
|-------|-----------|
| `claude-opus-5-5` | The default. Hardest reasoning, long agentic runs. |
| `claude-sonnet-5-5` | High-volume production — the balanced workhorse. |
| `claude-haiku-5-5` | Cheap, fast, simple tasks (classify, route, label). |
| `claude-fable-5-1` | The most capable model — reserve for the truly hard. |

Model list from platform.claude.com/docs/en/about-claude/models/overview, retrieved 2026-10-28. Re-check it; this table goes stale.

Three things that are *different* now, and that this guide assumes:

1. **Thinking is adaptive.** On current models you no longer set a token budget
   (the old `budget_tokens` setting returns an error from Claude 4.7 onward). You set
   *effort* (`low`/`medium`/`high`/`xhigh`/`max`) and the model decides how hard to
   think. Not every model supports every level, and the default differs by model
   (`high` on most, `medium` on Opus 5.5 and Haiku 5.5).
2. **Turns can run for minutes.** A single agentic request may take 15 minutes.
   Plan for it — don't sit and stare at a frozen terminal.
3. **Tools are standard (MCP).** Agents reach into real systems now. That makes
   verification *more* important, not less — see Rule 6.

---

## The 10 Rules

### Rule 1 — Start at the highest Spec Level you honestly hold

> A **vending machine** gives you exactly what you press. A **genie** guesses.
> Vague prompts summon the genie.

From the Field Manual's Specification Spectrum:

```
Level 1 (Features)   → "I want a RAG config"          ← you're still exploring
Level 2 (Behavior)   → "scores below 0.85 get dropped"
Level 3 (Contract)   → "ask(q:str) -> {answer, sources}"  ← your default
Level 4 (Test Cases) → "empty input returns None, not a crash"
```

**Rule of thumb:** boring code (lists, configs) → Level 1–2 is fine.
Code with *logic* (gates, tools, agents) → climb to Level 3–4 or pay later.

---

### Rule 2 — Always use the Constraint Sandwich

> A **recipe card** has three parts: what you've already decided, the one dish,
> and how you'll know it's done. Never hand the AI just the middle.

```
CONSTRAINTS: rules you've already decided (so the AI doesn't decide them for you)
REQUEST:     the ONE thing you want built
VALIDATION:  the checklist the output must pass
```

Every entry in this folder follows this shape. So should every prompt you write.

---

### Rule 3 — One concept per prompt

> You don't ask a chef to invent a sauce *and* redesign the menu in one breath.

Chain two new things and you can't tell which one broke. Build the schema.
*Then* build the tool that uses the schema. *Then* wire it together. This is
the same decomposition the End-to-End projects use (`schema.py` → `tools.py`
→ `main.py`).

---

### Rule 4 — Match the model to the job, not your ego

> You don't preheat a pizza oven to toast bread.

Reaching for `claude-fable-5-1` or `effort: max` on a classification task burns
time and money for no gain. Cost climbs with capability:

```python
# Cheap, fast — a label is all you need
client.messages.create(model="claude-haiku-5-5", max_tokens=64, ...)
# Hard, autonomous — worth the spend
client.messages.create(model="claude-opus-5-5",
                       output_config={"effort": "high"}, ...)
```

Pick the smallest model that can do the job, and leave effort at the model's
default unless you have a reason. Step effort down for routine work once your
evals show quality holds; step it up only when the output actually falls short.

---

### Rule 5 — Demo mode first, real key second

> You don't test-drive a car in traffic. You start in an empty parking lot.

Every template in this course runs with `DEMO_MODE = True` and **zero**
network calls. Get the *shape* right for free, then flip one switch:

```python
DEMO_MODE = True   # canned output, no API key, no cost
# ...prove the flow works...
DEMO_MODE = False  # now it's real
```

Make the demo path your default in everything you build.

---

### Rule 6 — Trust, then verify (the only rule that matters most)

> A **self-driving car** still has a steering wheel. You don't grab it often —
> but the day you need it, it has to be there.

This is the rule the genie-believers skip. AI-written code that *looks* right
and *runs* can still be confidently wrong. The cautionary tale lives in this
very repo: [`Project3_Codebase_Auditor`](../09-Phase09_End_to_End_Projects/Project3_Codebase_Auditor/eval_loop.py)
once flagged a harmless `add(a, b)` function as "SQL injection" because the
demo verdict was hardcoded. It *ran*. It *looked* authoritative. It was wrong.

Three habits that catch this:

1. **Read the output against the VALIDATION line** you wrote in Rule 2.
2. **Feed it the edge case** — empty input, the safe file, the zero score.
3. **Make the AI prove it** with a test, not a paragraph of reassurance.

---

### Rule 7 — Show the bad path, not just the happy one

> A good driving instructor doesn't just show you a smooth lane change —
> they show you the skid and how to recover.

Most prompts (and this folder) demonstrate the *clean* result. The skill you
actually live in is **correction**:

```
1. Vague prompt   → 2. Wrong code   → 3. Add a constraint   → 4. Right code
```

When the AI gives you something off, don't rewrite from scratch — add the one
constraint that rules out the mistake. That's Mode 3 (Iteration) from the
Field Manual, and it's where 80% of real vibe coding happens.

---

### Rule 8 — Treat the system prompt as context, not commands

> You brief a contractor on the building codes once. You don't scream "CRITICAL:
> YOU MUST USE A LEVEL" before every single nail.

2026 models follow instructions *closely*. Aggressive all-caps prompts written
for older, more reluctant models now **overtrigger**.

```
❌ "CRITICAL: You MUST use the search tool every time."
✅ "Use the search tool when the answer depends on current information."
```

State the situation. Let the model act on it.

---

### Rule 9 — Plan for the long turn

> A slow-cooker meal isn't a microwave meal. You don't lift the lid every minute.

Agentic runs take time. Don't block your whole session waiting:

- Give the **full task** up front in one clear brief (not dribbled across turns).
- Use **streaming** for anything long, so you see progress instead of a freeze.
- Check in **asynchronously** — let the agent work while you do something else.

---

### Rule 10 — Make the AI write down what it learns

> A good apprentice keeps a notebook. A great one re-reads it before the next job.

For anything multi-step, have the agent persist findings to a file and consult
it next time. One lesson per note, with a one-line summary on top. This is the
difference between an agent that repeats your corrections and one that doesn't.

---

## The pre-flight checklist (tape this to your monitor)

Before you send any vibe-coding prompt:

- [ ] **Spec Level** — am I as precise as my certainty allows? (Rule 1)
- [ ] **Sandwich** — Constraints / Request / Validation, all three present? (Rule 2)
- [ ] **One concept** — am I asking for exactly one new thing? (Rule 3)
- [ ] **Right model + effort** — cheapest tool that can do the job? (Rule 4)
- [ ] **Demo first** — can I prove the shape with no API key? (Rule 5)

After the AI responds:

- [ ] **Verify** — does it pass the VALIDATION line I wrote? (Rule 6)
- [ ] **Edge case** — did I feed it the empty / safe / zero input? (Rule 6)
- [ ] **Correct, don't restart** — one constraint to fix the miss? (Rule 7)

---

## The one sentence to remember

> **The AI writes the code. You own the outcome. Precision and verification are
> the whole job.**
