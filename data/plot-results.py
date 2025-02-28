import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

file_path = "results.csv"
df = pd.read_csv(file_path)

df["Maze Size"] = df["Maze Size"].astype(str)

plots_dir = "plots/"
os.makedirs(plots_dir, exist_ok=True)

df = df.rename(columns={
    'Nodes Expanded\Iteration Count\Policy Improvement Count': 'Iteration Count',
    'Max Frontier Size\Total Evaluation Iteration': 'Max Frontier Size'
})

classical_algorithms = ["DFS", "BFS", "ASTAR"]
mdp_algorithms = ["POLICY", "VALUE"]

def plot_and_save(x, y, ylabel, title, filename, algorithms):
    plt.figure(figsize=(10, 5))
    x_values = df[x].unique()
    x_indices = np.arange(len(x_values))
    width = 0.2  # Bar width for spacing
    
    for i, algorithm in enumerate(algorithms):
        subset = df[df["Algorithm"] == algorithm]
        y_values = [subset[subset[x] == val][y].values[0] if val in subset[x].values else 0 for val in x_values]
        plt.bar(x_indices + (i * width), y_values, width=width, label=algorithm, alpha=0.7)
    
    plt.xticks(x_indices + width, x_values)
    plt.xlabel("Maze Size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(axis='y')
    plt.savefig(os.path.join(plots_dir, filename))
    plt.close()

plot_and_save("Maze Size", "Execution Time", "Execution Time (seconds)", "Execution Time Comparison Across All Algorithms", "execution_time_comparison.png", df["Algorithm"].unique())
plot_and_save("Maze Size", "Memory Usage", "Memory Usage (MB)", "Memory Usage Comparison Across All Algorithms", "memory_usage_comparison.png", df["Algorithm"].unique())
plot_and_save("Maze Size", "Iteration Count", "Nodes Expanded", "Nodes Expanded Comparison Among Classical Algorithms", "nodes_expanded_comparison.png", classical_algorithms)
plot_and_save("Maze Size", "Max Frontier Size", "Max Frontier Size", "Max Frontier Size Comparison Among Classical Algorithms", "max_frontier_size_comparison.png", classical_algorithms)
plot_and_save("Maze Size", "Iteration Count", "Iteration Count / Policy Improvement Count", "Iteration Count Comparison Among MDP Algorithms", "mdp_iteration_count_comparison.png", mdp_algorithms)

print(f"Plots have been saved in: {plots_dir}")
