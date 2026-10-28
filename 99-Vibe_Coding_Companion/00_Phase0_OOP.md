# Phase 0 — OOP Anatomy (1 template)

The single foundational template: one class with every OOP concept labeled.

---

## 0. `template_ai_agent_anatomy.py`
**Pattern:** Phase 0 · **Level 2 (Behavior)** · **Mode 1 (Exploration)**

Source: `00-Phase00_OOP_Introduction/template_ai_agent_anatomy.py`

### 📝 THE VIBE PROMPT
```
CONSTRAINTS:
  Standard library only. One single class. Add a comment label on EVERY
  OOP concept as it appears (class, __init__, attribute, method, self, instance).

REQUEST:
  Build one teaching Agent class where I can watch its state change as I call
  methods. It should hold a name + history, have a method that does work and
  appends to history, and a method that prints its current state.

VALIDATION:
  - Creating two agents proves they are independent (separate state).
  - Calling a method visibly mutates that instance's history.
  - Running the file top-to-bottom narrates what each concept is.
```

### 💻 THE CODE IT PRODUCES (essence)
```python
class Agent:                       # ← class (the blueprint)
    def __init__(self, name):      # ← constructor
        self.name = name           # ← attribute (state)
        self.history = []          # ← state that will grow
    def act(self, task):           # ← method (behavior)
        self.history.append(task)  # ← self mutates THIS instance
```
> Two `Agent(...)` instances never share `history` — that's the whole lesson.
