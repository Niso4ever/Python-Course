"""
TEMPLATE: System Prompt Builder
CURRICULUM PATTERN: L21
DESCRIPTION: This script demonstrates how to construct a rock-solid, 
constraint-heavy system prompt for an internal agent taking action in your app.
"""

# Think of this class as a Prompt Factory.
class PromptBuilder:
    def __init__(self, agent_role: str):
        # 1. The Context (Who are you?)
        self.role = f"You are a highly skilled {agent_role}."
        self.constraints = []
        self.examples = []

    def add_constraint(self, rule: str):
        """Pattern [L21] - Adding rules to prevent hallucinations."""
        self.constraints.append(f"- {rule}")

    def add_example(self, input_text: str, output_text: str):
        """Pattern [L21] - Giving the AI a fill-in-the-blank pattern."""
        self.examples.append(f"Q: {input_text}\nA: {output_text}")

    def build_prompt(self) -> str:
        """Assembles the final string to send to the LLM."""
        prompt = f"[ROLE]\n{self.role}\n\n"
        
        if self.constraints:
            prompt += "[CRITICAL CONSTRAINTS]\n"
            prompt += "\n".join(self.constraints) + "\n\n"
            
        if self.examples:
            prompt += "[EXAMPLES OF DESIRED BEHAVIOR]\n"
            prompt += "\n\n".join(self.examples) + "\n"
            
        return prompt

# ==========================================
# USAGE
# ==========================================
if __name__ == "__main__":
    bullet_point_agent = PromptBuilder("Summarization Expert")
    
    # Notice how we specifically outline what NOT to do
    bullet_point_agent.add_constraint("Output exactly 3 bullet points, no more, no less.")
    bullet_point_agent.add_constraint("Do not use the word 'therefore'.")
    bullet_point_agent.add_constraint("Do not include conversational filler.")
    
    # We provide a 1-shot example it can mentally align to
    bullet_point_agent.add_example(
        input_text="The quick brown fox jumps over the lazy dog.",
        output_text="- Fox is quick\n- Fox jumps\n- Dog is lazy"
    )

    final_system_prompt = bullet_point_agent.build_prompt()
    
    print("----- ASSEMBLED SYSTEM PROMPT -----")
    print(final_system_prompt)
