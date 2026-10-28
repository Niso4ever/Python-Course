# 3-Pass Reading: Persistence

## Pass 1: Recognition (Labeling the Logic)

Look at `template_json_persistence.py`. What building blocks do we see?

1. `import json` and `import os`
   - **Pattern:** `[L08]` Import Patterns. We are pulling in external toolkits. `os` specifically lets us talk to the operating system (to check if a file exists on the hard drive).
2. `class PersistentAgent:`
   - **Pattern:** `[L06]` Classes as Blueprints. We are building a stateful agent machine.
3. `def load_memory(self):`
   - **Pattern:** `[L05]` Functions as Tools. This function encapsulates the "load from disk" behavior.
4. `if os.path.exists(self.memory_file):`
   - **Pattern:** `[L03]` Logic Gates. A simple fork in the road: if file exists, read it; else, return empty list.
5. `with open(self.memory_file, "w") as f:`
   - **Pattern:** `[L18]` JSON Persistence. The core pattern for writing strings to a file safely.

## Pass 2: Quality Check (What's Hardcoded?)
* The file paths are saved locally to whatever folder the script is run in (`f"{self.name}_memory.json"`). If we move the script to another directory, it might save files somewhere confusing or fail to find the old memory.
* We are trusting the LLM formatting. If the `self.history` object wasn't a clean list of dictionaries (for example, if it contained a custom Python object), `json.dump` might throw an error because it doesn't know how to turn a custom object into text.

## Pass 3: Extraction (What to Steal)
If you just want to add memory to your existing agent, grab the generic safe-loading block to put in your `__init__`:
```python
if os.path.exists("memory.json"):
    with open("memory.json", "r") as f:
        self.history = json.load(f)
else:
    self.history = []
```
