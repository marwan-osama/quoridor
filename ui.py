import pygame
from settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 18)

    def draw_menu(self, current_size):
        """Draws menu with Size Toggle."""
        self.screen.fill(BACKGROUND)

        # Title
        title = self.title_font.render("QUORIDOR", True, WALL_COLOR)
        rect = title.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(title, rect)

        # Buttons
        mx, my = pygame.mouse.get_pos()

        # Button 1: PvP
        btn1_rect = pygame.Rect(0, 0, 300, 50)
        btn1_rect.center = (SCREEN_WIDTH//2, 250)

        # Button 2: PvAI
        btn2_rect = pygame.Rect(0, 0, 300, 50)
        btn2_rect.center = (SCREEN_WIDTH//2, 320)

        # Button 3: Size Toggle
        btn3_rect = pygame.Rect(0, 0, 200, 40)
        btn3_rect.center = (SCREEN_WIDTH//2, 420)

        # Draw Buttons
        color1 = BUTTON_HOVER if btn1_rect.collidepoint((mx, my)) else BUTTON_COLOR
        color2 = BUTTON_HOVER if btn2_rect.collidepoint((mx, my)) else BUTTON_COLOR
        color3 = BUTTON_HOVER if btn3_rect.collidepoint((mx, my)) else BUTTON_COLOR

        pygame.draw.rect(self.screen, color1, btn1_rect, border_radius=10)
        pygame.draw.rect(self.screen, color2, btn2_rect, border_radius=10)
        pygame.draw.rect(self.screen, color3, btn3_rect, border_radius=10)

        text1 = self.font.render("Human vs Human", True, WHITE)
        text2 = self.font.render("Human vs Computer", True, WHITE)
        text3 = self.font.render(f"Board Size: {current_size}x{current_size}", True, WHITE)

        self.screen.blit(text1, text1.get_rect(center=btn1_rect.center))
        self.screen.blit(text2, text2.get_rect(center=btn2_rect.center))
        self.screen.blit(text3, text3.get_rect(center=btn3_rect.center))

        return btn1_rect, btn2_rect, btn3_rect

    def draw_game_screen(self, board, p1, p2, turn, input_mode, wall_orient):
        self.screen.fill(BACKGROUND)

        # 1. Draw Board Area
        self._draw_grid(board)
        self._draw_players(board, p1, p2)

        # 2. Draw Side Panel / HUD
        self._draw_hud(board, p1, p2, turn, input_mode, wall_orient)

    def _draw_hud(self, board, p1, p2, turn, input_mode, wall_orient):
        # Calculate dynamic panel X position based on board width
        ox, oy = self._get_offsets(board.size)
        board_width = board.size * (CELL_SIZE + MARGIN)
        panel_x = ox + board_width + 40

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

    def highlight_moves(self, board, moves):
        for move in moves:
            rect = self._get_cell_rect(board.size, move[0], move[1])
            s = pygame.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(128)
            s.fill(VALID_MOVE_COLOR)
            self.screen.blit(s, rect.topleft)

    def draw_ghost_wall(self, board, grid_x, grid_y, orientation):
        # Only draw if valid range
        if 0 <= grid_x < board.size-1 and 0 <= grid_y < board.size-1:
            self._draw_wall_graphic(board.size, (grid_x, grid_y), orientation, is_ghost=True)

    # --- Helpers ---
    def _get_offsets(self, size):
        """Calculate centering offsets dynamically."""
        total_w = size * (CELL_SIZE + MARGIN) - MARGIN
        total_h = size * (CELL_SIZE + MARGIN) - MARGIN
        # We shift left slightly to leave room for the HUD on the right
        start_x = (SCREEN_WIDTH - 250 - total_w) // 2
        # But ensure it's not offscreen
        if start_x < 20: start_x = 20
        start_y = (SCREEN_HEIGHT - total_h) // 2
        return start_x, start_y

    def _draw_grid(self, board):
        for c in range(board.size):
            for r in range(board.size):
                rect = self._get_cell_rect(board.size, c, r)
                pygame.draw.rect(self.screen, GRID_COLOR, rect)

        # Walls
        for wall in board.walls:
            self._draw_wall_graphic(board.size, wall[0], wall[1])

    def _draw_players(self, board, p1, p2):
        self._draw_pawn(board, p1)
        self._draw_pawn(board, p2)

    def _get_cell_rect(self, size, c, r):
        ox, oy = self._get_offsets(size)
        x = ox + c * (CELL_SIZE + MARGIN)
        y = oy + r * (CELL_SIZE + MARGIN)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def _draw_pawn(self, board, player):
        rect = self._get_cell_rect(board.size, player.pos[0], player.pos[1])
        center = rect.center
        pygame.draw.circle(self.screen, BLACK, center, int(CELL_SIZE * 0.45)) # Outline
        pygame.draw.circle(self.screen, player.color, center, int(CELL_SIZE * 0.4))

    def _draw_wall_graphic(self, size, pos, orientation, is_ghost=False):
        c, r = pos
        ox, oy = self._get_offsets(size)
        x = ox + c * (CELL_SIZE + MARGIN) + CELL_SIZE
        y = oy + r * (CELL_SIZE + MARGIN) + CELL_SIZE

        color = WALL_COLOR if not is_ghost else HOVER_COLOR

        if orientation == 'V':
            wall_rect = pygame.Rect(x, y - CELL_SIZE, MARGIN, WALL_LENGTH)
        else:
            wall_rect = pygame.Rect(x - CELL_SIZE, y, WALL_LENGTH, MARGIN)

        pygame.draw.rect(self.screen, color, wall_rect)
