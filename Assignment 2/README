# MLA03 – Reinforcement Learning: Assignment 2 (CO2)
## Intelligent Autonomous Robot Navigation and Path Optimization System Using Dynamic Programming, Monte Carlo Methods, Temporal-Difference Learning, and Deep Q-Networks

**Course:** MLA03 – Reinforcement Learning  
**Course Outcome:** CO2 – Apply Dynamic Programming methods to solve reinforcement learning problems and derive optimal policies for decision-making tasks  
**Maximum Marks:** 50 Marks  
**Assessment Nature:** Individual Implementation & Analytical Evaluation (Bloom's Levels: K3, K4, K5)  

---

## 1. Project Overview & Problem Context
In automated e-commerce fulfilment centres, autonomous mobile robots (AMRs) transport packages between storage racks and packing bays. Traditional shortest-path algorithms (BFS, Dijkstra, A*) fail under runtime variations such as unpredictable obstacle blockages, dynamic corridor congestion, and wheel slippage. 

This repository provides an end-to-end Reinforcement Learning solution spanning:
1. **Task 1 (K4):** Formal Markov Decision Process (MDP) modeling for 5×5 grid warehouse navigation.
2. **Task 2 (K3/K4):** Policy Iteration and Value Iteration on a 5-state inventory picking robot, plus code completion for Value Iteration.
3. **Task 3 (K4):** Monte Carlo prediction vs. TD(0) learning, including step-by-step mathematical calculations.
4. **Task 4 (K4):** Comparative evaluation of SARSA, Q-Learning, and Deep Q-Networks (DDQN, Dueling DQN, PER) with numerical proofs.
5. **Task 5 (K5):** Full simulation and comparative evaluation across Value Iteration, SARSA, and Q-Learning over 500 episodes with quantitative metrics and trajectory visualizations.

---

## 2. Directory Structure
```
rl_assignment1/
│
├── MLA03_RL_Assignment 2.docx               # Original Assignment Specification Document
├── MLA03_RL_Assignment 2_Answer_Document.docx# Generated Full Solution Document (Identical Format)
├── MLA03_RL_Assignment_2_Solutions.docx      # Duplicate Mirror Copy
│
├── run_experiments.py                       # Complete Python simulation & experimental script
├── build_complete_answer_doc.py             # Script that constructs the Word answer document
│
├── figures/                                 # High-resolution experimental and architecture figures
│   ├── fig1_learning_curves.png             # Training episode vs accumulated reward curves
│   ├── fig2_steps_convergence.png           # Navigation steps to destination per episode
│   ├── fig3_warehouse_grid_paths.png        # 5x5 Grid map with VI, SARSA, and QL trajectories
│   ├── fig4_algorithm_comparison_metrics.png# Grouped bar chart of performance metrics
│   ├── fig5_system_architecture.png         # End-to-end System Architecture diagram
│   └── fig6_dqn_dueling_per.png             # Dueling Double DQN with PER architecture diagram
│
└── README.md                                # Execution guide, parameter tables, and results
```

---

## 3. Environment & Prerequisites
- **Python Version:** 3.12 (or 3.10+)
- **Core Libraries:**
  - `numpy >= 1.24.0`
  - `matplotlib >= 3.7.0`
  - `python-docx >= 1.1.0`

### Installation
```bash
pip install numpy matplotlib python-docx
```

---

## 4. How to Run the Experiments & Regenerate the Answer Document

### Run Reinforcement Learning Experiments & Generate Plots
```bash
python run_experiments.py
```
This executes:
- Value Iteration and Policy Iteration on the 5-state inventory picking MDP.
- Value Iteration, SARSA, and Q-Learning on the 5×5 warehouse grid environment across 500 episodes.
- Generates all publication-grade figures in the `figures/` directory.

### Generate the Word Answer Document
```bash
python build_complete_answer_doc.py
```
This compiles `MLA03_RL_Assignment 2_Answer_Document.docx` formatted identically to the assignment document, complete with all mathematical derivations, styled comparison tables, code listings, execution logs, and embedded figures.

---

## 5. Experimental Summary & Key Results

| Metric | Dynamic Programming (VI) | SARSA (On-Policy TD) | Q-Learning (Off-Policy TD) |
|---|:---:|:---:|:---:|
| **Success Rate (Final 50 Ep)** | 100.0% | 100.0% | 100.0% |
| **Optimal Path Length** | 8 Steps | 8 Steps | 8 Steps |
| **Mean Reward (Final 50 Ep)** | +42.00 | +41.22 | +41.08 |
| **Convergence Epoch** | 9 Iterations | ~280 Episodes | ~210 Episodes |
| **Path Trajectory Characteristic** | Deterministic boundary | Safe clearance (outer aisle) | Shortest interior risk line |
| **Training Collisions** | 0 | Very Low (0.4%) | Moderate (2.8%) |

---

## 6. Numerical Proofs Summary

### Task 2 – Value Iteration Code Completion Output:
- Converged in: **3 iterations**
- State Values: `V = [8.0, 10.0, 0.0]`
- Optimal Policy: `State 0: Move Forward (0)`, `State 1: Move Forward (0)`

### Task 3 – TD(0) Calculation:
- Given: $V(S_t)=5.0$, $R_{t+1}=3.0$, $V(S_{t+1})=8.0$, $\alpha=0.2$, $\gamma=0.9$
- TD Target: $3.0 + 0.9(8.0) = 10.20$
- TD Error: $\delta = 10.20 - 5.00 = +5.20$
- Updated Value: $V(S_t) \leftarrow 5.00 + 0.2(5.20) = \mathbf{6.04}$

### Task 4 – SARSA vs. Q-Learning Numerical Calculation:
- Given: $Q(s, a) = 5.0$, $R = 4.0$, $\alpha = 0.2$, $\gamma = 0.9$, $Q(s', a') = 6.0$, $\max_{a'} Q(s', a') = 8.0$
- **SARSA:** $Q_{\text{SARSA}} = 5.0 + 0.2 [4.0 + 0.9(6.0) - 5.0] = \mathbf{5.88}$
- **Q-Learning:** $Q_{\text{QL}} = 5.0 + 0.2 [4.0 + 0.9(8.0) - 5.0] = \mathbf{6.24}$
- **Finding:** $Q_{\text{QL}} > Q_{\text{SARSA}}$ because Q-Learning assumes optimal future actions, while SARSA incorporates exploratory policy risks.
