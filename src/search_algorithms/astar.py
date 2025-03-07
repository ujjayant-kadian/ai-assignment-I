import pygame
from queue import PriorityQueue
from maze_generator import BLUE, ORANGE, PURPLE, GREEN, DELAY, highlight_cell, get_neighbors_coord, reconstruct_path

def heuristic(a, b):
    """Manhattan distance heuristic for A* search."""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def solve_astar(maze, win):
    """
    Solve the maze using the A* search algorithm and animate the process.
    Uses the Manhattan distance as the heuristic.
    
    Parameters:
        maze : Maze object.
        win  : Pygame window

    Returns a tuple: (steps_taken, nodes_expanded, max_frontier_size), where:
        - steps_taken: number of cells in the final optimal path.
        - nodes_expanded: number of nodes expanded during the search.
        - max_frontier_size: maximum number of nodes in the frontier at any point during the search.
    """
    start = (0, 0)
    end = (maze.rows - 1, maze.cols - 1)
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    
    # Initialize g_score and f_score dictionaries
    g_score = { (r, c): float('inf') for r in range(maze.rows) for c in range(maze.cols) }
    g_score[start] = 0
    f_score = { (r, c): float('inf') for r in range(maze.rows) for c in range(maze.cols) }
    f_score[start] = heuristic(start, end)
    
    open_set_hash = {start}
    visited = set()

    nodes_expanded = 0
    max_frontier_size = len(open_set_hash)

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)
        nodes_expanded += 1
        max_frontier_size = max(max_frontier_size, len(open_set_hash))
        visited.add(current)

        # Visualize the A* search state
        maze.draw(win)
        for cell in visited:
            highlight_cell(win, cell, BLUE, maze.cell_size)
        for cell in open_set_hash:
            highlight_cell(win, cell, ORANGE, maze.cell_size)
        highlight_cell(win, current, PURPLE, maze.cell_size)
        pygame.display.update()
        pygame.time.delay(DELAY)

        if current == end:
            break

        for neighbor in get_neighbors_coord(current, maze):
            tentative_g = g_score[current] + 1  # Cost of 1 for each move
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    max_frontier_size = max(max_frontier_size, len(open_set_hash))

    # Reconstruct and animate the final solution path
    path = reconstruct_path(came_from, start, end)
    for cell in path:
        maze.draw(win)
        for path_cell in path:
            highlight_cell(win, path_cell, GREEN, maze.cell_size)
        pygame.display.update()
        pygame.time.delay(DELAY)
    
    return (len(path), nodes_expanded, max_frontier_size)
