# player.py
from settings import *

class Player:
    def __init__(self, start_pos, color, goal_row, player_id):
        self.pos = start_pos  # Tuple (col, row)
        self.color = color
        self.walls_remaining = 10
        self.goal_row = goal_row
        self.id = player_id

    def move(self, new_pos):
        self.pos = new_pos

    def has_walls(self):
        return self.walls_remaining > 0

    def use_wall(self):
        if self.walls_remaining > 0:
            self.walls_remaining -= 1