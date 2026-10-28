# Phase 2: Real Systems — Build Production AI (2026)

**4 Projects — 8 to 12 hours total**

This phase takes everything from Phase 0 and Phase 1 and turns it into **real, runnable AI systems** — the kind that companies are deploying in 2026.

---

## The 2026 AI Landscape

In 2026, AI is no longer experimental. It is production infrastructure:

- **RAG systems** are how companies ground AI in their own data. Every enterprise knowledge base has one.
- **Autonomous agents** routinely browse the web, write code, and make decisions. A human reviews the output, not every step.
- **Multi-agent pipelines** replace entire teams for content creation, research, and analysis.
- **Self-optimizing pipelines** (DSPy) mean prompts are no longer hand-written — the system learns them from your data.

These 4 projects build exactly that.

---

## Projects

| # | Project | Stack | Real-World Use |
|:--|:--------|:------|:---------------|
| **1** | RAG Pipeline | Anthropic + ChromaDB | Company knowledge base / internal docs assistant |
| **2** | Agent with Tools | Anthropic direct | Autonomous research analyst |
| **3** | Multi-Agent CrewAI | CrewAI + Anthropic | AI content studio (research → write → review) |
| **4** | DSPy Pipeline | DSPy + Anthropic | Self-optimizing support ticket triage |

---

## Folder Structure

```
02-Phase02_Real_Systems/
├── README.md                          ← This file
├── Project1_RAG_Pipeline/             ← Enterprise knowledge assistant
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── ingest.py                      ← Load & embed documents
│   ├── retriever.py                   ← Search + answer
│   ├── main.py                        ← Run the assistant
│   └── sample_data/knowledge_base.txt ← Sample company docs
│
├── Project2_Agent_with_Tools/         ← Autonomous research agent
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── tools.py                       ← Tool definitions
│   ├── agent.py                       ← Agent loop
│   └── main.py                        ← Run the agent
│
├── Project3_MultiAgent_CrewAI/        ← AI content studio
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   ├── agents.py                      ← Crew member definitions
│   ├── tasks.py                       ← Task definitions
│   ├── crew.py                        ← Crew assembly
│   └── main.py                        ← Run the studio
│
└── Project4_DSPy_Pipeline/            ← Self-optimizing triage
    ├── README.md
    ├── requirements.txt
    ├── .env.example
    ├── signatures.py                  ← DSPy signatures
    ├── pipeline.py                    ← DSPy module
    ├── optimizer.py                   ← Training + optimization
    └── main.py                        ← Run the triage system
```

---

## How to Use Each Project

1. `cd` into the project folder
2. `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` and add `ANTHROPIC_API_KEY=sk-ant-...`
4. Run `python main.py` — or `python main.py --demo`, which runs every project without an API key

---

## What You Learn From Each Project

**Project 1 (RAG):** How to ingest documents, store them as embeddings, and retrieve the right chunks to answer questions. The backbone of every AI assistant in 2026.

**Project 2 (Agent):** How a single agent uses tools autonomously — reasoning about which tool to call, calling it, using the result, and knowing when to stop.

**Project 3 (CrewAI):** How to decompose work across specialist agents: a researcher, a writer, and an editor working in sequence to produce content that one agent alone couldn't.

**Project 4 (DSPy):** How to eliminate hand-written prompts entirely — define the task as a signature, train it on examples, and let the optimizer find better prompts than you could write manually.
