# Quoridor – Graph-Based Game Implementation

This project is a fully playable and **scalable** digital version of Quoridor, supporting both classic and custom board sizes.

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

- Board size: **9 × 9** (Classical) or Select a Custom size
- Each player starts with **10 walls** (Classical)
- Player 1 starts at the **bottom**, goal is the **top row**
- Player 2 (or AI) starts at the **top**, goal is the **bottom row**
- Players may:
  - Move one cell (or jump over opponent if possible)
  - Place a horizontal or vertical wall
- A wall placement is **invalid** if it blocks all paths to the goal

---

## Additional Feature : Custom Board Size Feature

This implementation supports **dynamic board sizes**, allowing players to play Quoridor on boards larger or smaller than the standard (9x9).

### Available Custom Board Sizes 
- **5 × 5**
- **7 × 7**
- **9 × 9** (default / classic)
- **11 × 11**

### How It Works
- The board size can be changed **directly from the main menu**
  
- The game automatically:
  - Rebuilds the board graph
  - Repositions players to the center (start position)
  - Adjusts goal rows
  
- All rules (valid paths, wall legality, AI logic) remains the same for any board size

### Why This Feature Actually Matter 
- Smaller boards means faster, more tactical games (suitable for beginners to understand how game works AND for professionals to train on limited number of moves)
- Larger boards means longer, more strategic matches (suitable for long fun games AND for professionals to train on very large amount of moves, thus learning to choose wisely)
- Demonstrates a **fully scalable graph-based design**


## Screenshots of Game in Action

### Main Menu
<img width="1009" height="746" alt="Screenshot From 2025-12-21 17-08-18" src="https://github.com/user-attachments/assets/4a4c35af-736e-4877-901c-ce7f8d260f4d" />

### Gameplay – Piece Movement 9x9 ( Player 2 Turn & No More Walls Avaliable )
<img width="908" height="745" alt="Screenshot From 2025-12-14 23-32-35" src="https://github.com/user-attachments/assets/f51f550a-cee6-49fe-a54e-863047bb5315" />

### Wall Placement
<img width="908" height="745" alt="Screenshot From 2025-12-14 23-32-57" src="https://github.com/user-attachments/assets/161af780-d487-441b-afe4-c27b59bb040c" />

### Gameplay 5x5 Custom Board 
<img width="1009" height="746" alt="Screenshot From 2025-12-21 17-18-43" src="https://github.com/user-attachments/assets/a2e60ec0-a427-4ea9-b8d4-c1acff260baa" />

### Gameplay 11x11 Custom Board 
<img width="1009" height="746" alt="Screenshot From 2025-12-21 17-08-51" src="https://github.com/user-attachments/assets/4abba8c2-830c-4563-bee5-f641c9d5cb62" />

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


## How To Begin A Game

 - To Start a local 2-player game ( Click Human Vs Human Button )
 - To Play against AI ( Click Human Vs AI Button )
 - Click on the Board Size Button to specify the Board Size


## Controls 

- TAB : 	Switch between Move play and Wall play
- SPACE	: Rotate wall placement
- Click :	Place the play / Move 
- Mode :  Informs the player which mode is game on right now
- Orient : Tells the orientation ( Horizontal OR Vertical )


## Link to demo Video : 


