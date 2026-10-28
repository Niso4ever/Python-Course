# Lesson 21: Vibe Coding & Prompt Agents (The Architect's Secret)

If you are following this curriculum correctly, you are not writing code from scratch. You are reading code, designing systems, and telling an AI to write the code for you. This is called **Vibe Coding**.

However, if you just tell an AI, "Build me a RAG chatbot," it will generate messy, outdated, hallucinated garbage.

To get perfect, curriculum-aligned code on the first try, you must give the AI three things: **Context**, **Constraints**, and **Examples**.

> **Metaphor:** Hiring a brilliant but manic junior developer who works infinitely fast, but needs literal, exact blueprints so they don't accidentally build the bathroom in the kitchen.

---

## The Anatomy of the Perfect Architect Prompt

Never talk to the AI like a search engine. Talk to it like an employee. Every prompt you write should have these three sections:

### 1. The Context (Who are you?)
Tell the AI what role it is playing and what you are trying to achieve broadly. 
* *Example:* "You are a senior AI engineer helping me build a local Python agent."

### 2. The Constraints (What are the rules?)
This is where vibe coders fail. If you do not give constraints, the AI will default to the most convoluted, complex, globally-popular solution it scooped up from Reddit in 2023. **You must forbid things.**
* *Example:* "Do not use LangChain or LlamaIndex. Write this using only raw the `dspy` framework."
* *Example:* "Do not use complex async patterns. Keep it under 50 lines."

### 3. The Example (The Template)
The AI is infinitely better at copying a pattern than inventing one. If you want the AI to write a DSPy node for your agent, **literally paste one of the `template_` files from this curriculum into your prompt** and say "Copy this exact shape."
* *Example:* "I want you to build me a weather tool. Follow the exact error-handling and API structure found in this template: [Paste `template_api_tool.py` here]."

---

## Generating Agent Instructions (System Prompts)

The same rules apply when you are writing the internal "System Prompt" that powers the agents you build inside your Python code.

An agent without constraints is a wild card. If you build a customer support agent but only give it the prompt "You are helpful support," it might offer free refunds to everyone. 

A production-grade system prompt uses our same three pillars:
```text
[CONTEXT] You are a customer support agent for Acme Corp.
[CONSTRAINTS] You may only answer questions based on the provided manual. Do not guess. You cannot authorize refunds.
[EXAMPLES]
User: My coffee is cold.
Agent: I'm sorry to hear that! Please check page 4 of the manual regarding the heating element.
```

## Why This Matters for Architecture
1. **Speed:** If you master the Architect Prompt, you stop debugging syntax errors. You can build a 3-agent orchestration system in 10 minutes because the AI writes the boilerplate flawlessly.
2. **Predictability:** When your internal Agent System Prompts are tightly constrained with examples, your agents stop hallucinating and start acting like deterministic functions.

In the cheatsheet, we will look at exact, copy-paste prompts you can use to force your coding assistants (Claude, Cursor, GitHub Copilot) to behave.
