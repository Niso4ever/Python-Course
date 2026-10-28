# Project 3: AI Content Studio (Multi-Agent CrewAI)

**The 2026 context:** Media companies, marketing teams, and research organizations run multi-agent "studios" where specialist AI agents collaborate on content — one researches, one writes, one edits, one optimizes for SEO. Output that took 4 hours now takes 4 minutes. A human editor reviews the final piece.

---

## What It Does

Takes a content brief and runs a 3-agent pipeline:

1. **Research Agent** — searches the web, gathers data, finds statistics and examples
2. **Writer Agent** — transforms research into structured, engaging content
3. **Editor Agent** — reviews for quality, accuracy, tone, and recommends final edits

Output: publication-ready article in Markdown format.

---

## Architecture

```
Content Brief (topic + audience + format)
        ↓
┌────────────────────────────────────────────┐
│  CrewAI Sequential Pipeline                │
│                                            │
│  [RESEARCHER]                              │
│  role: Senior Research Analyst             │
│  tools: web_search, read_document          │
│  output: Research notes + data points      │
│        ↓                                   │
│  [WRITER]                                  │
│  role: Senior Content Writer               │
│  tools: (none — pure writing)              │
│  output: Structured article draft          │
│        ↓                                   │
│  [EDITOR]                                  │
│  role: Editorial Director                  │
│  tools: (none — review + feedback)         │
│  output: Edited article + quality score    │
└────────────────────────────────────────────┘
        ↓
  Final Article (saved to ./output/)
```

---

## Files

| File | What it does |
|:-----|:-------------|
| `agents.py` | Define the 3 specialist agents with roles and backstories |
| `tasks.py` | Define what each agent is asked to produce |
| `crew.py` | Assemble and run the crew |
| `main.py` | CLI entry point with sample briefs |

---

## Setup

```bash
cd Project3_MultiAgent_CrewAI
pip install -r requirements.txt
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env
# Also add OPENAI_API_KEY: crew.py sets memory=True, and CrewAI memory uses
# OpenAI embeddings by default (or pass embedder={...} to Crew to use another provider)

python main.py
# or: python main.py --topic "How AI is changing software engineering in 2026"
# or: python main.py --demo
```

---

## Sample Output

Given brief: *"AI agents in enterprise: ROI and adoption patterns 2026"*

The crew produces a 600-800 word article with:
- Executive-level hook
- 3-5 data points from web research
- Expert analysis and narrative
- Clear sections (findings, analysis, implications)
- SEO-optimized subheadings
