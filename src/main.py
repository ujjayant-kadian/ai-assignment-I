import pygame
import sys
from maze_generator import Maze
from search_algorithms.dfs import solve_dfs
from search_algorithms.bfs import solve_bfs
from search_algorithms.astar import solve_astar

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

def choose_algorithm():
    """
    Allow the user to choose a search algorithm.
    Press 1 for DFS, 2 for BFS, or 3 for A* Search.
    """
    choosing = True
    algorithm = None
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    algorithm = "DFS"
                    choosing = False
                elif event.key == pygame.K_2:
                    algorithm = "BFS"
                    choosing = False
                elif event.key == pygame.K_3:
                    algorithm = "ASTAR"
                    choosing = False
    return algorithm

def wait_for_restart():
    """
    After completing the search animation, wait for the user to press a key.
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

def main():
    # Get maze dimensions from the user before starting the game.
    rows, cols = get_maze_dimensions()
    cell_size = 30  # Size of each cell in pixels
    width = cols * cell_size
    height = rows * cell_size

    # Initialize Pygame and set up the display window
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Generator and Search Visualizer")

    # Main loop: generate a maze, allow algorithm selection, and animate the search.
    while True:
        # Create and generate a new maze with animation.
        maze = Maze(rows, cols, cell_size)
        maze.generate_maze(win)

        # Choose a search algorithm.
        algorithm = choose_algorithm()

        # Clear the window and redraw the maze before starting the search animation.
        maze.draw(win)
        pygame.display.update()

        # Execute and animate the chosen search algorithm.
        if algorithm == "DFS":
            solve_dfs(maze, win)
        elif algorithm == "BFS":
            solve_bfs(maze, win)
        elif algorithm == "ASTAR":
            solve_astar(maze, win)

        # Wait for user input to restart (or quit) after the search animation.
        wait_for_restart()

if __name__ == "__main__":
    main()
