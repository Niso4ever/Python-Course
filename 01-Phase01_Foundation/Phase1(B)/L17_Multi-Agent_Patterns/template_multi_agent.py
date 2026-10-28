"""
TEMPLATE: Multi-Agent Patterns
=====================================
4 patterns: Sequential Pipeline, Hierarchical, Parallel Fan-Out, Critic-Actor.

pip install: pip install anthropic crewai python-dotenv

Simulated demos run without API key.
Real API calls need: ANTHROPIC_API_KEY in .env
"""
import json
from dotenv import load_dotenv

load_dotenv()


# ═══════════════════════════════════════════════════════════
# SIMULATED AGENT (replace with real LLM calls)
# ═══════════════════════════════════════════════════════════
def simulated_agent(role: str, prompt: str) -> str:
    """Simulated agent response. Replace with actual LLM call."""
    return f"[{role}]: Completed task based on: {prompt[:50]}..."

def make_agent(role: str, system_prompt: str = "", model: str = "claude-sonnet-5-5"):
    """
    Factory: creates a simple agent function.
    Each agent is specialized by its system_prompt.
    """
    import anthropic
    client = anthropic.Anthropic()

    def agent(user_input: str) -> str:
        messages = [{"role": "user", "content": user_input}]
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            system=system_prompt or f"You are a {role}. Be concise.",
            messages=messages
        )
        return response.content[0].text

    agent.__name__ = role
    return agent


# ═══════════════════════════════════════════════════════════
# TEMPLATE 1: Sequential Pipeline
# ═══════════════════════════════════════════════════════════
def sequential_pipeline(topic: str, use_api: bool = False) -> dict:
    """
    Sequential pipeline: Research → Outline → Write → Edit
    Each agent's output becomes the next agent's input.

    Pattern: agent2(agent1(agent0(input)))
    Use when: clear sequential stages, each builds on previous
    """
    if use_api:
        researcher = make_agent("Researcher",
            "Find key facts, statistics, and recent developments on any topic. Be factual.")
        outliner = make_agent("Outliner",
            "Create structured outlines for articles. Use clear sections with bullet points.")
        writer = make_agent("Writer",
            "Write engaging, clear articles based on outlines provided. 300-500 words.")
        editor = make_agent("Editor",
            "Polish and improve article drafts. Fix grammar, improve flow, enhance clarity.")
    else:
        # Simulated (no API)
        researcher = lambda x: f"[Research]: Key facts about {topic}: fact1, fact2, fact3"
        outliner   = lambda x: f"[Outline]: 1. Intro 2. Main Points 3. Conclusion"
        writer     = lambda x: f"[Draft]: Article about {topic} based on outline..."
        editor     = lambda x: f"[Final]: Polished article about {topic}..."

    print(f"\n=== Sequential Pipeline: {topic} ===")

    # Stage 1: Research
    print("Stage 1: Researching...")
    research = researcher(f"Research this topic thoroughly: {topic}")
    print(f"  Research: {research[:60]}...")

    # Stage 2: Outline (uses research)
    print("Stage 2: Creating outline...")
    outline = outliner(f"Create article outline based on this research:\n{research}")
    print(f"  Outline: {outline[:60]}...")

    # Stage 3: Write (uses outline)
    print("Stage 3: Writing draft...")
    draft = writer(f"Write an article based on this outline:\n{outline}")
    print(f"  Draft: {draft[:60]}...")

    # Stage 4: Edit (uses draft)
    print("Stage 4: Editing...")
    final = editor(f"Polish this draft:\n{draft}")
    print(f"  Final: {final[:60]}...")

    return {
        "research": research,
        "outline":  outline,
        "draft":    draft,
        "final":    final
    }


