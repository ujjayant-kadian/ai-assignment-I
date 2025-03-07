import pygame
from maze_generator import highlight_cell, get_neighbors_coord, reconstruct_path, DELAY, BLUE, ORANGE, PURPLE, GREEN

def solve_dfs(maze, win):
    """
    Solve the maze using Depth-First Search (DFS) and animate the search.
    
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
    stack = [start]
    came_from = {start: None}
    visited = set()
    
    nodes_expanded = 0
    max_frontier_size = len(stack)

    while stack:
        current = stack.pop()
        nodes_expanded += 1
        max_frontier_size = max(max_frontier_size, len(stack))
        visited.add(current)

        # Visualize the current state of the search
        maze.draw(win)
        for cell in visited:
            highlight_cell(win, cell, BLUE, maze.cell_size)
        for cell in stack:
            highlight_cell(win, cell, ORANGE, maze.cell_size)
        highlight_cell(win, current, PURPLE, maze.cell_size)
        pygame.display.update()
        pygame.time.delay(DELAY)

        if current == end:
            break

        for neighbor in get_neighbors_coord(current, maze):
            if neighbor not in visited and neighbor not in stack:
                came_from[neighbor] = current
                stack.append(neighbor)
                max_frontier_size = max(max_frontier_size, len(stack))

    # Reconstruct and animate the final solution path
    path = reconstruct_path(came_from, start, end)
    for cell in path:
        maze.draw(win)
        for path_cell in path:
            highlight_cell(win, path_cell, GREEN, maze.cell_size)
        pygame.display.update()
        pygame.time.delay(DELAY)
    
    return (len(path), nodes_expanded, max_frontier_size)
