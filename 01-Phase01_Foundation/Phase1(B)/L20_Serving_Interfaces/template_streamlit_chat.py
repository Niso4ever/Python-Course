"""
TEMPLATE: Streamlit Chat Wrapper
CURRICULUM PATTERN: L20
DESCRIPTION: A generic wrapper that puts a web UI on top of ANY text-based agent.
Important: Run with `streamlit run template_streamlit_chat.py`
"""

import streamlit as st
import time # Just for simulating an LLM typing delay

# 1. Dummy Agent Class (Imagine this is imported from your real agent file!)
class DummyAgent:
    def chat(self, user_msg):
        # Pretend the LLM is thinking and making API calls
        time.sleep(1)
        return f"ROBOT SAYS: I processed '{user_msg}'. Beep boop."

# ==========================================
# STREAMLIT UI WRAPPER
# ==========================================

st.title("🤖 My Custom Agent Web Interface")

# Initialize Session State Variables
if "agent" not in st.session_state:
    # Boot up the engine only exactly once!
    st.session_state.agent = DummyAgent()

if "messages" not in st.session_state:
    # A list to store the UI chat logs
    st.session_state.messages = []

# ==========================================
# RENDER HISTORICAL MESSAGES
# ==========================================
# Because Streamlit reruns the script top-to-bottom every click,
# we must "re-draw" all past messages on the screen.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# NEW USER INPUT
# ==========================================
# Wait for the user to type something and press Enter
if prompt := st.chat_input("What is up?"):

    # 1. Draw the user's message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save it to the UI logs
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Ask the underlying Agent for an answer
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            # Call the agent engine!
            response = st.session_state.agent.chat(prompt)
            st.markdown(response)
    
    # Save the agent's answer to the UI logs
    st.session_state.messages.append({"role": "assistant", "content": response})