# ═══════════════════════════════════════════════════════════
# TEMPLATE 2: Hierarchical (Supervisor/Worker)
# ═══════════════════════════════════════════════════════════
def hierarchical_supervisor(task: str, use_api: bool = False) -> str:
    """
    Supervisor routes tasks to specialized workers.
    Workers are defined as tools — supervisor calls them as needed.

    Pattern: supervisor + workers_as_tools
    Use when: complex tasks with unknown/variable subtasks
    """
    if not use_api:
        print(f"\n=== Hierarchical Supervisor: {task[:50]} ===")
        print("  Supervisor: analyzing task...")
        print("  → Calling: researcher('key facts needed')")
        print("  → Result: [Research findings]")
        print("  → Calling: writer('draft from research')")
        print("  → Result: [Draft content]")
        print("  Supervisor: combining results...")
        return f"[Supervisor final answer for: {task[:50]}]"

    import anthropic
    client = anthropic.Anthropic()

    # Workers as actual functions
    def researcher_worker(query: str) -> str:
        r = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=500,
            system="You are a researcher. Find key facts and information.",
            messages=[{"role": "user", "content": query}]
        )
        return r.content[0].text

    def writer_worker(content: str) -> str:
        r = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=500,
            system="You are a writer. Create clear, engaging content.",
            messages=[{"role": "user", "content": content}]
        )
        return r.content[0].text

    def fact_checker_worker(text: str) -> str:
        r = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=300,
            system="You are a fact checker. Verify claims and flag any inaccuracies.",
            messages=[{"role": "user", "content": f"Fact check this:\n{text}"}]
        )
        return r.content[0].text

    # Workers as tools (supervisor calls these)
    WORKER_TOOLS = [
        {
            "name": "researcher",
            "description": "Find accurate information on any topic. Use first to gather facts.",
            "input_schema": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        },
        {
            "name": "writer",
            "description": "Draft and write content based on provided information.",
            "input_schema": {
                "type": "object",
                "properties": {"content": {"type": "string"}},
                "required": ["content"]
            }
        },
        {
            "name": "fact_checker",
            "description": "Verify accuracy of written content. Use before finalizing.",
            "input_schema": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"]
            }
        }
    ]

    SUPERVISOR_SYSTEM = (
        "You are a supervisor with access to specialized workers: "
        "researcher, writer, fact_checker. "
        "Analyze the task and call workers in the right order. "
        "When complete, provide the final answer directly."
    )

    messages = [{"role": "user", "content": task}]
    registry = {"researcher": researcher_worker, "writer": writer_worker,
                "fact_checker": fact_checker_worker}

    for _ in range(10):  # max 10 supervisor iterations
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=2000,
            system=SUPERVISOR_SYSTEM,
            tools=WORKER_TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  → Supervisor calls: {block.name}")
                    result = registry[block.name](**block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })
            messages.append({"role": "user", "content": results})

    return "Max iterations reached."


