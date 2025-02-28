import math
import pygame
from maze_generator import highlight_cell, DELAY, GREEN
from utils import get_possible_actions, extract_policy_path

def policy_iteration(maze, win, gamma=0.9, theta=1e-4):
    """
    Solve the maze using Policy Iteration.
    
    Parameters:
      maze   : Maze object.
      gamma  : Discount factor.
      theta  : Convergence threshold for policy evaluation.
      win    : Pygame window
      
    Returns:
      A tuple (steps_taken, policy_improvement_count, total_evaluation_iterations) where:
        - steps_taken: number of cells in the final optimal path.
        - policy_improvement_count: number of times the policy was improved.
        - total_evaluation_iterations: total sweeps performed during all policy evaluations.
    
    Reward for each move is -1; terminal state is (maze.rows-1, maze.cols-1).
    """
    states = []
    for r in range(maze.rows):
        for c in range(maze.cols):
            states.append((r, c))
    # Initialize arbitrary policy and value function.
    policy = {}
    V = {}
    for state in states:
        V[state] = 0.0
        if state == (maze.rows - 1, maze.cols - 1):
            policy[state] = None
        else:
            actions = get_possible_actions(maze, state)
            policy[state] = actions[0][0] if actions else None
    terminal = (maze.rows - 1, maze.cols - 1)
    
    total_evaluation_iterations = 0
    policy_improvement_count = 0

    def policy_evaluation(policy, V):
        eval_iterations = 0
        while True:
            eval_iterations += 1
            delta = 0
            for state in states:
                if state == terminal:
                    continue
                a = policy[state]
                actions = get_possible_actions(maze, state)
                next_state = None
                for (act, ns) in actions:
                    if act == a:
                        next_state = ns
                        break
                if next_state is None:
                    continue
                v = V[state]
                V[state] = -1 + gamma * V[next_state]
                delta = max(delta, abs(v - V[state]))
            if delta < theta:
                break
        return eval_iterations

    stable = False
    while not stable:
        eval_iters = policy_evaluation(policy, V)
        total_evaluation_iterations += eval_iters
        policy_improvement_count += 1
        stable = True
        for state in states:
            if state == terminal:
                continue
            actions = get_possible_actions(maze, state)
            if not actions:
                continue
            old_action = policy[state]
            best_action = None
            best_value = -math.inf
            for (a, next_state) in actions:
                q = -1 + gamma * V[next_state]
                if q > best_value:
                    best_value = q
                    best_action = a
            if best_action != old_action:
                policy[state] = best_action
                stable = False

    # Animate the optimal path.
    path = extract_policy_path(policy, maze)
    if win is not None:
        for state in path:
            maze.draw(win)
            highlight_cell(win, state, GREEN, maze.cell_size)
            pygame.display.update()
            pygame.time.delay(DELAY)
    return len(path), policy_improvement_count, total_evaluation_iterations
