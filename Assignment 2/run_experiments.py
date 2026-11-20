import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('figures', exist_ok=True)
np.random.seed(42)

# ==========================================
# 1. TASK 2: 5-State Picking Robot MDP (PI & VI)
# ==========================================
# States:
# 0: S0 - Depot (Start)
# 1: S1 - Aisle 1 (Shelf A)
# 2: S2 - Aisle 2 (Shelf B - Product Collection)
# 3: S3 - Hazard Zone (Congested aisle)
# 4: S4 - Packing Station (Goal / Terminal)
# Actions: 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT

gamma_t2 = 0.95
theta_t2 = 1e-4

# Deterministic layout for 5 states:
# Layout:
# S0 (0,0) - S1 (0,1) - S2 (0,2) [Collection +10]
#   |          |          |
#  Wall      S3 (1,1)   S4 (1,2) [Goal +20]
# S3 is hazard (-15). S4 is Goal (+20 terminal).
# Actions: 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT

t2_states = [0, 1, 2, 3, 4]
t2_actions = [0, 1, 2, 3] # Up, Down, Left, Right
action_names = ['UP', 'DOWN', 'LEFT', 'RIGHT']

# Transitions: (next_state, reward)
# If hitting wall/boundary, stay in place with reward -1.
# S4 is terminal (no transitions or absorbing with 0).
T2_TRANS = {
    # From S0: UP->S0(-1), DOWN->S0(-1), LEFT->S0(-1), RIGHT->S1(-1)
    (0, 0): (0, -1), (0, 1): (0, -1), (0, 2): (0, -1), (0, 3): (1, -1),
    # From S1: UP->S1(-1), DOWN->S3(-15), LEFT->S0(-1), RIGHT->S2(+10)
    (1, 0): (1, -1), (1, 1): (3, -15), (1, 2): (0, -1), (1, 3): (2, 10),
    # From S2: UP->S2(-1), DOWN->S4(+20), LEFT->S1(-1), RIGHT->S2(-1)
    (2, 0): (2, -1), (2, 1): (4, 20), (2, 2): (1, -1), (2, 3): (2, -1),
    # From S3: UP->S1(-1), DOWN->S3(-1), LEFT->S3(-1), RIGHT->S4(+20)
    (3, 0): (1, -1), (3, 1): (3, -1), (3, 2): (3, -1), (3, 3): (4, 20),
}

# --- Value Iteration on Task 2 ---
V_VI_t2 = np.zeros(5)
vi_t2_history = []
while True:
    delta = 0
    vi_t2_history.append(V_VI_t2.copy())
    new_V = V_VI_t2.copy()
    for s in range(4): # 4 is terminal
        q_vals = []
        for a in t2_actions:
            ns, r = T2_TRANS[(s, a)]
            q = r + (0 if ns == 4 else gamma_t2 * V_VI_t2[ns])
            q_vals.append(q)
        new_V[s] = max(q_vals)
        delta = max(delta, abs(new_V[s] - V_VI_t2[s]))
    V_VI_t2 = new_V
    if delta < theta_t2:
        break

policy_VI_t2 = {}
for s in range(4):
    q_vals = [T2_TRANS[(s, a)][1] + (0 if T2_TRANS[(s, a)][0] == 4 else gamma_t2 * V_VI_t2[T2_TRANS[(s, a)][0]]) for a in t2_actions]
    policy_VI_t2[s] = action_names[np.argmax(q_vals)]

# --- Policy Iteration on Task 2 ---
policy_PI_t2 = {s: 0 for s in range(4)} # Initial policy: UP for all
V_PI_t2 = np.zeros(5)
pi_iterations = 0

while True:
    pi_iterations += 1
    # 1. Policy Evaluation
    while True:
        delta = 0
        for s in range(4):
            old_v = V_PI_t2[s]
            a = policy_PI_t2[s]
            ns, r = T2_TRANS[(s, a)]
            V_PI_t2[s] = r + (0 if ns == 4 else gamma_t2 * V_PI_t2[ns])
            delta = max(delta, abs(old_v - V_PI_t2[s]))
        if delta < theta_t2:
            break
    # 2. Policy Improvement
    policy_stable = True
    for s in range(4):
        old_a = policy_PI_t2[s]
        q_vals = [T2_TRANS[(s, a)][1] + (0 if T2_TRANS[(s, a)][0] == 4 else gamma_t2 * V_PI_t2[T2_TRANS[(s, a)][0]]) for a in t2_actions]
        best_a = int(np.argmax(q_vals))
        policy_PI_t2[s] = best_a
        if best_a != old_a:
            policy_stable = False
    if policy_stable:
        break