# ═══════════════════════════════════════════════════════════
# TEMPLATE 3: Parallel Fan-Out
# ═══════════════════════════════════════════════════════════
async def parallel_fan_out_async(tasks: list[str],
                                  model: str = "claude-haiku-5-5") -> list[str]:
    """
    Run multiple agents in parallel using asyncio.gather.
    N tasks take the same time as 1 task.

    Pattern: asyncio.gather(*[agent(x) for x in tasks])
    Use when: same operation on many independent inputs
    """
    import anthropic, asyncio
    client = anthropic.AsyncAnthropic()

    async def call_once(prompt: str) -> str:
        response = await client.messages.create(
            model=model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    # All tasks run simultaneously ← the fan-out
    results = await asyncio.gather(*[call_once(t) for t in tasks])
    return list(results)


def parallel_fan_out(tasks: list[str], use_api: bool = False) -> list[str]:
    """
    Synchronous wrapper for parallel_fan_out_async.
    Call this from non-async code.
    """
    import asyncio

    if not use_api:
        print(f"\n=== Parallel Fan-Out: {len(tasks)} tasks ===")
        print(f"  Running {len(tasks)} agents simultaneously...")
        results = [f"[Result {i+1}: {t[:30]}...]" for i, t in enumerate(tasks)]
        print(f"  All {len(tasks)} completed (parallel time = 1 agent's time)")
        return results

    return asyncio.run(parallel_fan_out_async(tasks))


# ═══════════════════════════════════════════════════════════
# TEMPLATE 4: Critic-Actor (Quality Loop)
# ═══════════════════════════════════════════════════════════
def critic_actor(task: str, max_rounds: int = 3, use_api: bool = False) -> dict:
    """
    Actor produces draft. Critic reviews. Loop until approved.

    Pattern: for round in max_rounds: draft → critique → revise
    Use when: output quality is critical (legal, medical, finance)
    """
    if not use_api:
        print(f"\n=== Critic-Actor: {task[:50]} ===")
        draft = f"[Initial draft about: {task[:30]}]"
        print(f"  Initial draft: {draft}")
        print("  Round 1 - Critic: needs more detail and specific examples")
        draft = f"[Improved draft with details: {task[:30]}]"
        print(f"  Revised: {draft}")
        print("  Round 2 - Critic: Approved! Quality meets standards.")
        return {"final": draft, "rounds": 2}

    import anthropic
    client = anthropic.Anthropic()

    actor_system  = "You are a skilled writer. Produce high-quality drafts."
    critic_system = (
        "You are a strict quality reviewer. "
        "List specific improvements needed, OR write 'APPROVED' if the draft meets standards. "
        "Be specific about what needs to change."
    )

    def actor(prompt: str) -> str:
        r = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=1000,
            system=actor_system,
            messages=[{"role": "user", "content": prompt}]
        )
        return r.content[0].text

    def critic(draft: str) -> str:
        r = client.messages.create(
            model="claude-sonnet-5-5", max_tokens=500,
            system=critic_system,
            messages=[{"role": "user", "content": f"Review this draft:\n{draft}"}]
        )
        return r.content[0].text

    print(f"\n=== Critic-Actor: {task[:50]} ===")

    # Initial draft
    draft = actor(f"Complete this task: {task}")
    print(f"  Initial draft ({len(draft)} chars)")

    for round_num in range(max_rounds):
        critique = critic(draft)
        print(f"  Round {round_num + 1} critique: {critique[:80]}...")

        if "APPROVED" in critique.upper():
            print(f"  → Approved after {round_num + 1} rounds!")
            return {"final": draft, "rounds": round_num + 1}

        # Actor revises based on critique
        draft = actor(
            f"Revise this draft based on the critique:\n\n"
            f"Draft:\n{draft}\n\n"
            f"Critique:\n{critique}"
        )
        print(f"  Revised ({len(draft)} chars)")

    print(f"  → Max rounds ({max_rounds}) reached.")
    return {"final": draft, "rounds": max_rounds}


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Agent Pattern Templates — Demo (Simulated)")
    print("=" * 60)

    # Template 1: Sequential
    result1 = sequential_pipeline("quantum computing", use_api=False)
    print()

    # Template 2: Hierarchical
    result2 = hierarchical_supervisor("Write a report on AI safety", use_api=False)
    print()

    # Template 3: Parallel
    tasks = [
        "Summarize the history of Python",
        "Explain quantum entanglement simply",
        "What is the difference between ML and AI?"
    ]
    result3 = parallel_fan_out(tasks, use_api=False)
    print()

    # Template 4: Critic-Actor
    result4 = critic_actor("Write a product description for a smart water bottle", use_api=False)
    print()

    print("=" * 60)
    print("Pattern Summary:")
    print("  Sequential:   agent1 → agent2 → agent3 (staged pipeline)")
    print("  Hierarchical: supervisor → workers as tools → combine")
    print("  Parallel:     asyncio.gather(all agents simultaneously)")
    print("  Critic-Actor: draft → critique → revise → repeat")
    print()
    print("To use with real API: set use_api=True and ANTHROPIC_API_KEY in .env")
