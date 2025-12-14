# board.py
import collections
from settings import *

class Board:
    def __init__(self):
        # 1. GRAPH REPRESENTATION
        # Dictionary: key = (c, r), value = list of neighbors [(c, r), ...]
        self.graph = {} 
        self._init_graph()
        
        # 2. VISUAL/LOGICAL STORAGE FOR WALLS
        # Stores placed walls to draw them and check overlap
        # Format: ((c, r), 'H' or 'V')
        self.walls = [] 

    def _init_graph(self):
        """Builds a fully connected 9x9 grid."""
        for c in range(BOARD_SIZE):
            for r in range(BOARD_SIZE):
                neighbors = []
                if r > 0: neighbors.append((c, r-1)) # Up
                if r < BOARD_SIZE-1: neighbors.append((c, r+1)) # Down
                if c > 0: neighbors.append((c-1, r)) # Left
                if c < BOARD_SIZE-1: neighbors.append((c+1, r)) # Right
                self.graph[(c, r)] = neighbors

    def place_wall(self, c, r, orientation, p1, p2):
        """
        Tries to place a wall.
        c, r: Top-left coordinate of the wall reference.
        orientation: 'H' (Horizontal) or 'V' (Vertical).
        p1, p2: Player objects (to check pathfinding).
        Returns: True if successful, False if invalid.
        """
        
        # 1. Boundary Checks
        if c < 0 or c >= BOARD_SIZE - 1 or r < 0 or r >= BOARD_SIZE - 1:
            return False

        # 2. Overlap Checks
        # New wall cannot intersect or overlap existing walls
        new_wall = ((c, r), orientation)
        if new_wall in self.walls: return False
        
        # Check for crossing walls (A vertical wall cannot cut through a horizontal one)
        if orientation == 'H':
            if ((c, r), 'V') in self.walls: return False # Exact cross (invalid in standard rules)
            if ((c+1, r), 'H') in self.walls: return False # Overlap right
            if ((c-1, r), 'H') in self.walls: return False # Overlap left
        else: # Vertical
            if ((c, r), 'H') in self.walls: return False
            if ((c, r+1), 'V') in self.walls: return False
            if ((c, r-1), 'V') in self.walls: return False

        # 3. Temporarily remove edges from graph
        removed_edges = []
        
        if orientation == 'H':
            # Blocks (c, r)<->(c, r+1) AND (c+1, r)<->(c+1, r+1)
            nodes_to_sever = [((c, r), (c, r+1)), ((c+1, r), (c+1, r+1))]
        else: # Vertical
            # Blocks (c, r)<->(c+1, r) AND (c, r+1)<->(c+1, r+1)
            nodes_to_sever = [((c, r), (c+1, r)), ((c, r+1), (c+1, r+1))]

        try:
            for u, v in nodes_to_sever:
                if v in self.graph[u]:
                    self.graph[u].remove(v)
                    self.graph[v].remove(u)
                    removed_edges.append((u, v))
        except ValueError:
            # Should not happen if logic is correct, but safe rollback
            self._restore_edges(removed_edges)
            return False

        # 4. Pathfinding Check (A* or BFS)
        # Does P1 still have a path to row 0? Does P2 still have a path to row 8?
        if self.path_exists(p1.pos, p1.goal_row) and self.path_exists(p2.pos, p2.goal_row):
            self.walls.append(new_wall)
            return True
        else:
            # Path blocked, rollback changes
            self._restore_edges(removed_edges)
            return False

    def _restore_edges(self, edges):
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)

    def path_exists(self, start_pos, target_row):
        """BFS to check if a player can reach their target row."""
        queue = collections.deque([start_pos])
        visited = {start_pos}

        while queue:
            current = queue.popleft()
            if current[1] == target_row:
                return True
            
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False

    def get_valid_moves(self, player, opponent):
        """
        Calculates valid pawn moves, including jump logic.
        Returns a list of (c, r) tuples.
        """
        moves = []
        current = player.pos
        
        # Look at immediate graph neighbors
        for neighbor in self.graph[current]:
            if neighbor == opponent.pos:
                # Opponent is adjacent. Try to jump.
                # Find direction of jump
                dx = neighbor[0] - current[0]
                dy = neighbor[1] - current[1]
                jump_dest = (neighbor[0] + dx, neighbor[1] + dy)
                
                # Check if we can jump STRAIGHT over (is there an edge from Opp to JumpDest?)
                if jump_dest in self.graph[neighbor]:
                    moves.append(jump_dest)
                else:
                    # Straight jump blocked (by wall or board edge).
                    # Add diagonal neighbors of the opponent (if connected to opponent)
                    for diag_neighbor in self.graph[neighbor]:
                        if diag_neighbor != current: # Don't go back
                            moves.append(diag_neighbor)
            else:
                # Normal move to empty square
                moves.append(neighbor)
        
        return moves