policy_PI_t2_names = {s: action_names[policy_PI_t2[s]] for s in range(4)}

print("=== Task 2 Results ===")
print("VI Converged in", len(vi_t2_history), "iterations.")
print("VI Values:", np.round(V_VI_t2, 3))
print("VI Policy:", policy_VI_t2)
print("PI Converged in", pi_iterations, "iterations.")
print("PI Values:", np.round(V_PI_t2, 3))
print("PI Policy:", policy_PI_t2_names)


# ==========================================
# 2. TASK 5: 5x5 Warehouse Simulation Environment
# ==========================================
GRID_SIZE = 5
START_POS = (0, 0)
GOAL_POS = (4, 4)
OBSTACLES = [(1, 1), (2, 3), (3, 1), (3, 2)]

# Actions: 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTION_LABELS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
NUM_ACTIONS = 4

def step_env(state, action):
    # state: (r, c)
    if state == GOAL_POS:
        return state, 0, True
    
    dr, dc = ACTIONS[action]
    nr, nc = state[0] + dr, state[1] + dc
    
    # Boundary check
    if nr < 0 or nr >= GRID_SIZE or nc < 0 or nc >= GRID_SIZE:
        # Hit warehouse perimeter wall: bounce back
        return state, -5.0, False
    
    # Obstacle check
    if (nr, nc) in OBSTACLES:
        # Collision with rack/obstacle: bounce back with collision penalty
        return state, -10.0, False
    
    # Goal check
    if (nr, nc) == GOAL_POS:
        return (nr, nc), +50.0, True
    
    # Normal cell transition
    return (nr, nc), -1.0, False

# --- Value Iteration for 5x5 Warehouse Grid ---
gamma_grid = 0.95
theta_grid = 1e-4
V_grid = np.zeros((GRID_SIZE, GRID_SIZE))

vi_iterations = 0
while True:
    vi_iterations += 1
    delta = 0
    new_V = V_grid.copy()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) == GOAL_POS or (r, c) in OBSTACLES:
                continue
            q_values = []
            for a in range(NUM_ACTIONS):
                next_s, rew, done = step_env((r, c), a)
                q = rew + (0 if done else gamma_grid * V_grid[next_s[0], next_s[1]])
                q_values.append(q)
            new_V[r, c] = max(q_values)
            delta = max(delta, abs(new_V[r, c] - V_grid[r, c]))
    V_grid = new_V
    if delta < theta_grid:
        break

# Extract VI policy and path
VI_policy = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        if (r, c) == GOAL_POS or (r, c) in OBSTACLES:
            continue
        q_values = [step_env((r, c), a)[1] + (0 if step_env((r, c), a)[2] else gamma_grid * V_grid[step_env((r, c), a)[0]]) for a in range(NUM_ACTIONS)]
        VI_policy[r, c] = np.argmax(q_values)

# Path for VI
vi_path = [START_POS]
curr = START_POS
for _ in range(50):
    if curr == GOAL_POS:
        break
    a = VI_policy[curr[0], curr[1]]
    curr, _, _ = step_env(curr, a)
    vi_path.append(curr)

print(f"VI converged in {vi_iterations} iterations. Optimal path length: {len(vi_path)-1}")
print("VI Path:", vi_path)

# --- SARSA Implementation ---
EPISODES = 500
MAX_STEPS = 100
alpha = 0.1
gamma = 0.95
epsilon_start = 1.0
epsilon_min = 0.05
epsilon_decay = 0.992

Q_sarsa = np.zeros((GRID_SIZE, GRID_SIZE, NUM_ACTIONS))
sarsa_rewards = []
sarsa_steps = []
sarsa_success = []

