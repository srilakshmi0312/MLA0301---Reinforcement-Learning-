# MLA03 - Reinforcement Learning: Assignment 1 (CO1)
**Project Title:** Design, Implement and Evaluate an Intelligent Reinforcement Learning Agent for Adaptive Smart Traffic Signal Management Using Markov Decision Processes and Bandit Algorithms

## Student Details
- **Student Name:** [Your Name]
- **Register Number:** [Your Register Number]
- **Course Outcome:** CO1 (Bloom's Levels Assessed: K4 – Analyse & K5 – Evaluate)
- **Repository Name:** MLA03-[RegisterNumber]-Assignment1

---

## Environment & Requirements
- **Python Version:** Python 3.10+
- **Key Libraries:** `numpy`, `python-docx`
- **Installation:**
  ```bash
  pip install numpy python-docx
  ```

---

## Repository Structure
```
├── README.md
├── MLA03_RL_Assignment1_Answers.docx  # Full comprehensive solution document
├── Task01/                            # RL Framework & Problem Analysis
├── Task02/                            # Markov Decision Process Formulation
├── Task03/
│   └── bellman_calc.py                # Completed Bellman One-Step Value Calculation
├── Task04/
│   └── bandit_eps_greedy.py           # Completed ε-Greedy Multi-Armed Bandit
└── Task05/
    └── experiment_evaluation.py       # Comparative Evaluation (Fixed-Time vs Greedy vs ε-Greedy)
```

---

## Execution Commands & Results Summary

### Task 03: Bellman One-Step Value Calculation
```bash
python Task03/bellman_calc.py
```
**Output:**
```
Bellman return: 8.28
```
*Verification:*
- Branch 1: `0.6 * [5 + 0.8 * 10] = 7.80`
- Branch 2: `0.4 * [-2 + 0.8 * 4] = 0.48`
- Total: `7.80 + 0.48 = 8.28`

---

### Task 04: ε-Greedy Multi-Armed Bandit (1000 Steps)
```bash
python Task04/bandit_eps_greedy.py
```
**Output:**
```
Arm selections: [ 17  24 932  27]
Estimated rewards: [1.163 1.306 1.966 0.859]
Average reward: 1.907
```
*Observation:* Optimal Arm 2 is selected 932 times (93.2% convergence).

---

### Task 05: Experimental Evaluation
```bash
python Task05/experiment_evaluation.py
```
**Results:**
| Strategy | Arm Selection Distribution | Optimal Arm % | Average Reward | Congestion Reduction |
|---|---|---|---|---|
| Fixed-Time Baseline | [250, 250, 250, 250] | 25.0% | 1.444 | Baseline (0%) |
| Greedy Strategy (ε=0) | [1, 1, 995, 3] | 99.5% | 2.015 | +39.5% improvement |
| ε-Greedy Strategy (ε=0.1) | [17, 24, 932, 27] | 93.2% | 1.907 | +32.1% improvement |

---
## Main Document
The complete answer document with all explanations, mathematical derivations, complexity analysis, system architecture, pseudocode, and rubric alignment is saved as:
**`MLA03_RL_Assignment1_Answers.docx`**

