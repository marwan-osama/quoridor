import pygame
import sys
from settings import *
from board import Board
from player import Player
from ui import UI
from ai import AI

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    ui = UI(screen)

    state = 'MENU' # State: 'MENU', 'GAME', 'GAMEOVER'
    game_mode = None # 'PvP' or 'PvAI'
    current_board_size = 9 # Default game size

    # Game Objects
    board = None
    p1 = None
    p2 = None
    ai_agent = None
    turn = 1

    # Input State
    input_mode = 'MOVE'
    wall_orientation = 'H'
    valid_moves = []
    winner = None

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == 'MENU':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    btn1, btn2, btn3 = ui.draw_menu(current_board_size)
                    mx, my = pygame.mouse.get_pos()

                    # 1. Start PvP
                    if btn1.collidepoint((mx, my)):
                        game_mode = 'PvP'
                        state = 'GAME'
                        board = Board(size=current_board_size)
                        # Center pawns based on size
                        mid = current_board_size // 2
                        p1 = Player((mid, current_board_size - 1), PLAYER_1_COLOR, 0, 1)
                        p2 = Player((mid, 0), PLAYER_2_COLOR, current_board_size - 1, 2)
                        valid_moves = board.get_valid_moves(p1, p2)

                    # 2. Start PvAI
                    elif btn2.collidepoint((mx, my)):
                        game_mode = 'PvAI'
                        state = 'GAME'
                        board = Board(size=current_board_size)
                        mid = current_board_size // 2
                        p1 = Player((mid, current_board_size - 1), PLAYER_1_COLOR, 0, 1)
                        p2 = Player((mid, 0), PLAYER_2_COLOR, current_board_size - 1, "AI")
                        ai_agent = AI(2)
                        valid_moves = board.get_valid_moves(p1, p2)

                    # 3. Toggle Size
                    elif btn3.collidepoint((mx, my)):
                        # Cycle 5 -> 7 -> 9 -> 11 -> 5
                        if current_board_size == 9: current_board_size = 11
                        elif current_board_size == 11: current_board_size = 5
                        elif current_board_size == 5: current_board_size = 7
                        else: current_board_size = 9

            elif state == 'GAME':
                current_player = p1 if turn == 1 else p2
                opponent = p2 if turn == 1 else p1

                # Input Handling for Human
                if not (game_mode == 'PvAI' and turn == 2):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            wall_orientation = 'V' if wall_orientation == 'H' else 'H'
                        if event.key == pygame.K_TAB:
                            input_mode = 'WALL' if input_mode == 'MOVE' else 'MOVE'
                            if input_mode == 'MOVE':
                                valid_moves = board.get_valid_moves(current_player, opponent)
                            else:
                                valid_moves = []

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()

                        # Dynamic conversion from mouse to grid requires dynamic offset
                        ox, oy = ui._get_offsets(current_board_size)
                        gx = (mx - ox) // (CELL_SIZE + MARGIN)
                        gy = (my - oy) // (CELL_SIZE + MARGIN)

                        if input_mode == 'MOVE':
                            if (gx, gy) in valid_moves:
                                current_player.move((gx, gy))
                                if current_player.pos[1] == current_player.goal_row:
                                    winner = turn
                                    state = 'GAMEOVER'
                                else:
                                    turn = 3 - turn # Switch 1 <-> 2
                                    valid_moves = board.get_valid_moves(opponent, current_player) # Prep for next

                        elif input_mode == 'WALL':
                            if current_player.has_walls():
                                if board.place_wall(gx, gy, wall_orientation, p1, p2):
                                    current_player.use_wall()
                                    turn = 3 - turn
                                    valid_moves = [] # Reset

        # Logic Update
        if state == 'GAME':
            current_player = p1 if turn == 1 else p2

            # AI TURN
            if game_mode == 'PvAI' and turn == 2:
                # Force draw before AI thinks
                ui.draw_game_screen(board, p1, p2, turn, input_mode, wall_orientation)
                pygame.display.flip()

                # AI Logic
                move = ai_agent.get_best_move(board, p1, p2)
                ai_agent.apply_move(board, p2, p1, move)

                if p2.pos[1] == p2.goal_row:
                    winner = 2
                    state = 'GAMEOVER'
                else:
                    turn = 1
                    valid_moves = board.get_valid_moves(p1, p2) # Prep for human

        # Drawing
        if state == 'MENU':
            ui.draw_menu(current_board_size)
        elif state == 'GAME':
            ui.draw_game_screen(board, p1, p2, turn, input_mode, wall_orientation)

            if turn == 1 or game_mode == 'PvP': # Only highlight valid moves for humans
                if input_mode == 'MOVE':
                    ui.highlight_moves(board, valid_moves)
                elif input_mode == 'WALL':
                    mx, my = pygame.mouse.get_pos()
                    ox, oy = ui._get_offsets(current_board_size)
                    gx = (mx - ox) // (CELL_SIZE + MARGIN)
                    gy = (my - oy) // (CELL_SIZE + MARGIN)
                    ui.draw_ghost_wall(board, gx, gy, wall_orientation)

        elif state == 'GAMEOVER':
            screen.fill(BACKGROUND)

            win_text = f"PLAYER {winner} WINS!"
            if game_mode == 'PvAI' and winner == 2:
                win_text = "COMPUTER WINS!"

            txt = ui.title_font.render(win_text, True, WHITE)
            screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

            sub = ui.font.render("Press SPACE to restart", True, TEXT_COLOR)
            screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60)))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                state = 'MENU'
                turn = 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
