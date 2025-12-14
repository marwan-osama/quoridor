# settings.py

# Window Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900 # Extra height for text/stats
CAPTION = "Quoridor - Graph Implementation"

# Board Settings
BOARD_SIZE = 9
CELL_SIZE = 60
MARGIN = 10  # Space between cells (where walls go)
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 100

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (40, 40, 40)
GRID_COLOR = (200, 200, 200)
WALL_COLOR = (219, 172, 52)     # Gold/Brown
HOVER_COLOR = (255, 255, 255, 100) # Semi-transparent
PLAYER_1_COLOR = (200, 50, 50)  # Red
PLAYER_2_COLOR = (50, 50, 200)  # Blue
VALID_MOVE_COLOR = (50, 200, 50) # Green

# Wall Specs
WALL_THICKNESS = MARGIN
WALL_LENGTH = (CELL_SIZE * 2) + MARGIN