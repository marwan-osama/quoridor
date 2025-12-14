# ui.py
import pygame
from settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 18)

    def draw_menu(self):
        self.screen.fill(BACKGROUND)
        
        # Title
        title = self.title_font.render("QUORIDOR", True, WALL_COLOR)
        rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, rect)

        # Buttons
        mx, my = pygame.mouse.get_pos()
        
        # Button 1: PvP
        btn1_rect = pygame.Rect(0, 0, 300, 60)
        btn1_rect.center = (SCREEN_WIDTH//2, 300)
        
        # Button 2: PvAI
        btn2_rect = pygame.Rect(0, 0, 300, 60)
        btn2_rect.center = (SCREEN_WIDTH//2, 400)
        
        # Draw Buttons
        color1 = BUTTON_HOVER if btn1_rect.collidepoint((mx, my)) else BUTTON_COLOR
        color2 = BUTTON_HOVER if btn2_rect.collidepoint((mx, my)) else BUTTON_COLOR
        
        pygame.draw.rect(self.screen, color1, btn1_rect, border_radius=10)
        pygame.draw.rect(self.screen, color2, btn2_rect, border_radius=10)
        
        text1 = self.font.render("Human vs Human", True, WHITE)
        text2 = self.font.render("Human vs Computer", True, WHITE)
        
        self.screen.blit(text1, text1.get_rect(center=btn1_rect.center))
        self.screen.blit(text2, text2.get_rect(center=btn2_rect.center))

        return btn1_rect, btn2_rect

    def draw_game_screen(self, board, p1, p2, turn, input_mode, wall_orient):
        self.screen.fill(BACKGROUND)
        
        # 1. Draw Board Area
        self._draw_grid(board)
        self._draw_players(p1, p2)
        
        # 2. Draw Side Panel / HUD
        self._draw_hud(p1, p2, turn, input_mode, wall_orient)

    def _draw_hud(self, p1, p2, turn, input_mode, wall_orient):
        # Panel Background
        panel_x = BOARD_OFFSET_X + (BOARD_SIZE * (CELL_SIZE + MARGIN)) + 20
        
        # Turn Info
        lbl = self.font.render("Current Turn:", True, TEXT_COLOR)
        self.screen.blit(lbl, (panel_x, 50))
        
        turn_color = p1.color if turn == 1 else p2.color
        turn_name = "Player 1" if turn == 1 else "Player 2"
        if p2.id == "AI" and turn == 2: turn_name = "Computer"
            
        val = self.title_font.render(turn_name, True, turn_color)
        self.screen.blit(val, (panel_x, 80))

        # Wall Counts
        p1_stats = self.font.render(f"P1 Walls: {p1.walls_remaining}", True, p1.color)
        p2_stats = self.font.render(f"P2 Walls: {p2.walls_remaining}", True, p2.color)
        self.screen.blit(p1_stats, (panel_x, 150))
        self.screen.blit(p2_stats, (panel_x, 180))

        # Instructions
        self.screen.blit(self.font.render("Controls:", True, WHITE), (panel_x, 300))
        
        inst_list = [
            "TAB: Switch Move/Wall",
            "SPACE: Rotate Wall",
            "Click: Place / Move",
            f"Mode: {input_mode}",
            f"Orient: {wall_orient}"
        ]
        
        y = 340
        for line in inst_list:
            t = self.small_font.render(line, True, TEXT_COLOR)
            self.screen.blit(t, (panel_x, y))
            y += 30

    def highlight_moves(self, moves):
        for move in moves:
            rect = self._get_cell_rect(move[0], move[1])
            s = pygame.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(128)
            s.fill(VALID_MOVE_COLOR)
            self.screen.blit(s, rect.topleft)
            
    def draw_ghost_wall(self, grid_x, grid_y, orientation):
        # Only draw if valid range
        if 0 <= grid_x < BOARD_SIZE-1 and 0 <= grid_y < BOARD_SIZE-1:
            self._draw_wall_graphic((grid_x, grid_y), orientation, is_ghost=True)

    # --- Helpers ---
    def _draw_grid(self, board):
        for c in range(BOARD_SIZE):
            for r in range(BOARD_SIZE):
                rect = self._get_cell_rect(c, r)
                pygame.draw.rect(self.screen, GRID_COLOR, rect)
        
        # Walls
        for wall in board.walls:
            self._draw_wall_graphic(wall[0], wall[1])

    def _draw_players(self, p1, p2):
        self._draw_pawn(p1)
        self._draw_pawn(p2)

    def _get_cell_rect(self, c, r):
        x = BOARD_OFFSET_X + c * (CELL_SIZE + MARGIN)
        y = BOARD_OFFSET_Y + r * (CELL_SIZE + MARGIN)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def _draw_pawn(self, player):
        rect = self._get_cell_rect(player.pos[0], player.pos[1])
        center = rect.center
        pygame.draw.circle(self.screen, BLACK, center, int(CELL_SIZE * 0.45)) # Outline
        pygame.draw.circle(self.screen, player.color, center, int(CELL_SIZE * 0.4))

    def _draw_wall_graphic(self, pos, orientation, is_ghost=False):
        c, r = pos
        x = BOARD_OFFSET_X + c * (CELL_SIZE + MARGIN) + CELL_SIZE
        y = BOARD_OFFSET_Y + r * (CELL_SIZE + MARGIN) + CELL_SIZE
        
        color = WALL_COLOR if not is_ghost else HOVER_COLOR
        
        if orientation == 'V':
            wall_rect = pygame.Rect(x, y - CELL_SIZE, MARGIN, WALL_LENGTH)
        else:
            wall_rect = pygame.Rect(x - CELL_SIZE, y, WALL_LENGTH, MARGIN)
            
        pygame.draw.rect(self.screen, color, wall_rect)