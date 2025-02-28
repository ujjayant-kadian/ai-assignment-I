import math
import pygame
from maze_generator import highlight_cell, DELAY, GREEN
from utils import get_possible_actions, extract_policy_path

def value_iteration(maze, win, gamma=0.9, theta=1e-4):
    """
    Solve the maze using Value Iteration.
    
    Parameters:
      maze   : Maze object (with attributes rows, cols, and grid where each cell has .walls)
      gamma  : Discount factor.
      theta  : Convergence threshold.
      win    : Pygame window
    
    Returns:
      A tuple (steps_taken, iter_count, 0) where:
        - steps_taken: number of cells in the final optimal path.
        - iter_count: number of full state sweeps (iterations) until convergence.
        - The third metric is 0 (not used for value iteration).
    
    Reward for each move is -1; terminal state is (maze.rows-1, maze.cols-1).
    """
    # Initialize V(s)=0 for all states.
    V = {}
    states = []
    for r in range(maze.rows):
        for c in range(maze.cols):
            state = (r, c)
            V[state] = 0.0
            states.append(state)
    terminal = (maze.rows - 1, maze.cols - 1)
    
    iter_count = 0
    while True:
        iter_count += 1
        delta = 0
        for state in states:
            if state == terminal:
                continue
            actions = get_possible_actions(maze, state)
            if not actions:
                continue
            v = V[state]
            Q_values = []
            for (a, next_state) in actions:
                Q_values.append(-1 + gamma * V[next_state])
            V[state] = max(Q_values)
            delta = max(delta, abs(v - V[state]))
        if delta < theta:
            break
    
    # Derive optimal policy.
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

    # Animate the optimal path if a window is provided.
    path = extract_policy_path(policy, maze)
    if win is not None:
        for state in path:
            maze.draw(win)
            highlight_cell(win, state, GREEN, maze.cell_size)
            pygame.display.update()
            pygame.time.delay(DELAY)
    return len(path), iter_count, 0