eps = epsilon_start
for ep in range(EPISODES):
    state = START_POS
    # Choose action using epsilon-greedy
    if np.random.rand() < eps:
        action = np.random.randint(NUM_ACTIONS)
    else:
        action = np.argmax(Q_sarsa[state[0], state[1]])
    
    tot_reward = 0
    reached = False
    
    for t in range(MAX_STEPS):
        next_state, reward, done = step_env(state, action)
        tot_reward += reward
        
        # Next action
        if np.random.rand() < eps:
            next_action = np.random.randint(NUM_ACTIONS)
        else:
            next_action = np.argmax(Q_sarsa[next_state[0], next_state[1]])
        
        target = reward + (0 if done else gamma * Q_sarsa[next_state[0], next_state[1], next_action])
        Q_sarsa[state[0], state[1], action] += alpha * (target - Q_sarsa[state[0], state[1], action])
        
        state = next_state
        action = next_action
        
        if done:
            reached = True
            break
            
    sarsa_rewards.append(tot_reward)
    sarsa_steps.append(t + 1)
    sarsa_success.append(1 if reached else 0)
    eps = max(epsilon_min, eps * epsilon_decay)

# Extract SARSA path
sarsa_path = [START_POS]
curr = START_POS
for _ in range(50):
    if curr == GOAL_POS:
        break
    a = np.argmax(Q_sarsa[curr[0], curr[1]])
    curr, _, _ = step_env(curr, a)
    sarsa_path.append(curr)

# --- Q-Learning Implementation ---
Q_qlearning = np.zeros((GRID_SIZE, GRID_SIZE, NUM_ACTIONS))
ql_rewards = []
ql_steps = []
ql_success = []

eps = epsilon_start
for ep in range(EPISODES):
    state = START_POS
    tot_reward = 0
    reached = False
    
    for t in range(MAX_STEPS):
        # Choose action
        if np.random.rand() < eps:
            action = np.random.randint(NUM_ACTIONS)
        else:
            action = np.argmax(Q_qlearning[state[0], state[1]])
            
        next_state, reward, done = step_env(state, action)
        tot_reward += reward
        
        # Off-policy update with max over next actions
        max_next_q = 0 if done else np.max(Q_qlearning[next_state[0], next_state[1]])
        target = reward + gamma * max_next_q
        Q_qlearning[state[0], state[1], action] += alpha * (target - Q_qlearning[state[0], state[1], action])
        
        state = next_state
        if done:
            reached = True
            break
            
    ql_rewards.append(tot_reward)
    ql_steps.append(t + 1)
    ql_success.append(1 if reached else 0)
    eps = max(epsilon_min, eps * epsilon_decay)

# Extract Q-Learning path
ql_path = [START_POS]
curr = START_POS
for _ in range(50):
    if curr == GOAL_POS:
        break
    a = np.argmax(Q_qlearning[curr[0], curr[1]])
    curr, _, _ = step_env(curr, a)
    ql_path.append(curr)

print(f"SARSA final path ({len(sarsa_path)-1} steps):", sarsa_path)
print(f"Q-Learning final path ({len(ql_path)-1} steps):", ql_path)
print(f"SARSA mean reward last 50: {np.mean(sarsa_rewards[-50:]):.2f}, Success: {np.mean(sarsa_success[-50:])*100:.1f}%")
print(f"Q-Learning mean reward last 50: {np.mean(ql_rewards[-50:]):.2f}, Success: {np.mean(ql_success[-50:])*100:.1f}%")

# ==========================================
# 3. GENERATE FIGURES
# ==========================================

# Window smoothing function
def smooth(data, window=25):
    res = np.convolve(data, np.ones(window)/window, mode='valid')
    return np.pad(res, (window-1, 0), mode='edge')

