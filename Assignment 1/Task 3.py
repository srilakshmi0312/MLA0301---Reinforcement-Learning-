# Task 3: Bellman One-Step Value Calculation
# MLA03 - Reinforcement Learning - Assignment 1

gamma = 0.8 
# Two possible next states and their transition probabilities 
probabilities = [0.6, 0.4] 
rewards = [5, -2] 
next_state_values = [10, 4] 

def bellman_return(probabilities, rewards, next_state_values, gamma): 
    total = 0.0 
    for i in range(len(probabilities)): 
        # TODO 1: Calculate the probability-weighted reward 
        weighted_reward = probabilities[i] * rewards[i]
        # TODO 2: Include the discounted next-state value 
        discounted_next = probabilities[i] * gamma * next_state_values[i]
        # TODO 3: Add the contribution to total 
        total += weighted_reward + discounted_next
    return total 

if __name__ == "__main__":
    result = bellman_return(probabilities, rewards, next_state_values, gamma)
    print("Bellman return:", result)

