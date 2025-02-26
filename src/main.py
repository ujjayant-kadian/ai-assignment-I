import pygame
import sys
import time
import tracemalloc
import copy
from maze_generator import Maze, highlight_cell
from search_algorithms.dfs import solve_dfs
from search_algorithms.bfs import solve_bfs
from search_algorithms.astar import solve_astar
from utils import log_result, compare_algorithms
from mdp_algorithms.policy_iteration import policy_iteration
from mdp_algorithms.value_iteration import value_iteration

def get_maze_dimensions():
    """
    Prompt the user via the console to input the maze dimensions.
    Defaults to 20x20 if no valid input is provided.
    """
    try:
        rows_input = input("Enter number of rows (default 20): ").strip()
        cols_input = input("Enter number of columns (default 20): ").strip()
        rows = int(rows_input) if rows_input else 20
        cols = int(cols_input) if cols_input else 20
    except ValueError:
        print("Invalid input detected. Using default maze dimensions (20x20).")
        rows, cols = 20, 20
    return rows, cols

def choose_run_mode():
    """
    Allow the user to choose a run mode:
      - Press 1 for DFS, 2 for BFS, 3 for A* Search,
      - 4 to run ALL classical search algorithms,
      - 5 for Policy Iteration (MDP),
      - 6 for Value Iteration (MDP),
      - 7 to run ALL MDP algorithms sequentially,
      - 8 to run ALL algorithms (classical and MDP) sequentially.
    """
    choosing = True
    mode = None
    print("Choose run mode:")
    print("  1: DFS")
    print("  2: BFS")
    print("  3: A* Search")
    print("  4: ALL classical search algorithms")
    print("  5: Policy Iteration (MDP)")
    print("  6: Value Iteration (MDP)")
    print("  7: ALL MDP algorithms")
    print("  8: ALL algorithms (classical + MDP)")
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "DFS"
                    choosing = False
                elif event.key == pygame.K_2:
                    mode = "BFS"
                    choosing = False
                elif event.key == pygame.K_3:
                    mode = "ASTAR"
                    choosing = False
                elif event.key == pygame.K_4:
                    mode = "ALL_CLASSICAL"
                    choosing = False
                elif event.key == pygame.K_5:
                    mode = "POLICY"
                    choosing = False
                elif event.key == pygame.K_6:
                    mode = "VALUE"
                    choosing = False
                elif event.key == pygame.K_7:
                    mode = "ALL_MDP"
                    choosing = False
                elif event.key == pygame.K_8:
                    mode = "ALL_ALL"
                    choosing = False
    return mode

def wait_for_restart():
    """
    After completing the search animations, wait for the user to press a key.
    Press ESC to quit, or any other key to generate a new maze.
    """
    waiting = True
    print("Press any key to generate a new maze, or press ESC to quit.")
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    waiting = False
                    break

def run_algorithm(algorithm, maze, win, rows, cols):
    """
    Run a classical search algorithm (DFS, BFS, or A*) on a deep copy of the maze.
    Measures execution time, memory usage, and returns a tuple:
    (steps_taken, nodes_expanded, max_frontier_size).
    """
    maze_copy = copy.deepcopy(maze)
    start_time = time.time()
    tracemalloc.start()
    
    if algorithm == "DFS":
        metrics = solve_dfs(maze_copy, win)
    elif algorithm == "BFS":
        metrics = solve_bfs(maze_copy, win)
    elif algorithm == "ASTAR":
        metrics = solve_astar(maze_copy, win)
    else:
        metrics = (None, None, None)
    
    execution_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_usage = peak / (1024 * 1024)  # Convert bytes to MB

    steps_taken, nodes_expanded, max_frontier_size = metrics
    log_result(algorithm, (rows, cols), execution_time, steps_taken, memory_usage, nodes_expanded, max_frontier_size)

    print(f"{algorithm}: Execution Time: {execution_time:.4f} s, Steps: {steps_taken}, Memory Usage: {memory_usage:.4f} MB, Nodes Expanded: {nodes_expanded}, Max Frontier Size: {max_frontier_size}")
    return metrics

def run_mdp_algorithm(algorithm, maze, win, rows, cols):
    """
    Run an MDP algorithm (Policy or Value Iteration) on a deep copy of the maze.
    Measures execution time, memory usage, and then extracts and animates the optimal path.
    Returns a tuple: (steps_taken, 0, 0) where nodes expanded and frontier size are not measured.
    """
    maze_copy = copy.deepcopy(maze)
    start_time = time.time()
    tracemalloc.start()
    
    if algorithm == "POLICY":
        steps_taken = policy_iteration(maze_copy, win, gamma=0.9)
    elif algorithm == "VALUE":
        steps_taken = value_iteration(maze_copy, win, gamma=0.9)
    else:
        policy = {}
    
    execution_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_usage = peak / (1024 * 1024)

    # For MDP algorithms, nodes expanded and max frontier size are set to 0.
    log_result(algorithm, (rows, cols), execution_time, steps_taken, memory_usage, 0, 0)
    print(f"{algorithm}: Execution Time: {execution_time:.4f} s, Steps: {steps_taken}, Memory Usage: {memory_usage:.4f} MB")
    return (steps_taken, 0, 0)

def main():
    rows, cols = get_maze_dimensions()
    cell_size = 30  # Size of each cell in pixels
    width = cols * cell_size
    height = rows * cell_size

    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Generator and Search Visualizer")

    while True:
        # Generate one maze instance for all runs.
        maze = Maze(rows, cols, cell_size)
        maze.generate_maze(win)

        mode = choose_run_mode()

        # Clear the window and redraw the maze.
        maze.draw(win)
        pygame.display.update()

        if mode == "ALL_CLASSICAL":
            for alg in ["DFS", "BFS", "ASTAR"]:
                run_algorithm(alg, maze, win, rows, cols)
                pygame.time.delay(1000)
        elif mode == "ALL_MDP":
            for alg in ["POLICY", "VALUE"]:
                run_mdp_algorithm(alg, maze, win, rows, cols)
                pygame.time.delay(1000)
        elif mode == "ALL_ALL":
            # Run classical algorithms first, then MDP algorithms.
            for alg in ["DFS", "BFS", "ASTAR"]:
                run_algorithm(alg, maze, win, rows, cols)
                pygame.time.delay(1000)
            for alg in ["POLICY", "VALUE"]:
                run_mdp_algorithm(alg, maze, win, rows, cols)
                pygame.time.delay(1000)
        elif mode in ["DFS", "BFS", "ASTAR"]:
            run_algorithm(mode, maze, win, rows, cols)
        elif mode in ["POLICY", "VALUE"]:
            run_mdp_algorithm(mode, maze, win, rows, cols)

        print("\nComparison results for maze size {}x{}:".format(rows, cols))
        results = compare_algorithms((rows, cols))
        for result in results:
            print(result)

        wait_for_restart()

if __name__ == "__main__":
    main()