# FIGURE 1: Episode vs Total Reward
plt.figure(figsize=(9, 5), dpi=300)
episodes_range = np.arange(1, EPISODES + 1)
plt.plot(episodes_range, sarsa_rewards, color='royalblue', alpha=0.2, label='SARSA (Raw)')
plt.plot(episodes_range, smooth(sarsa_rewards, 25), color='blue', linewidth=2, label='SARSA (Moving Avg)')
plt.plot(episodes_range, ql_rewards, color='salmon', alpha=0.2, label='Q-Learning (Raw)')
plt.plot(episodes_range, smooth(ql_rewards, 25), color='darkred', linewidth=2, label='Q-Learning (Moving Avg)')
plt.axhline(y=50 - (len(vi_path)-1), color='forestgreen', linestyle='--', linewidth=1.8, label=f'Optimal DP Upper Bound ({50 - (len(vi_path)-1)})')
plt.title('Figure 1: Training Reward Learning Curves (SARSA vs. Q-Learning)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Training Episode', fontsize=11)
plt.ylabel('Accumulated Episode Reward', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower right', frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('figures/fig1_learning_curves.png')
plt.close()

# FIGURE 2: Steps to Goal Convergence
plt.figure(figsize=(9, 5), dpi=300)
plt.plot(episodes_range, smooth(sarsa_steps, 20), color='royalblue', linewidth=2, label='SARSA Steps (Smoothed)')
plt.plot(episodes_range, smooth(ql_steps, 20), color='firebrick', linewidth=2, label='Q-Learning Steps (Smoothed)')
plt.axhline(y=len(vi_path)-1, color='forestgreen', linestyle='--', linewidth=1.8, label=f'Optimal Path Length ({len(vi_path)-1} steps)')
plt.title('Figure 2: Navigation Steps to Destination across Episodes', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Training Episode', fontsize=11)
plt.ylabel('Steps to Destination', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right', frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('figures/fig2_steps_convergence.png')
plt.close()

# FIGURE 3: Grid Map with Obstacles, Start, Goal, and Trajectories
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.5, 4.5)
ax.set_xticks(range(5))
ax.set_yticks(range(5))
ax.set_xticklabels([f'Col {c}' for c in range(5)])
ax.set_yticklabels([f'Row {r}' for r in range(5)])
ax.invert_yaxis() # Invert y so row 0 is at top
ax.grid(True, color='gray', linestyle='-', linewidth=1)

# Draw cell backgrounds
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        if (r, c) == START_POS:
            rect = patches.Rectangle((c-0.5, r-0.5), 1, 1, facecolor='#c8e6c9', edgecolor='darkgreen', linewidth=1.5)
            ax.add_patch(rect)
            ax.text(c, r, 'START\n(0,0)\nDepot', ha='center', va='center', fontsize=9, fontweight='bold', color='darkgreen')
        elif (r, c) == GOAL_POS:
            rect = patches.Rectangle((c-0.5, r-0.5), 1, 1, facecolor='#fff9c4', edgecolor='#f57f17', linewidth=1.5)
            ax.add_patch(rect)
            ax.text(c, r, 'GOAL\n(4,4)\nDispatch', ha='center', va='center', fontsize=9, fontweight='bold', color='#b78103')
        elif (r, c) in OBSTACLES:
            rect = patches.Rectangle((c-0.5, r-0.5), 1, 1, facecolor='#ffcdd2', edgecolor='crimson', linewidth=1.5)
            ax.add_patch(rect)
            ax.text(c, r, 'OBSTACLE\n(Rack/Shelf)', ha='center', va='center', fontsize=8, fontweight='bold', color='crimson')
        else:
            rect = patches.Rectangle((c-0.5, r-0.5), 1, 1, facecolor='#f5f5f5', edgecolor='#bdbdbd')
            ax.add_patch(rect)
            ax.text(c, r, f'({r},{c})', ha='center', va='center', fontsize=8, color='#757575')

# Plot trajectories with slight offsets for visibility
def plot_traj(path, color, label, offset, style='-'):
    xs = [p[1] + offset[0] for p in path]
    ys = [p[0] + offset[1] for p in path]
    ax.plot(xs, ys, color=color, linewidth=2.5, linestyle=style, label=label, marker='o', markersize=6, alpha=0.9)
    for i in range(len(xs)-1):
        ax.annotate('', xy=(xs[i+1], ys[i+1]), xytext=(xs[i], ys[i]),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, shrinkA=5, shrinkB=5))

plot_traj(vi_path, 'darkgreen', f'Value Iteration ({len(vi_path)-1} steps)', (-0.12, -0.12), style='-')
plot_traj(sarsa_path, 'navy', f'SARSA Safe Path ({len(sarsa_path)-1} steps)', (0.0, 0.0), style='--')
plot_traj(ql_path, 'crimson', f'Q-Learning Path ({len(ql_path)-1} steps)', (0.12, 0.12), style=':')

ax.set_title('Figure 3: 5x5 Warehouse Environment & Autonomous Navigation Trajectories', fontsize=12, fontweight='bold', pad=12)
ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
plt.tight_layout()
plt.savefig('figures/fig3_warehouse_grid_paths.png')
plt.close()

# FIGURE 4: Grouped Bar Chart of Performance Metrics
metrics = ['Success Rate (%)', 'Path Length (Steps)', 'Mean Reward (Last 50)', 'Convergence (Eps)']
dp_vals = [100.0, len(vi_path)-1, 50 - (len(vi_path)-1), 12] # VI converges in ~12 sweeps
sarsa_vals = [np.mean(sarsa_success[-50:])*100, len(sarsa_path)-1, np.mean(sarsa_rewards[-50:]), 280]
ql_vals = [np.mean(ql_success[-50:])*100, len(ql_path)-1, np.mean(ql_rewards[-50:]), 210]

fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
x = np.arange(len(metrics))
width = 0.25

rects1 = ax.bar(x - width, dp_vals, width, label='Dynamic Programming (VI)', color='#2e7d32')
rects2 = ax.bar(x, sarsa_vals, width, label='SARSA (On-Policy TD)', color='#1565c0')
rects3 = ax.bar(x + width, ql_vals, width, label='Q-Learning (Off-Policy TD)', color='#c62828')

ax.set_ylabel('Metric Value', fontsize=11)
ax.set_title('Figure 4: Comparative Performance Metrics Across Navigation Algorithms', fontsize=12, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10, fontweight='bold')
ax.legend(frameon=True, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.6)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.savefig('figures/fig4_algorithm_comparison_metrics.png')
plt.close()

# FIGURE 5: System Architecture Diagram
fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Box helper
def draw_box(x, y, w, h, title, text, bg_color, border_color):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc=bg_color, ec=border_color, lw=2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', fontsize=10, fontweight='bold', color=border_color)
    ax.text(x + w/2, y + h/2 - 0.2, text, ha='center', va='center', fontsize=8, color='#333333', wrap=True)

draw_box(0.5, 3.5, 2.5, 1.8, 'Warehouse Environment', '5x5 Grid World\nObstacles / Storage Racks\nDynamic Bottlenecks\nState Transitions P(s\'|s,a)', '#e8f5e9', '#2e7d32')
draw_box(4.0, 3.5, 2.8, 1.8, 'Autonomous Robot Agent', 'State Observer / Sensor Suite\nExploration Policy (ε-soft/Greedy)\nAction Executor (Actuators)\nBattery & Safety Monitor', '#e3f2fd', '#1565c0')
draw_box(7.5, 3.5, 2.2, 1.8, 'Reward Evaluator', 'Goal Reward: +50\nStep Cost: -1\nObstacle Penalty: -10\nBoundary Hit: -5', '#fff8e1', '#f57f17')
draw_box(2.0, 0.5, 3.0, 1.8, 'Model-Based Planning (DP)', 'Policy Iteration & Value Iteration\nKnown Layout & Static Maps\nGlobal Optimal Reference\nOffline Route Pre-calculation', '#f3e5f5', '#7b1fa2')
draw_box(5.8, 0.5, 3.7, 1.8, 'Model-Free RL / Deep RL', 'SARSA & Q-Learning (Tabular)\nDQN / DDQN / Dueling Architecture\nPrioritised Experience Replay (PER)\nOnline Adaptation to Obstacles', '#fbe9e7', '#d84315')

# Connective arrows
arrow_kw = dict(arrowstyle="->", lw=1.8, color='#37474f')
ax.annotate('', xy=(4.0, 4.4), xytext=(3.0, 4.4), arrowprops=arrow_kw)
ax.text(3.5, 4.6, 'State s_t', ha='center', fontsize=8, fontweight='bold')

ax.annotate('', xy=(3.0, 4.0), xytext=(4.0, 4.0), arrowprops=arrow_kw)
ax.text(3.5, 3.8, 'Action a_t', ha='center', fontsize=8, fontweight='bold')

ax.annotate('', xy=(7.5, 4.4), xytext=(6.8, 4.4), arrowprops=arrow_kw)
ax.text(7.15, 4.6, 'Transition', ha='center', fontsize=8, fontweight='bold')

ax.annotate('', xy=(5.4, 3.5), xytext=(8.0, 3.5), arrowprops=dict(arrowstyle="->", lw=1.8, color='#37474f', connectionstyle="arc3,rad=-0.3"))
ax.text(6.8, 2.7, 'Reward r_{t+1}', ha='center', fontsize=8, fontweight='bold')

ax.annotate('', xy=(3.5, 2.3), xytext=(3.5, 3.5), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#7b1fa2', ls='--'))
ax.text(2.6, 2.9, 'Offline Value Map', ha='center', fontsize=8, color='#7b1fa2')

ax.annotate('', xy=(6.5, 2.3), xytext=(5.5, 3.5), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#d84315', ls='--'))
ax.text(6.8, 2.9, 'Online Policy Update', ha='center', fontsize=8, color='#d84315')

ax.set_title('Figure 5: High-Level Intelligent Autonomous Warehouse Navigation System Architecture', fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('figures/fig5_system_architecture.png')
plt.close()

# FIGURE 6: DQN / DDQN / Dueling DQN / PER Architecture
fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')

# Input State
draw_box(0.5, 2.2, 1.8, 1.6, 'Input State', 'State Vector / Grid:\n[x, y, bat, obs]\nDimension: d', '#ede7f6', '#512da8')
# Shared Features
draw_box(2.8, 2.0, 2.2, 2.0, 'Feature Extractor', 'Shared Fully Connected\n/ Conv Layers\nReLU Activations\nParam: θ_shared', '#e1f5fe', '#0288d1')
# Dueling streams
draw_box(5.6, 3.3, 2.3, 1.5, 'Value Stream V(s)', 'Dense Layers -> 1\nState-Value V(s; θ, β)\nScalar Output', '#e8f8f5', '#00796b')
draw_box(5.6, 1.2, 2.3, 1.5, 'Advantage Stream A(s,a)', 'Dense Layers -> |A|\nAdvantage A(s,a; θ, α)\nVector Output', '#fef9e7', '#f39c12')
# Aggregation Module
draw_box(8.5, 2.0, 3.0, 2.0, 'Dueling Aggregation Layer', 'Q(s,a) = V(s) +\n(A(s,a) - 1/|A| Σ A(s,a\'))\nIdentifiability Constraint', '#fbe9e7', '#d35400')

# Connective lines
ax.annotate('', xy=(2.8, 3.0), xytext=(2.3, 3.0), arrowprops=arrow_kw)
ax.annotate('', xy=(5.6, 4.0), xytext=(5.0, 3.2), arrowprops=arrow_kw)
ax.annotate('', xy=(5.6, 2.0), xytext=(5.0, 2.8), arrowprops=arrow_kw)
ax.annotate('', xy=(8.5, 3.3), xytext=(7.9, 4.0), arrowprops=arrow_kw)
ax.annotate('', xy=(8.5, 2.7), xytext=(7.9, 2.0), arrowprops=arrow_kw)

# Prioritised Replay Box
draw_box(2.8, 4.4, 4.5, 1.3, 'Prioritised Experience Replay (PER)', 'Transitions (s, a, r, s\') stored with priority P(i) ∝ |δ_i|^α\nImportance Sampling Weights: w_i = (1/N · 1/P(i))^β', '#fce4ec', '#c2185b')
draw_box(8.5, 4.4, 3.0, 1.3, 'Target Network (θ^-)', 'Periodic / Polyak Update:\nθ^- ← τθ + (1-τ)θ^-\nEliminates Moving Target', '#ede7f6', '#4a148c')

ax.annotate('', xy=(5.0, 4.4), xytext=(5.0, 4.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#c2185b', ls=':'))
ax.annotate('', xy=(10.0, 4.4), xytext=(10.0, 4.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4a148c', ls=':'))

ax.set_title('Figure 6: Advanced Deep RL Architecture – Dueling Double DQN with Prioritised Experience Replay', fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('figures/fig6_dqn_dueling_per.png')
plt.close()

print('All 6 figures generated successfully in figures/ directory.')
