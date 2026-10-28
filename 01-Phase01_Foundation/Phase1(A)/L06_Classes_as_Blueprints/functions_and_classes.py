# ============================================================
# FUNCTIONS AND CLASSES — type this out to feel the syntax
# Curriculum: L05 (functions) + L06 (classes)
# ============================================================


# ============================================================
# PART 1 — STANDALONE FUNCTIONS (individual tools)
# Each function does ONE job. No memory. Input in → output out.
# ============================================================

def count_tokens(text):
    # counts roughly how many tokens are in a piece of text
    # 1 token ≈ 4 characters
    return len(text) // 4


def format_prompt(user_query, context):
    # builds the full prompt string to send to the LLM
    # combines the context (what we know) with the user question
    return f"Context: {context}\nQuestion: {user_query}"


def call_llm(prompt):
    # sends the prompt to the LLM and returns the response
    # simulated here so you can run it locally
    return f"[simulated response to: '{prompt[:40]}...']"


# ============================================================
# PART 2 — CLASS THAT USES THOSE FUNCTIONS
# The class is the toolbox. It holds memory AND calls the tools.
# ============================================================

class RAGAgent:
    # this is the BLUEPRINT — not the machine yet, just the design

    def __init__(self, model):
        # runs once when you CREATE the agent
        # powering on and configuring the machine

        self.model        = model   # remember which model to use
        self.history      = []      # empty memory — grows with each query
        self.total_tokens = 0       # token counter starts at zero

    def run(self, user_query, context):
        # the main tool on the machine
        # calls all three standalone functions in sequence

        # Step 1 — count tokens
        tokens = count_tokens(user_query)
        self.total_tokens += tokens

        # Step 2 — build the prompt
        prompt = format_prompt(user_query, context)

        # Step 3 — call the LLM
        llm_response = call_llm(prompt)

        # Step 4 — remember this query
        self.history.append(user_query)

        return llm_response

    def get_stats(self):
        # read the machine's memory
        return {
            "total_queries": len(self.history),
            "total_tokens":  self.total_tokens,
            "last_query":    self.history[-1] if self.history else None
        }


# ============================================================
# PART 3 — CREATING AND USING THE AGENT
# ============================================================

# create the machine from the blueprint
agent = RAGAgent("claude-sonnet-5-5")

# use the machine
response = agent.run(
    user_query = "What is RAG?",
    context    = "RAG stands for Retrieval Augmented Generation."
)

print(response)
print(agent.get_stats())
