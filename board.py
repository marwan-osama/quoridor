import collections
import copy
from settings import *

class Board:
    def __init__(self, size=9, graph=None, walls=None):
        self.size = size

        if graph:
            self.graph = graph
        else:
            self.graph = {}
            self._init_graph()

        self.walls = walls if walls is not None else []

    def _init_graph(self):
        for c in range(self.size):
            for r in range(self.size):
                neighbors = []
                if r > 0: neighbors.append((c, r-1))
                if r < self.size-1: neighbors.append((c, r+1))
                if c > 0: neighbors.append((c-1, r))
                if c < self.size-1: neighbors.append((c+1, r))
                self.graph[(c, r)] = neighbors

    def clone(self):
        """Creates a deep copy of the board for AI simulation."""
        # We must deepcopy the graph because lists (neighbors) are mutable
        return Board(self.size, copy.deepcopy(self.graph), copy.deepcopy(self.walls))

    def place_wall(self, c, r, orientation, p1, p2):
        if c < 0 or c >= self.size - 1 or r < 0 or r >= self.size - 1:
            return False

        new_wall = ((c, r), orientation)
        if new_wall in self.walls: return False

        # Check overlaps
        if orientation == 'H':
            if ((c, r), 'V') in self.walls: return False
            if ((c+1, r), 'H') in self.walls: return False
            if ((c-1, r), 'H') in self.walls: return False
        else: 
            if ((c, r), 'H') in self.walls: return False
            if ((c, r+1), 'V') in self.walls: return False
            if ((c, r-1), 'V') in self.walls: return False

        # Temporarily remove edges
        removed_edges = []
        if orientation == 'H':
            nodes_to_sever = [((c, r), (c, r+1)), ((c+1, r), (c+1, r+1))]
        else:
            nodes_to_sever = [((c, r), (c+1, r)), ((c, r+1), (c+1, r+1))]

        try:
            for u, v in nodes_to_sever:
                if v in self.graph[u]:
                    self.graph[u].remove(v)
                    self.graph[v].remove(u)
                    removed_edges.append((u, v))
        except ValueError:
            self._restore_edges(removed_edges)
            return False

        # Check path validity
        if self.path_exists(p1.pos, p1.goal_row) and self.path_exists(p2.pos, p2.goal_row):
            self.walls.append(new_wall)
            return True
        else:
            self._restore_edges(removed_edges)
            return False

    def _restore_edges(self, edges):
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)

    def path_exists(self, start_pos, target_row):
        return self.get_shortest_path_len(start_pos, target_row) != -1

    def get_shortest_path_len(self, start_pos, target_row):
        """BFS to find shortest path length. Used by AI Heuristic."""
        queue = collections.deque([(start_pos, 0)])
        visited = {start_pos}

        while queue:
            current, dist = queue.popleft()
            if current[1] == target_row:
                return dist

            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        return -1

    def get_valid_moves(self, player, opponent):
        moves = []
        current = player.pos
        if current not in self.graph: return [] # Safety check

        for neighbor in self.graph[current]:
            if neighbor == opponent.pos:
                # Jump Logic
                dx = neighbor[0] - current[0]
                dy = neighbor[1] - current[1]
                jump_dest = (neighbor[0] + dx, neighbor[1] + dy)

                if jump_dest in self.graph[neighbor]:
                    moves.append(jump_dest)
                else:
                    for diag_neighbor in self.graph[neighbor]:
                        if diag_neighbor != current:
                            moves.append(diag_neighbor)
            else:
                moves.append(neighbor)
        return moves
