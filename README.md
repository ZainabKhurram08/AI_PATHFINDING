# Dynamic Pathfinding Agent

An interactive pathfinding visualizer built with Python and Pygame.  
Visualizes **A* Search** and **Greedy Best-First Search (GBFS)** on a configurable grid with real-time animation and dynamic obstacle support.

---

## Requirements

- Python 3.8+
- pygame

---

## Installation
```bash
pip install pygame
```

---

## How to Run
```bash
python pathfinding.py
```

---

## How to Use

### Grid Config
- Set **Rows**, **Cols**, and **Dens%** using the input boxes on the left panel
- Click **Apply** to apply changes
- Click **Gen Maze** to randomly generate walls

### Algorithm
- **A*** — optimal, finds shortest path
- **GBFS** — faster but not always optimal

### Heuristic
- **Manhattan** — horizontal + vertical distance
- **Euclidean** — straight-line distance

### Edit Mode
Click a mode then click/drag on the grid:
- **Wall** — draw obstacles
- **Erase** — remove obstacles
- **Start** — move the start point
- **Goal** — move the goal point

<<<<<<< Updated upstream
### Actions
- **START** — run the algorithm and animate
- **Reset** — clear the grid

### Dynamic Mode
Toggle **Dynamic** to spawn random walls while the agent moves.  
If the path is blocked, the agent re-plans automatically.

---

## Stats (Top Bar)

| Metric | Description |
|---|---|
| Nodes Visited | Total nodes explored |
| Path Cost | Steps from start to goal |
| Exec Time | Algorithm runtime (ms) |

---

## Color Guide

| Color | Meaning |
|---|---|
| Yellow | Frontier (open set) |
| Cyan | Visited (closed set) |
| Green | Final path |
| Purple | Start cell |
| Red | Goal cell |
| Grey | Wall |
| Pink | Dynamically added wall |
| Orange circle | Agent |
=======
Actions
•	START: run the algorithm and animate
•	Reset: clear the grid
Dynamic Mode
Toggle Dynamic to spawn random walls while the agent moves. If the path is blocked, the agent re-plans automatically.
Stats (Top Bar)
Metric	Description
Nodes Visited:	Total nodes explored
Path Cost:	Steps from start to goal
Exec Time:	Algorithm runtime (ms)

Color Guide
Color	Meaning
Yellow:	Frontier (open set)
Cyan:	Visited (closed set)
Green:	Final path
Purple:	Start cell
Red:	Goal cell
Grey:	Wall
Pink:	Dynamically added wall
Orange circle:	Agent
>>>>>>> Stashed changes
