# Lesson 20: Serving Interfaces (Giving Your Agent a Face)

Up until now, you have been interacting with your agents through the terminal (the black text screen). The terminal is the engine room. But normal users don't want to go into the engine room; they want a sleek, modern interface.

We can add a UI (User Interface) to almost any Python script using a library called **Streamlit**. 

> **Metaphor:** The glossy touch-screen bolted onto the front of the coffee machine. The brewing mechanics inside haven't changed, but the way the user *orders* their coffee is much nicer.
> **Plain English:** We write a few lines of Python that automatically generate a fully-functional web page with chat boxes, buttons, and text fields.

## 1. Streamlit Basics
Streamlit reads your Python script from top to bottom and draws web elements on the screen in that order.

```python
import streamlit as st

# Draw a title on the web page
st.title("My First AI App 🤖")

# Draw a text input box
user_name = st.text_input("What is your name?")

# Draw a button
if st.button("Say Hello"):
    st.write(f"Hello there, {user_name}!")
```
> This is the **[L20]** pattern — drawing basic UI widgets.

*Note: To run a Streamlit app, you don't type `python script.py`. You type `streamlit run script.py` in your terminal!*

## 2. The Golden Rule of Streamlit (Script Reruns)
Here is the hardest concept to grasp about Streamlit: **Every time the user clicks a button or types in a box, the ENTIRE script runs again from top to bottom.**

If you create your AI Agent model inside the script, a *new* agent is created every time the user types a new message, wiping out its memory!

To fix this, we use `st.session_state`. This is a special dictionary that guarantees variables survive the script reruns.

```python
import streamlit as st
from my_agent_file import PersistentAgent # Assume we built an agent in L06

# Only create the heavy agent on the VERY FIRST run
if "agent" not in st.session_state:
    st.session_state.agent = PersistentAgent("bot")

# Now we can safely use the agent without it being erased on reruns
st.session_state.agent.chat("Hello!")
```

## Why This Matters for Architecture
1. **Decoupling (Separation of Concerns):** Notice that we didn't change the `PersistentAgent` code at all. The UI is just a thin wrapper sitting on *top* of our existing logic. A good architect keeps the "engine" (the agent functionality) totally separate from the "paint job" (the UI).
2. **Prototyping Speed:** If you design a brilliant multi-agent system, the absolute fastest way to get it into the hands of real users to test it is to throw a 20-line Streamlit wrapper around your `main()` loop.
