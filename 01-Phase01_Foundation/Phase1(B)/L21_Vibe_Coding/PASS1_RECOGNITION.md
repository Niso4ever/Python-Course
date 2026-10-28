# 3-Pass Reading: System Prompt Builder

## Pass 1: Recognition (Labeling the Logic)

Look at `template_system_prompt.py`. What building blocks do we see?

1. `class PromptBuilder:`
   - **Pattern:** `[L06]` Classes as Blueprints. We built a machine designed strictly to generate text dynamically.
2. `self.constraints = []`
   - **Pattern:** `[L02]` Lists and Collections. Instead of writing one massive, messy string, we store the constraints in a clean list so we can manage them programmatically.
3. `def add_constraint(self, rule: str):`
   - **Pattern:** `[L05]` Functions as Tools (+ Type Hints). This is a tool to mutate the state of our PromptBuilder machine.
4. `prompt += "\n".join(self.constraints) + "\n\n"`
   - **Pattern:** Python string manipulation. The `.join()` command takes a list like `["Rule 1", "Rule 2"]` and glues it into a single string separated by newlines. 

## Pass 2: Quality Check (What's Hardcoded?)
* This is a very rigid structure `[ROLE] -> [CONSTRAINTS] -> [EXAMPLES]`. If a specific foundation model prefers a different prompting style (e.g., Anthropic prefers XML tags like `<constraints>`), we would have to rewrite the `build_prompt()` logic.

## Pass 3: Extraction (What to Steal)
If you want to quickly build prompts programmatically without needing a giant, ugly multi-line f-string in the middle of your code:
```python
role = "You are an assistant."
rules = ["Keep it short", "Use emojis"]
prompt = f"{role}\n\nRULES:\n" + "\n".join(rules)
```
