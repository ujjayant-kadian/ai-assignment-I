import os
import csv

# Define the CSV file location and header.
RESULTS_FILE = os.path.join("data", "results.csv")
HEADER = ["Algorithm", "Maze Size", "Execution Time", "Steps Taken", "Memory Usage", "Nodes Expanded", "Max Frontier Size"]

def initialize_results_file(file_path=RESULTS_FILE):
    """
    Ensure the results CSV exists and write the header if the file is new.
    """
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

def log_result(algorithm, maze_size, execution_time, steps_taken, memory_usage, nodes_expanded, max_frontier_size, file_path=RESULTS_FILE):
    """
    Append a new result line to the CSV file.

    Parameters:
      algorithm (str): e.g., "DFS", "BFS", "ASTAR"
      maze_size (tuple or str): Maze dimensions; if tuple, converted to "rowsxcols".
      execution_time (float): Time taken in seconds.
      steps_taken (int): Number of steps in the solution path.
      memory_usage (float): Peak memory usage in MB.
      nodes_expanded (int): Number of nodes expanded during the search.
      max_frontier_size (int): Maximum size of the frontier during the search.
    """
    initialize_results_file(file_path)
    if isinstance(maze_size, tuple):
        maze_size = f"{maze_size[0]}x{maze_size[1]}"
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([algorithm, maze_size, execution_time, steps_taken, memory_usage, nodes_expanded, max_frontier_size])

def compare_algorithms(maze_size, file_path=RESULTS_FILE):
    """
    Retrieve all logged results for a given maze size.

    Parameters:
      maze_size (tuple or str): Maze dimensions (e.g., (20, 20) or "20x20").

    Returns:
      List of dictionaries, one per logged result for the specified maze size.
    """
    initialize_results_file(file_path)
    if isinstance(maze_size, tuple):
        maze_size = f"{maze_size[0]}x{maze_size[1]}"
    results = []
    with open(file_path, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Maze Size"] == maze_size:
                results.append(row)
    return results

if __name__ == "__main__":
    # Example usage: log some dummy results and print the comparison.
    log_result("DFS", "20x20", 0.05, 100, 1.2, 300, 15)
    log_result("BFS", "20x20", 0.07, 120, 1.3, 350, 20)
    log_result("ASTAR", "20x20", 0.03, 90, 1.1, 280, 18)
    for res in compare_algorithms("20x20"):
        print(res)
