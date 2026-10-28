# Lesson 18: Persistence (Data That Survives)

If the context window is the agent's short-term memory (a sticky note that gets thrown away when the conversation ends), then persistence is the agent's long-term memory (a filing cabinet).

When a Python script finishes running, everything in its memory (`self.history`, variables) is erased. To save that history so the agent remembers you tomorrow, we must write that data to a physical file on the hard drive.

## 1. JSON Files (The Filing Cabinet)
JSON (JavaScript Object Notation) is a text format shaped exactly like Python lists and dictionaries. It is the universal language for saving structured data across almost all programming languages.

> **Metaphor:** Writing down the coffee machine's internal state into a physical ledger book before unplugging it.
> **Plain English:** We convert a Python dictionary into a string of text and save it to a `.json` file on your computer.

```python
import json

# 1. The data we want to save (a normal dictionary)
agent_memory = {
    "user_name": "Alice",
    "last_topic": "RAG architecture"
}

# 2. Writing (saving) the file
with open("memory.json", "w") as file:
    json.dump(agent_memory, file)
print("Memory saved to cabinet!")
```
> This is the **[L18]** pattern — saving dictionaries to JSON.

## 2. Loading JSON (Opening the Cabinet)
When the agent starts up *tomorrow*, the first thing it should do is check if the filing cabinet has a memory file, and load it back into its `self.history`.

> **Metaphor:** The coffee machine reading the ledger book before brewing the first cup of the day to remember your usual order.
> **Plain English:** We open the `.json` file from the hard drive and convert the text back into a Python dictionary.

```python
import json

# 1. Opening (loading) the file
with open("memory.json", "r") as file:
    loaded_memory = json.load(file)

print(f"Welcome back, {loaded_memory['user_name']}!")
# We can now use it like a normal dictionary again
```
> This is the **[L18]** pattern — loading JSON into dictionaries.

## Why This Matters for Architecture
1. **Chat History:** When you use ChatGPT, it remembers your past conversations. It does this by saving the message list to a database and loading it when you select a past chat.
2. **Configuration:** Agent instructions, system prompts, and tool configurations are often saved in `.json` files so you can change the agent's behavior without editing the actual Python logic code.

In the next lesson, we will look at how to get data from *other* people's filing cabinets across the internet using Network Requests and APIs.
