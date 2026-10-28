"""
Template: Agent Eval Pipeline
=============================
A runnable demonstration of an agent evaluation pipeline.
It compares a "stateless" baseline agent against a "learning" agent
over 10 instances, tracking rewards and calculating the gain.

Usage:
    python template_agent_eval.py

2026 Note: This uses simulated agents to demonstrate the evaluation
math and structure without requiring API keys.
"""

import random
import statistics
from dataclasses import dataclass
from typing import Optional


# ─── 1. Data Structures ─────────────────────────────────────

@dataclass
class InstanceOutcome:
    instance_id: str
    instance_index: int
    reward: float
    success: Optional[bool] = None


@dataclass
class EvalMetrics:
    loss_curve: list[float]
    mean_reward: float
    std_reward: float
    is_improving: bool


# ─── 2. Simulated Agents ────────────────────────────────────

class BaselineAgent:
    """An agent that has no memory. It performs roughly the same every time."""
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.base_skill = 0.4

    def reset(self):
        pass  # Nothing to reset, it has no memory

    def respond(self, query: str) -> float:
        # Performance fluctuates randomly around base_skill
        return min(1.0, max(0.0, self.base_skill + self.rng.uniform(-0.15, 0.15)))


class LearningAgent:
    """An agent with memory. It learns from feedback and improves."""
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.skill = 0.4  # Starts at same skill level as baseline

    def reset(self):
        self.skill = 0.4  # Reset learning back to 0

    def respond(self, query: str) -> float:
        reward = min(1.0, max(0.0, self.skill + self.rng.uniform(-0.1, 0.1)))
        # The agent learns! Skill goes up after each turn.
        self.skill += 0.05
        return reward


# ─── 3. The Eval Runner ─────────────────────────────────────

def run_evaluation(agent, num_instances: int = 10) -> list[InstanceOutcome]:
    """Run an agent through a sequence of task instances."""
    outcomes = []
    
    # Crucial: Reset the agent BEFORE the run begins
    agent.reset()

    for i in range(num_instances):
        query = f"Task instance {i}"
        
        # 1. Agent responds
        reward = agent.respond(query)
        
        # 2. Collect outcome
        outcomes.append(InstanceOutcome(
            instance_id=f"inst_{i}",
            instance_index=i,
            reward=round(reward, 3),
            success=reward > 0.6
        ))
        
        # (In a real system, you'd send feedback back to the agent here)
        
    return outcomes


def calculate_metrics(outcomes: list[InstanceOutcome]) -> EvalMetrics:
    """Compute standard metrics from a list of outcomes."""
    rewards = [o.reward for o in outcomes]
    
    # Loss is the distance from a perfect score (1.0)
    loss_curve = [round(1.0 - r, 3) for r in rewards]
    
    # Check if the last 3 instances are better than the first 3
    first_third = statistics.mean(rewards[:3])
    last_third = statistics.mean(rewards[-3:])
    
    return EvalMetrics(
        loss_curve=loss_curve,
        mean_reward=round(statistics.mean(rewards), 3),
        std_reward=round(statistics.stdev(rewards), 3) if len(rewards) > 1 else 0.0,
        is_improving=last_third > first_third
    )


# ─── 4. Main Execution ──────────────────────────────────────

def main():
    print("Starting Agent Evaluation Pipeline...\n")
    num_instances = 10

    # 1. Evaluate Baseline (No Memory)
    print("--- Evaluating Baseline Agent (Stateless) ---")
    baseline = BaselineAgent(seed=42)
    baseline_outcomes = run_evaluation(baseline, num_instances)
    baseline_metrics = calculate_metrics(baseline_outcomes)
    
    print(f"Mean Reward: {baseline_metrics.mean_reward}")
    print(f"Loss Curve:  {baseline_metrics.loss_curve}")
    print(f"Improving:   {baseline_metrics.is_improving}\n")

    # 2. Evaluate Learning Agent (Stateful)
    print("--- Evaluating Learning Agent (Stateful) ---")
    learner = LearningAgent(seed=42)
    learner_outcomes = run_evaluation(learner, num_instances)
    learner_metrics = calculate_metrics(learner_outcomes)
    
    print(f"Mean Reward: {learner_metrics.mean_reward}")
    print(f"Loss Curve:  {learner_metrics.loss_curve}")
    print(f"Improving:   {learner_metrics.is_improving}\n")

    # 3. Compute Gain
    print("--- Final Comparison ---")
    gain = round(learner_metrics.mean_reward - baseline_metrics.mean_reward, 3)
    
    print(f"Baseline Score: {baseline_metrics.mean_reward}")
    print(f"Learner Score:  {learner_metrics.mean_reward}")
    print(f"Gain:          {'+' if gain > 0 else ''}{gain}")
    
    if gain > 0 and learner_metrics.is_improving:
        print("\n✅ Conclusion: The learning mechanism is working effectively!")
    else:
        print("\n❌ Conclusion: The agent is not learning from experience.")


if __name__ == "__main__":
    main()
