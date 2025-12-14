# main.py
import pygame
import sys
from settings import *
from board import Board
from player import Player
from ui import UI

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    # Init Game Objects
    board = Board()
    # P1 starts bottom (row 8), goes to row 0. P2 starts top (row 0), goes to row 8.
    p1 = Player((4, 8), PLAYER_1_COLOR, 0, 1)
    p2 = Player((4, 0), PLAYER_2_COLOR, 8, 2)
    ui = UI(screen)

    turn = 1 # 1 or 2
    selected_pawn = False
    valid_moves = []
    
    # Input Mode: 'MOVE' or 'WALL'
    # For simplicity in this phase, let's use Right Click to toggle Wall Placement mode
    input_mode = 'MOVE' 
    wall_orientation = 'H' # 'H' or 'V', toggle with Spacebar

    running = True
    while running:
        screen.fill(BACKGROUND)
        
        # 1. Determine current player
        current_player = p1 if turn == 1 else p2
        opponent = p2 if turn == 1 else p1

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    wall_orientation = 'V' if wall_orientation == 'H' else 'H'
                if event.key == pygame.K_TAB:
                    input_mode = 'WALL' if input_mode == 'MOVE' else 'MOVE'

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # Logic to convert mouse pixels to Grid Coordinates
                # This is a rough estimation logic
                grid_x = (mx - BOARD_OFFSET_X) // (CELL_SIZE + MARGIN)
                grid_y = (my - BOARD_OFFSET_Y) // (CELL_SIZE + MARGIN)
                
                if input_mode == 'MOVE':
                    # Check if clicked on a valid move
                    if (grid_x, grid_y) in valid_moves:
                        current_player.move((grid_x, grid_y))
                        # Check Win
                        if current_player.pos[1] == current_player.goal_row:
                            print(f"Player {turn} Wins!")
                            running = False
                        turn = 2 if turn == 1 else 1
                        valid_moves = []
                    else:
                        # Calculate moves for current player to show highlights
                        valid_moves = board.get_valid_moves(current_player, opponent)

                elif input_mode == 'WALL':
                    if current_player.has_walls():
                        # For wall placement, grid_x/y represents the top-left cell 
                        # relative to the wall gap.
                        if board.place_wall(grid_x, grid_y, wall_orientation, p1, p2):
                            current_player.use_wall()
                            turn = 2 if turn == 1 else 1
                            valid_moves = [] # Clear move highlights if any

        # 3. Drawing
        ui.draw_board(board)
        ui.draw_players(p1, p2)

        if input_mode == 'MOVE':
            ui.highlight_moves(valid_moves)
        elif input_mode == 'WALL':
            # Draw ghost wall at mouse position
            mx, my = pygame.mouse.get_pos()
            gx = (mx - BOARD_OFFSET_X) // (CELL_SIZE + MARGIN)
            gy = (my - BOARD_OFFSET_Y) // (CELL_SIZE + MARGIN)
            ui._draw_wall_graphic((gx, gy), wall_orientation) # Using internal helper for preview

        ui.draw_stats(p1, p2, turn)

        # Mode Indicator
        mode_text = ui.font.render(f"Mode: {input_mode} (Tab) | Orient: {wall_orientation} (Space)", True, WHITE)
        screen.blit(mode_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()