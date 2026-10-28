# Project 2: AI Research Analyst (Agent with Tools)

**The 2026 context:** In 2026, autonomous AI agents handle the research workload that used to take a junior analyst hours: web searches, data retrieval, calculations, report writing. A human reviews the final report, not every search. This project builds that agent.

---

## What It Does

You give it a research brief. It:
1. **Plans** what information it needs (Thought)
2. **Searches** the web for current data (Action → web_search)
3. **Calculates** numbers and statistics (Action → calculator)
4. **Reads** documents from disk (Action → read_document)
5. **Synthesizes** everything into a structured report (Final Answer)

The human only sees the finished report.

---

## Architecture

```
User Research Brief
      ↓
   ReAct Agent (Claude Opus 5.5)
      ├── Thought: "What data do I need?"
      ├── Action: web_search("AI investment 2025")
      ├── Observe: [results]
      ├── Action: calculator("245000 * 1.42")
      ├── Observe: 347900
      ├── Action: read_document("background.txt")
      ├── Observe: [document content]
      └── Final Answer: [Structured Report]
```

---

## The Tools

| Tool | What it does | When agent uses it |
|:-----|:-------------|:-------------------|
| `web_search` | Search the internet for current data | Any question needing recent/live info |
| `calculator` | Evaluate math expressions accurately | Any arithmetic — LLMs make math errors |
| `read_document` | Read a local file | Background research docs, reports |
| `write_report` | Save the final report to disk | Always used last to persist the report |

---

## Files

| File | What it does |
|:-----|:-------------|
| `tools.py` | All 4 tool definitions + execution functions |
| `agent.py` | ReAct agent loop using Anthropic tool-use API |
| `main.py` | Run the research agent on a topic |

---

## Setup

```bash
cd Project2_Agent_with_Tools
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

python main.py
# or: python main.py --topic "Impact of AI agents on knowledge work in 2026"
# or: python main.py --demo
```

---

## In Production (2026)

- Web search uses real APIs: Exa.ai, Tavily, or Brave Search API
- Agent runs on a schedule: daily competitive intelligence report
- Reports saved to Google Drive / SharePoint automatically
- Slack notification when report is ready
- Human reviews and approves in 5 minutes instead of 5 hours
