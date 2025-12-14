# main.py
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

    # State: 'MENU', 'GAME', 'GAMEOVER'
    state = 'MENU'
    game_mode = None # 'PvP' or 'PvAI'
    
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
                    btn1, btn2 = ui.draw_menu() # Get rects to check click
                    mx, my = pygame.mouse.get_pos()
                    if btn1.collidepoint((mx, my)):
                        game_mode = 'PvP'
                        state = 'GAME'
                        # Init Game
                        board = Board()
                        p1 = Player((4, 8), PLAYER_1_COLOR, 0, 1)
                        p2 = Player((4, 0), PLAYER_2_COLOR, 8, 2)
                        valid_moves = board.get_valid_moves(p1, p2)
                    elif btn2.collidepoint((mx, my)):
                        game_mode = 'PvAI'
                        state = 'GAME'
                        # Init Game
                        board = Board()
                        p1 = Player((4, 8), PLAYER_1_COLOR, 0, 1)
                        p2 = Player((4, 0), PLAYER_2_COLOR, 8, "AI")
                        ai_agent = AI(2)
                        valid_moves = board.get_valid_moves(p1, p2)

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
                            valid_moves = board.get_valid_moves(current_player, opponent) if input_mode == 'MOVE' else []

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        gx = (mx - BOARD_OFFSET_X) // (CELL_SIZE + MARGIN)
                        gy = (my - BOARD_OFFSET_Y) // (CELL_SIZE + MARGIN)

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
            opponent = p2 if turn == 1 else p1
            
            # AI TURN
            if game_mode == 'PvAI' and turn == 2:
                # Force draw before AI thinks (so user sees their own move immediately)
                ui.draw_game_screen(board, p1, p2, turn, input_mode, wall_orientation)
                pygame.display.flip()
                
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
            ui.draw_menu()
        elif state == 'GAME':
            ui.draw_game_screen(board, p1, p2, turn, input_mode, wall_orientation)
            
            if turn == 1 or game_mode == 'PvP': # Only highlight valid moves for humans
                if input_mode == 'MOVE':
                    ui.highlight_moves(valid_moves)
                elif input_mode == 'WALL':
                    mx, my = pygame.mouse.get_pos()
                    gx = (mx - BOARD_OFFSET_X) // (CELL_SIZE + MARGIN)
                    gy = (my - BOARD_OFFSET_Y) // (CELL_SIZE + MARGIN)
                    ui.draw_ghost_wall(gx, gy, wall_orientation)
                    
        elif state == 'GAMEOVER':
            screen.fill(BACKGROUND)
            txt = ui.title_font.render(f"PLAYER {winner} WINS!", True, WHITE)
            screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
            sub = ui.font.render("Press SPACE to restart", True, TEXT_COLOR)
            screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60)))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                state = 'MENU'

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()