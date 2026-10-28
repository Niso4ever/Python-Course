"""
═══════════════════════════════════════════════════════════════════
LESSON 15 CHEATSHEET: Multi-Agent Patterns
═══════════════════════════════════════════════════════════════════
Sequential, Hierarchical, Parallel, Critic-Actor, CrewAI.
═══════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════
# 1. THE FOUR PATTERNS (Quick Reference)
# ═══════════════════════════════════════════════════════════
"""
SEQUENTIAL:     agent2.run(agent1.run(agent0.run(topic)))
                → each agent's output = next agent's input

HIERARCHICAL:   supervisor(task) → supervisor calls workers as tools
                → supervisor decides who does what

PARALLEL:       asyncio.gather(agent1(x), agent2(x), agent3(x))
                → all run at same time; N tasks take 1 task's time

CRITIC-ACTOR:   for round in max_rounds:
                    draft = actor.run(task)
                    critique = critic.run(draft)
                    if approved: break
                → self-improving quality loop
"""

# ═══════════════════════════════════════════════════════════
# 2. PATTERN RECOGNITION GUIDE
# ═══════════════════════════════════════════════════════════
"""
You see                                   You understand
──────────────────────────────────────    ──────────────────────────────────────
agent2.run(agent1.run(...))               Sequential pipeline
agent_n.run(previous_output)              Sequential stage
supervisor + tools=WORKER_TOOLS           Hierarchical (workers as tools)
asyncio.gather(*[agent(x) for x in ...]) Parallel fan-out
for round in range(max_rounds): critic   Critic-actor quality loop
Agent + Task + Crew + crew.kickoff()     CrewAI framework
Process.sequential                       CrewAI sequential pipeline
Process.hierarchical + manager_agent     CrewAI supervisor pattern
self.state = {} shared across methods    Shared state communication
tasks_output / intermediate_steps        Full agent trace (debug)
max_rounds=N                             Critic-actor iteration limit
max_iterations=N in supervisor loop      Hierarchical safety limit
"""

# ═══════════════════════════════════════════════════════════
# 3. CREWAI MINIMAL SKELETON
# ═══════════════════════════════════════════════════════════
"""
from crewai import Agent, Task, Crew, Process

agent = Agent(
    role="...",        # job title
    goal="...",        # what to achieve
    backstory="...",   # context for LLM personality
    tools=[],          # optional tools (L11 pattern)
    verbose=True
)

task = Task(
    description="...",       # what to do
    agent=agent,             # who does it
    expected_output="..."    # what the output looks like
)

crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,   # or Process.hierarchical
    verbose=True
)

result = crew.kickoff(inputs={"key": "value"})
print(result.raw)            # final answer
print(result.tasks_output)   # each agent's work
"""

# ═══════════════════════════════════════════════════════════
# 4. PARALLEL FAN-OUT SKELETON
# ═══════════════════════════════════════════════════════════
"""
import asyncio, anthropic

async def call_agent(prompt: str) -> str:
    client   = anthropic.AsyncAnthropic()
    response = await client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

async def fan_out(tasks: list[str]) -> list[str]:
    return await asyncio.gather(*[call_agent(t) for t in tasks])
    #                           ↑ all run simultaneously

# Run:
results = asyncio.run(fan_out(["task1", "task2", "task3"]))
"""

# ═══════════════════════════════════════════════════════════
# 5. CRITIC-ACTOR SKELETON
# ═══════════════════════════════════════════════════════════
"""
def critic_actor(task: str, max_rounds: int = 3) -> str:
    draft = actor_agent.run(task)

    for _ in range(max_rounds):
        critique = critic_agent.run(f"Review and list flaws:\n{draft}")

        if "approved" in critique.lower():
            break

        draft = actor_agent.run(f"Revise based on:\n{critique}\n\nDraft:\n{draft}")

    return draft
"""

# ═══════════════════════════════════════════════════════════
# 6. WHEN TO USE WHICH PATTERN
# ═══════════════════════════════════════════════════════════
"""
Task has clear stages (research → write → edit)
  → Sequential Pipeline

Task has unknown/variable subtasks
  → Hierarchical (supervisor decides dynamically)

Same task on many inputs (10 translations, 5 analyses)
  → Parallel Fan-Out (asyncio.gather)

Output quality is critical (legal, medical, financial)
  → Critic-Actor (iterate to quality)

Using a Python framework
  → CrewAI (wraps any pattern above)
"""

# ═══════════════════════════════════════════════════════════
# 7. COMMON MULTI-AGENT MISTAKES
# ═══════════════════════════════════════════════════════════
"""
MISTAKE 1: Over-engineering with many agents for simple tasks
  FIX: Start with one agent. Add more only when quality ceiling reached.

MISTAKE 2: No safety limits on loops (supervisor/critic-actor)
  while True: supervisor calls workers   ← may loop forever
  FIX: max_iterations=5, max_rounds=3

MISTAKE 3: Sequential when parallel possible
  result1 = agent(task1)    ← 5 seconds
  result2 = agent(task2)    ← 5 more seconds = 10s total
  FIX: asyncio.gather(agent(task1), agent(task2))  → 5s

MISTAKE 4: Missing context injection in sequential pipeline
  stage2.run("write now")   ← stage 2 doesn't know what to write about!
  FIX: stage2.run(f"Write about:\n{stage1_result}")

MISTAKE 5: Critic always finds flaws → infinite revision
  critic never says "approved" → loop runs max_rounds every time
  FIX: Explicit approval criterion in critic's system prompt
"""

print("Multi-agent cheatsheet loaded!")
print("Key patterns: Sequential → Hierarchical → Parallel → Critic-Actor")
print("CrewAI = clean framework wrapping all patterns.")
