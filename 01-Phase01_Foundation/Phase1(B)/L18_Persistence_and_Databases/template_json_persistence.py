"""
TEMPLATE: JSON Persistence
CURRICULUM PATTERN: L18
DESCRIPTION: An agent that saves its conversation history to the hard drive,
so it can remember you between script runs.
"""

import json
import os

class PersistentAgent:
    def __init__(self, agent_name):
        self.name = agent_name
        # The filename where this specific agent keeps its memories
        self.memory_file = f"{self.name}_memory.json"
        
        # Load memory from the hard drive if it exists, otherwise start fresh
        self.history = self.load_memory()
        
        print(f"[{self.name}] Booted up. History length: {len(self.history)} messages.")

    def load_memory(self):
        """Pattern [L18] - Opening the filing cabinet."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        else:
            # If no file exists, return an empty list
            return []

    def save_memory(self):
        """Pattern [L18] - Putting files into the cabinet."""
        with open(self.memory_file, "w") as f:
            json.dump(self.history, f, indent=4)
        print(f"[{self.name}] Memory saved to disk.")

    def chat(self, user_message):
        """Main interaction loop."""
        # 1. Add user message to history
        self.history.append({"role": "user", "content": user_message})
        
        # [Simulating LLM call here]
        bot_reply = f"I hear you saying: {user_message}"
        
        # 2. Add bot reply to history
        self.history.append({"role": "assistant", "content": bot_reply})
        
        # 3. Save the updated history back to the hard drive
        self.save_memory()
        
        return bot_reply

# ==========================================
# USAGE
# ==========================================
if __name__ == "__main__":
    # 1. Create the agent
    # If you run this script multiple times, it will remember the history!
    bot = PersistentAgent("helper_bot")
    
    # 2. Add some new history
    # Try changing this message, saving, and running the script again
    response = bot.chat("My favorite color is blue.")
    print(response)
