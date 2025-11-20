
# 🔱 AI Maze Generator and Runner: Kruskal's Algorithm Implementation

## Project Overview

This repository hosts a robust implementation of a **Randomized Kruskal's Algorithm** for generating perfect mazes, coupled with a full-featured **Pygame** interface for real-time visualization, interactive navigation, and performance timing.

Designed as a core component of the CSC 4121 (Artificial Intelligence) coursework, this project serves as a foundational environment for testing pathfinding algorithms such as Breadth-First Search (BFS), Depth-First Search (DFS), and Genetic Algorithms (GA), modules which are integrated within the code structure.

### 🏷️ Technologies & Key Concepts

| Category | Technology | Algorithm/Concept |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Randomized Kruskal's Algorithm |
| **Graphics** | Pygame | Disjoint Set Union (DSU) Structure |
| **Computation** | NumPy | Grid Representation & Matrix Operations |
| **AI Focus** | Pathfinding Visualization | Time Complexity Analysis |

***

## ✨ Features

* **Perfect Maze Generation:** Utilizes Kruskal's algorithm, ensuring a maze with no loops and a guaranteed path between any two points.
* **Interactive Gameplay:** Users can navigate the maze from the blue start point to the red exit point using standard controls.
* **Time Recording:** A precise timer starts on the first movement and stops upon reaching the goal, allowing for performance measurement.
* **Maze Regeneration:** A dedicated button allows for the instant generation of a new, unique maze.
* **Modular Design:** The project is structured with separate modules for `Maze` generation, `Game` logic, and `Player` mechanics, facilitating easy integration of search algorithms.

***

## ⚙️ Setup and Installation

Follow these steps to set up and run the project locally. It is highly recommended to use a virtual environment to manage dependencies.

### 1. Clone the Repository

```bash
git clone [https://github.com/MiltonJ23/MazeSearch.git](https://github.com/MiltonJ23/MazeSearch.git)
cd MazeSearch/Code
````

### 2\. Set Up the Virtual Environment

Create a virtual environment (e.g., named `AIvenv`) and activate it.

```bash
# navigate to the virtual environment 
cd .. 

# Activate the virtual environment
# For macOS/Linux:
source AIvenv/bin/activate
# For Windows (Command Prompt):
# AIvenv\Scripts\activate.bat
# For Windows (PowerShell):
# AIvenv\Scripts\Activate.ps1
```

### 3\. Install Dependencies

This project requires the `numpy` library for matrix manipulation and `pygame` for the graphical interface.

```bash
pip install numpy pygame
```

-----

## 🚀 Usage

Once the environment is active and dependencies are installed, you can launch the maze application by executing the main script within the `Code` directory.

### Launching the Application

Execute the following command from the `Code` directory:

```bash
python3 main.py
```

### Game Controls

The game starts with the player (green square) at the blue entrance. Movement keys initiate the timer.

| Action | Key | Alternate Key |
| :--- | :--- | :--- |
| **Move Up** | **W** | ↑ (Up Arrow) |
| **Move Down** | **S** | ↓ (Down Arrow) |
| **Move Left** | **A** | ← (Left Arrow) |
| **Move Right** | **D** | → (Right Arrow) |

### Win Condition

The game is won when the player reaches the **Red Exit** point. The timer will stop, and the final time will be recorded. Use the **Regenerate Maze** button to start a new challenge.

-----

## 🧩 Architectural Details

The core of the maze generation lies in the `MAZE/maze.py` module.

### Kruskal's Algorithm

The maze is generated using **Randomized Kruskal's Algorithm** leveraging a Disjoint Set Union (DSU) data structure. The DSU structure efficiently tracks connected cells, allowing walls to be broken only if they connect two previously unconnected regions, thereby preventing cycles and ensuring the maze is "perfect."

### Pygame Integration

The `Game/game.py` module manages the Pygame loop, handling:

  * Rendering the 1D maze matrix onto a 2D graphical grid.
  * Processing player input (`Player/player.py`).
  * Managing the game state and timer logic.

<!-- end list -->



