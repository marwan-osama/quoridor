# ui.py
import pygame
from settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)

    def draw_board(self, board):
        # Draw background grid cells
        for c in range(BOARD_SIZE):
            for r in range(BOARD_SIZE):
                rect = self._get_cell_rect(c, r)
                pygame.draw.rect(self.screen, GRID_COLOR, rect)

        # Draw Walls stored in the board
        for wall in board.walls:
            self._draw_wall_graphic(wall[0], wall[1])

    def draw_players(self, p1, p2):
        self._draw_pawn(p1)
        self._draw_pawn(p2)

    def highlight_moves(self, moves):
        for move in moves:
            rect = self._get_cell_rect(move[0], move[1])
            s = pygame.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(128)
            s.fill(VALID_MOVE_COLOR)
            self.screen.blit(s, rect.topleft)

    def draw_stats(self, p1, p2, current_turn):
        # Draw text at bottom
        text_y = SCREEN_HEIGHT - 80
        
        p1_text = f"P1 Walls: {p1.walls_remaining}"
        p2_text = f"P2 Walls: {p2.walls_remaining}"
        turn_text = f"Turn: Player {current_turn}"

        surf1 = self.font.render(p1_text, True, PLAYER_1_COLOR)
        surf2 = self.font.render(p2_text, True, PLAYER_2_COLOR)
        surf3 = self.font.render(turn_text, True, WHITE)

        self.screen.blit(surf1, (20, text_y))
        self.screen.blit(surf2, (SCREEN_WIDTH - 150, text_y))
        self.screen.blit(surf3, (SCREEN_WIDTH // 2 - 50, text_y))

    # --- Helpers ---
    def _get_cell_rect(self, c, r):
        x = BOARD_OFFSET_X + c * (CELL_SIZE + MARGIN)
        y = BOARD_OFFSET_Y + r * (CELL_SIZE + MARGIN)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def _draw_pawn(self, player):
        rect = self._get_cell_rect(player.pos[0], player.pos[1])
        center = rect.center
        pygame.draw.circle(self.screen, player.color, center, int(CELL_SIZE * 0.4))

    def _draw_wall_graphic(self, pos, orientation):
        c, r = pos
        # Calculate pixel position of the gap between cells
        x = BOARD_OFFSET_X + c * (CELL_SIZE + MARGIN) + CELL_SIZE
        y = BOARD_OFFSET_Y + r * (CELL_SIZE + MARGIN) + CELL_SIZE
        
        if orientation == 'V':
            # Vertical wall starts in the gap between Col C and C+1
            # Starts at Row R top, goes down 2 cells + 1 margin
            wall_rect = pygame.Rect(x, y - CELL_SIZE, MARGIN, WALL_LENGTH)
        else:
            # Horizontal wall starts in gap between Row R and R+1
            wall_rect = pygame.Rect(x - CELL_SIZE, y, WALL_LENGTH, MARGIN)
            
        pygame.draw.rect(self.screen, WALL_COLOR, wall_rect)