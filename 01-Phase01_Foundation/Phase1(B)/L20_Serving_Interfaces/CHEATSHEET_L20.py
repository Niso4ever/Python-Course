"""
CHEATSHEET L20: Serving Interfaces
Concepts: Streamlit UI components, Session State, Chat Elements
Important: Run this with `streamlit run CHEATSHEET_L20.py`
"""
import streamlit as st

# ==========================================
# PATTERN 1: Basic Page Layout
# ==========================================
st.set_page_config(page_title="Cheat Sheet App", page_icon="📝")

st.title("My App Dashboard")
st.markdown("This is a paragraph of **markdown** text.")

# ==========================================
# PATTERN 2: Widgets (Inputs and Buttons)
# ==========================================
# Sidebar inputs (moves these widgets to the left side menu)
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Robot Temperature", min_value=0.0, max_value=1.0)
    api_key = st.text_input("API Key", type="password")

# Main page button
if st.button("Run Process"):
    st.success("The process ran successfully!")
    st.info(f"Using temp: {temperature}")

# ==========================================
# PATTERN 3: Session State (Surviving Reruns)
# ==========================================
st.divider() # Draws a horizontal line
st.subheader("Counter Example")

# Initialize the state variable on the first run only
if "click_count" not in st.session_state:
    st.session_state.click_count = 0

if st.button("Click me!"):
    st.session_state.click_count += 1

st.write(f"Total clicks: {st.session_state.click_count}")

# ==========================================
# PATTERN 4: Chat UI Elements
# ==========================================
st.divider()
st.subheader("Chat Interface")

# Displaying a message bubble on screen (like iMessage styling)
with st.chat_message("assistant"):
    st.write("Hello human! How can I help you?")

# Getting input from the user at the bottom of the screen
user_input = st.chat_input("Type your message here...")
if user_input:
    # This block triggers when the user presses Enter
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        st.write(f"I received: {user_input}")
