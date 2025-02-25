import pygame
from collections import deque
from maze_generator import highlight_cell, get_neighbors_coord, reconstruct_path, DELAY, BLUE, ORANGE, PURPLE, GREEN

def solve_bfs(maze, win):
    """
    Solve the maze using Breadth-First Search (BFS) and animate the search.
    The search starts at (0,0) and continues until the bottom-right cell is reached.
    """
    start = (0, 0)
    end = (maze.rows - 1, maze.cols - 1)
    queue = deque([start])
    came_from = {start: None}
    visited = {start}

    while queue:
        current = queue.popleft()

        # Visualize the current search state
        maze.draw(win)
        for cell in visited:
            highlight_cell(win, cell, BLUE, maze.cell_size)
        for cell in queue:
            highlight_cell(win, cell, ORANGE, maze.cell_size)
        highlight_cell(win, current, PURPLE, maze.cell_size)
        pygame.display.update()
        pygame.time.delay(DELAY)

        if current == end:
            break

        for neighbor in get_neighbors_coord(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    # Reconstruct and animate the final solution path
    path = reconstruct_path(came_from, start, end)
    for cell in path:
        maze.draw(win)
        for path_cell in path:
            highlight_cell(win, path_cell, GREEN, maze.cell_size)
        pygame.display.update()
        pygame.time.delay(DELAY)