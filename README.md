# Quoridor – Graph-Based Game Implementation

## Game Description

**Quoridor** is a strategic two-player board game where both players stand at their side of the board , and the goal is simple to win:  
 **be the first player to reach the opposite side of the board**.

Players take turns choosing **one of two actions**:
1. **Move their piece** to an adjacent valid cell.
2. **Place a wall** to block the opponent's direct path , slowing the opponent down.

Walls can block movement paths but **must never completely block all possible paths** to the goal. This rule is strictly enforced using graph traversal algorithms.

This project is a **fully playable digital version of Quoridor**, implemented in **Python using Pygame library**, featuring:
- Human vs Human mode
- Human vs Computer (AI) mode
- Graph-based board representation
- Operates using Minimax AI with Alpha–Beta pruning
- GUI Implementation

---

## Game Rules

- Board size: **9 × 9**
- Each player starts with **10 walls**
- Player 1 starts at the **bottom**, goal is the **top row**
- Player 2 (or AI) starts at the **top**, goal is the **bottom row**
- Players may:
  - Move one cell (or jump over opponent if possible)
  - Place a horizontal or vertical wall
- A wall placement is **invalid** if it blocks all paths to the goal

---

## Screenshots of Game in Action

### Main Menu
<img width="908" height="745" alt="Screenshot From 2025-12-14 23-31-37" src="https://github.com/user-attachments/assets/ca30aca2-b66a-4515-8525-1ae350659685" />

### Gameplay – Piece Movement ( Player 2 Turn & No More Walls Avaliable )
<img width="908" height="745" alt="Screenshot From 2025-12-14 23-32-35" src="https://github.com/user-attachments/assets/f51f550a-cee6-49fe-a54e-863047bb5315" />

### Wall Placement
<img width="908" height="745" alt="Screenshot From 2025-12-14 23-32-57" src="https://github.com/user-attachments/assets/161af780-d487-441b-afe4-c27b59bb040c" />

### Winning Announcement Page 
<img width="908" height="745" alt="Screenshot From 2025-12-14 23-34-23" src="https://github.com/user-attachments/assets/bf371db9-d403-44ca-8ac3-50db971110cc" />

---

## Installation & Running Instructions

### Prerequisites

- Python **3.8 or higher**
- Pygame library
  
- Install Pygame -> ON bash : pip install pygame
- Clone Github Repo -> ON bash : git clone https://github.com/marwan-osama/quoridor.git  cd quoridor
- ON bash to run the project : python main.py


## Controls 

- TAB : 	Switch between Move play and Wall play
- SPACE	: Rotate wall placement
- Click :	Place the play / Move 
- Mode :  Informs the player which mode is game on right now
- Orient : Tells the orientation ( Horizontal OR Vertical )


## Link to demo Video : 


