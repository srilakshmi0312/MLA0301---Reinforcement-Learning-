# Task 4: Epsilon-Greedy Multi-Armed Bandit
# MLA03 - Reinforcement Learning - Assignment 1

import numpy as np 

def run_bandit():
    np.random.seed(7) 
    true_rewards = [1.0, 1.5, 2.0, 1.2] # illustrative reward means 
    n_arms = len(true_rewards) 
    epsilon = 0.1 
    steps = 1000 
    counts = np.zeros(n_arms) 
    estimates = np.zeros(n_arms) 
    total_reward = 0.0 

    for step in range(steps): 
        # TODO 1: Explore with probability epsilon; otherwise exploit the arm with highest estimate
        if np.random.rand() < epsilon: 
            action = np.random.randint(n_arms) 
        else: 
            action = int(np.argmax(estimates)) 
        
        # Simulated reward with Gaussian noise 
        reward = np.random.normal(true_rewards[action], 1.0) 
        
        # TODO 2: Update the selected arm's count
        counts[action] += 1
        
        # TODO 3: Update its estimated average reward incrementally
        estimates[action] += (reward - estimates[action]) / counts[action]
        
        # TODO 4: Add reward to total_reward
        total_reward += reward

    print("Arm selections:", counts.astype(int)) 
    print("Estimated rewards:", np.round(estimates, 3)) 
    print("Average reward:", round(total_reward / steps, 3))

if __name__ == "__main__":
    run_bandit()

