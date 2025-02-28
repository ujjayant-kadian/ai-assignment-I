# Maze Solver & Search Algorithm Visualizer

## Overview
This project is a **Maze Solver & Search Algorithm Visualizer** built using **Pygame**. It generates a random maze and allows users to solve it using various **classical search algorithms** (DFS, BFS, A*) and **MDP-based algorithms** (Policy Iteration, Value Iteration).

---

## Installation & Setup
### 1️. Install Dependencies
Ensure **Python 3.x** is installed, then install required libraries:
```bash
pip install pygame
```

### 2. Run the Program
```bash
python src/main.py
```

---

## How to Use
### **1️. Choose Maze Size**
The program will prompt:
```
Enter number of rows (default 20):
Enter number of columns (default 20):
```
Press **Enter** for default **20x20**.

### **2️. Choose Algorithm Mode**
Use the keyboard to select an algorithm:
```
  1: DFS
  2: BFS
  3: A* Search
  4: ALL classical search algorithms
  5: Policy Iteration (MDP)
  6: Value Iteration (MDP)
  7: ALL MDP algorithms
  8: ALL algorithms (classical + MDP)
```
- Press the **corresponding number key** to start.

### **3️. Observe Algorithm Execution**
The search process will be **visualized**:
- **🟦 Blue**: Visited nodes
- **🟧 Orange**: Frontier (Nodes in Queue/Stack)
- **🟪 Purple**: Currently Processing Node
- **🟩 Green**: Final Solution Path

### **4️. View Results & Compare**
Results are displayed in the console:
```
A*: Execution Time: 0.0321 s, Steps: 45, Memory Usage: 1.23 MB, Nodes Expanded: 90, Max Frontier Size: 15
```

All results are logged in `data/results.csv` for **comparison**.

### **5️. Restart or Exit**
At the end, press:
- **Any key** → Generate a new maze.
- **ESC** → Quit.

---



