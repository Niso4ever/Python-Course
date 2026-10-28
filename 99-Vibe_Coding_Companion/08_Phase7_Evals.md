# Phase 7 — Evals & Testing (Ph7-L01, 1 template)

Tier 2 of the landscape: benchmarking how well an agent performs and learns across multiple instances. These prompts rely heavily on **Mode 2 (Specification)** and **Mode 3 (Iteration)** to ensure you are actually measuring what you think you're measuring.

---

## 54. `template_agent_eval.py` — Ph7-L01 Agent Eval Pipeline
**Level 3 (Contract) · Mode 5 (Integration)** — Measuring if an agent learns over time.

#### 📝 VIBE PROMPT
```
CONSTRAINTS: Build an eval pipeline to compare a simulated learning agent against a stateless baseline over 10 task instances.
REQUEST: Run the baseline agent and collect rewards. Run the learning agent and collect rewards. Calculate the mean reward, loss curve, and performance gain of the learner over the baseline.
VALIDATION: The output includes a loss curve showing improvement over the 10 instances, and computes a positive gain demonstrating that memory helps.
```
#### 💻 PRODUCES (essence)
```python
for i in range(num_instances):
    reward = agent.respond(query)
    outcomes.append(InstanceOutcome(reward=reward))

metrics = calculate_metrics(outcomes)
gain = learner_metrics.mean_reward - baseline_metrics.mean_reward
```
