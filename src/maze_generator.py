import pygame
import random
from queue import PriorityQueue
from collections import deque

# ----------------------------- #
#       Color Definitions       #
# ----------------------------- #
WHITE   = (255, 255, 255)  # Maze walls
BLACK   = (0, 0, 0)        # Background
BLUE    = (0, 0, 255)      # Visited cells during search
ORANGE  = (255, 165, 0)    # Frontier cells (cells to be explored)
GREEN   = (0, 255, 0)      # Final solution path
PURPLE  = (128, 0, 128)    # Currently processing cell

DELAY   = 30             # Delay in milliseconds for animation speed

# ----------------------------- #
#       Maze Cell Class         #
# ----------------------------- #
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        # Each cell has four walls in order: [top, right, bottom, left]
        self.walls = [True, True, True, True]
        self.visited = False   # Used during maze generation

    def draw(self, win, cell_size):
        """Draw the cell walls on the window."""
        x = self.col * cell_size
        y = self.row * cell_size
        
        # Draw the top wall
        if self.walls[0]:
            pygame.draw.line(win, WHITE, (x, y), (x + cell_size, y), 2)
        # Draw the right wall
        if self.walls[1]:
            pygame.draw.line(win, WHITE, (x + cell_size, y), (x + cell_size, y + cell_size), 2)
        # Draw the bottom wall
        if self.walls[2]:
            pygame.draw.line(win, WHITE, (x + cell_size, y + cell_size), (x, y + cell_size), 2)
        # Draw the left wall
        if self.walls[3]:
            pygame.draw.line(win, WHITE, (x, y + cell_size), (x, y), 2)

# ----------------------------- #
#          Maze Class           #
# ----------------------------- #
class Maze:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        # Create a 2D grid of cells
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.stack = []  # Stack used for the recursive backtracking algorithm

    def index(self, row, col):
        """Return the cell at (row, col) if within bounds; otherwise return None."""
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return None
        return self.grid[row][col]

    def get_unvisited_neighbors(self, cell):
        """Return a list of unvisited neighbor cells (top, right, bottom, left)."""
        neighbors = []
        row, col = cell.row, cell.col
        
        # Check the four directions
        top    = self.index(row - 1, col)
        right  = self.index(row, col + 1)
        bottom = self.index(row + 1, col)
        left   = self.index(row, col - 1)
        
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return neighbors

    def remove_walls(self, current, next_cell):
        """Remove the walls between the current cell and the next cell."""
        dx = current.col - next_cell.col
        dy = current.row - next_cell.row
        if dx == 1:  # next_cell is to the left of current
            current.walls[3] = False
            next_cell.walls[1] = False
        elif dx == -1:  # next_cell is to the right of current
            current.walls[1] = False
            next_cell.walls[3] = False
        if dy == 1:  # next_cell is above current
            current.walls[0] = False
            next_cell.walls[2] = False
        elif dy == -1:  # next_cell is below current
            current.walls[2] = False
            next_cell.walls[0] = False

    def generate_maze(self, win):
        """Generate the maze using recursive backtracking."""
        current = self.grid[0][0]
        current.visited = True
        self.stack.append(current)
        
        while self.stack:
            current = self.stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            
            if neighbors:
                # Choose a random unvisited neighbor
                next_cell = random.choice(neighbors)
                next_cell.visited = True
                # Remove the wall between current and next_cell
                self.remove_walls(current, next_cell)
                self.stack.append(next_cell)
            else:
                self.stack.pop()

            # Optional: Animate the maze generation process
            self.draw(win)
            highlight_cell(win, (current.row, current.col), PURPLE, self.cell_size)
            pygame.display.update()
            pygame.time.delay(DELAY)
        
        # Reset visited flags so they can be used in the search visualizations
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def draw(self, win):
        """Draw the complete maze (all cells and their walls)."""
        win.fill(BLACK)
        for row in self.grid:
            for cell in row:
                cell.draw(win, self.cell_size)

# ----------------------------- #
#       Helper Functions        #
# ----------------------------- #
def highlight_cell(win, cell_coord, color, cell_size):
    """
    Highlight a cell at the given coordinate with a colored rectangle.
    A small margin is added so the underlying walls are still visible.
    """
    row, col = cell_coord
    x = col * cell_size
    y = row * cell_size
    pygame.draw.rect(win, color, (x + 4, y + 4, cell_size - 8, cell_size - 8))

def get_neighbors_coord(cell_coord, maze):
    """
    Given a cell coordinate (row, col), return a list of neighboring cell coordinates
    that are accessible (i.e. where the wall between them has been removed).
    """
    row, col = cell_coord
    neighbors = []
    cell = maze.grid[row][col]
    
    # Check top neighbor
    if not cell.walls[0] and row > 0:
        neighbors.append((row - 1, col))
    # Check right neighbor
    if not cell.walls[1] and col < maze.cols - 1:
        neighbors.append((row, col + 1))
    # Check bottom neighbor
    if not cell.walls[2] and row < maze.rows - 1:
        neighbors.append((row + 1, col))
    # Check left neighbor
    if not cell.walls[3] and col > 0:
        neighbors.append((row, col - 1))
    return neighbors

def reconstruct_path(came_from, start, end):
    """
    Reconstruct the path from start to end using the dictionary that maps each cell
    to the cell it came from.
    """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path