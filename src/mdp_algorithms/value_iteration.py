import math
import pygame
from maze_generator import GREEN, DELAY, highlight_cell

def get_possible_actions(maze, state):
    """
    Given a maze and a state (r, c), return a list of tuples (action, next_state)
    for all available actions from that state.
    
    The maze Cell's walls are assumed to be in order [top, right, bottom, left].
    An action "U" is available if there is no top wall, "R" if no right wall, etc.
    """
    r, c = state
    actions = []
    cell = maze.grid[r][c]
    # Up
    if not cell.walls[0] and r > 0:
        actions.append(("U", (r - 1, c)))
    # Right
    if not cell.walls[1] and c < maze.cols - 1:
        actions.append(("R", (r, c + 1)))
    # Down
    if not cell.walls[2] and r < maze.rows - 1:
        actions.append(("D", (r + 1, c)))
    # Left
    if not cell.walls[3] and c > 0:
        actions.append(("L", (r, c - 1)))
    return actions

def extract_policy_path(policy, maze):
    """
    Given a policy dict and a maze, extract the path from start to terminal.
    Start state is (0, 0) and terminal state is (maze.rows-1, maze.cols-1).
    Returns a list of states representing the optimal path.
    """
    path = []
    state = (0, 0)
    terminal = (maze.rows - 1, maze.cols - 1)
    while state != terminal:
        path.append(state)
        action = policy.get(state)
        if action is None:
            break
        r, c = state
        if action == "U":
            state = (r - 1, c)
        elif action == "R":
            state = (r, c + 1)
        elif action == "D":
            state = (r + 1, c)
        elif action == "L":
            state = (r, c - 1)
        else:
            break
    path.append(terminal)
    return path

def value_iteration(maze, win, gamma=0.9, theta=1e-4):
    """
    Solve the maze using Value Iteration.
    
    Parameters:
      maze   : Maze object (with attributes rows, cols, and grid where each cell has .walls)
      gamma  : Discount factor.
      theta  : Convergence threshold.
    
    Returns:
      A tuple (V, policy) where:
        - V is a dict mapping state (r, c) to its computed value.
        - policy is a dict mapping state (r, c) to the optimal action ("U", "R", "D", or "L").
    
    The reward for every move is -1, and the terminal state is the bottom-right cell.
    """
    # Initialize state-value function V(s)=0 for all states.
    V = {}
    states = []
    for r in range(maze.rows):
        for c in range(maze.cols):
            state = (r, c)
            V[state] = 0.0
            states.append(state)
    terminal = (maze.rows - 1, maze.cols - 1)
    
    while True:
        delta = 0
        for state in states:
            # Terminal state has zero value.
            if state == terminal:
                continue
            actions = get_possible_actions(maze, state)
            if not actions:
                continue
            v = V[state]
            # For each available action, Q(s,a) = reward + gamma * V(s')
            # Here reward = -1 for every move.
            Q_values = []
            for (a, next_state) in actions:
                Q_values.append(-1 + gamma * V[next_state])
            V[state] = max(Q_values)
            delta = max(delta, abs(v - V[state]))
        if delta < theta:
            break
    
    # Derive policy: for each state, choose the action achieving the maximum Q-value.
    policy = {}
    for state in states:
        if state == terminal:
            policy[state] = None
            continue
        actions = get_possible_actions(maze, state)
        if not actions:
            policy[state] = None
            continue
        best_action = None
        best_value = -math.inf
        for (a, next_state) in actions:
            q = -1 + gamma * V[next_state]
            if q > best_value:
                best_value = q
                best_action = a
        policy[state] = best_action
    
    path = extract_policy_path(policy, maze)
    for state in path:
        maze.draw(win)
        highlight_cell(win, state, GREEN, maze.cell_size)
        pygame.display.update()
        pygame.time.delay(DELAY)

    return len(path)