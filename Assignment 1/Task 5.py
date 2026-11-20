# Task 5: Experimental Evaluation of Traffic Signal Strategies
# Fixed-Time Baseline vs. Greedy Bandit vs. Epsilon-Greedy Bandit
# MLA03 - Reinforcement Learning - Assignment 1

import numpy as np

def run_experiment():
    true_rewards = [1.0, 1.5, 2.0, 1.2]  # Arm 2 represents optimal green timing split
    n_arms = len(true_rewards)
    steps = 1000

    print("=" * 65)
    print("TASK 5: TRAFFIC SIGNAL CONTROLLER COMPARATIVE EXPERIMENT")
    print("=" * 65)

    # 1. Fixed-time baseline (Cyclic / Round-robin schedule)
    np.random.seed(42)
    fixed_counts = np.zeros(n_arms)
    fixed_total = 0.0
    for step in range(steps):
        action = step % n_arms
        reward = np.random.normal(true_rewards[action], 1.0)
        fixed_counts[action] += 1
        fixed_total += reward
    print(f"Fixed-Time Baseline | Arm Selections: {fixed_counts.astype(int)} | Avg Reward: {round(fixed_total/steps, 3)}")

    # 2. Greedy Strategy (epsilon = 0 with 1 initial sample per arm)
    np.random.seed(42)
    greedy_counts = np.zeros(n_arms)
    greedy_estimates = np.zeros(n_arms)
    greedy_total = 0.0
    for step in range(steps):
        if step < n_arms:
            action = step
        else:
            action = int(np.argmax(greedy_estimates))
        reward = np.random.normal(true_rewards[action], 1.0)
        greedy_counts[action] += 1
        greedy_estimates[action] += (reward - greedy_estimates[action]) / greedy_counts[action]
        greedy_total += reward
    print(f"Greedy Strategy     | Arm Selections: {greedy_counts.astype(int)} | Avg Reward: {round(greedy_total/steps, 3)} | Final Estimates: {np.round(greedy_estimates, 3)}")

    # 3. Epsilon-Greedy Strategy (epsilon = 0.1)
    np.random.seed(7)
    eps_counts = np.zeros(n_arms)
    eps_estimates = np.zeros(n_arms)
    eps_total = 0.0
    for step in range(steps):
        if np.random.rand() < 0.1:
            action = np.random.randint(n_arms)
        else:
            action = int(np.argmax(eps_estimates))
        reward = np.random.normal(true_rewards[action], 1.0)
        eps_counts[action] += 1
        eps_estimates[action] += (reward - eps_estimates[action]) / eps_counts[action]
        eps_total += reward
    print(f"Epsilon-Greedy (0.1)| Arm Selections: {eps_counts.astype(int)} | Avg Reward: {round(eps_total/steps, 3)} | Final Estimates: {np.round(eps_estimates, 3)}")
    print("=" * 65)

if __name__ == "__main__":
    run_experiment()

