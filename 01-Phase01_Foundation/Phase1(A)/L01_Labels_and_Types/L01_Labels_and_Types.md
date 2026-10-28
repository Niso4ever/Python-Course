# Lesson 01: Labels, Containers, and Types
## The Drawer & Sticker Theory

> **2026 Note:** In real AI code you will see TWO labeling styles:
> Classic: `user_query = "text"` — still valid everywhere
> With type hint: `user_query: str = "text"` — same drawer, adds a type label
> The `: str` part is documentation for humans and editors. Code runs identically.

Welcome, Architect. In this first lesson, we aren't "coding." We are **labeling the materials** of our AI system.

Imagine your computer's memory as a massive wall of empty drawers. To build anything meaningful, like a chatbot or a search agent, we need to put data into these drawers so we can find it later.

### 1. The Sticker Principle (Variables)
In Python, we don't just "store" things. We put a **Sticker** (a Label) on a drawer. From then on, whenever we use that label, Python reaches into that specific drawer and pulls out what's inside.

```python
# Classic style (still valid everywhere):
user_query = "How do I build an AI agent?"
token_limit = 4096

# 2026 style — same drawers, adds type labels:
user_query: str = "How do I build an AI agent?"
token_limit: int = 4096
```

| Label | Annotation | Role |
| :--- | :--- | :--- |
| `user_query` | `str` (Text) | The raw energy (input) sent by the user to our system. |
| `token_limit` | `int` (Number) | The physical constraint of our "brain" (LLM context window). |

**Type hint shape:** `name: type = value` — colon + type comes BEFORE the `=` sign.

---

### 2. The Material Types (Data Types)
Not all materials are the same. An Architect must know if they are working with raw text (Steel) or numbers (Measurements).

- **`str` (Text)**: Surrounding things in quotes `" "` tells Python "This is a message, don't try to calculate it."
- **`int` (Whole Numbers)**: Used for counting steps or limiting results.
- **`dict` (DNA/JSON)**: The most important tool. A container that maps a "Key" to a "Value." This is how AI components talk to each other.

```python
# The DNA of a Retrieval result
context_meta = {
    "source": "knowledge_base_v1",
    "relevance_score": 0.98,
    "is_verified": True
}
```

---

### 3. Intermediate Reinforcement: Material Check
**Question:** If you have a Drawer labeled `llm_temperature = "0.7"`, what material type is it?
*A) A Number (int)*
*B) Text (str)*
*C) A Logic Gate (bool)*

*(Think about those quotes...)*

---

### 4. Interactive Training Ground
Now, enter the construction site. Open [template_llm_metadata.py](template_llm_metadata.py) and [CHEATSHEET_L01.py](CHEATSHEET_L01.py) in this folder to practice labeling your materials.

**Mission:** Complete the blueprint for the `context_meta` DNA and initialize the `user_query` drawer.
