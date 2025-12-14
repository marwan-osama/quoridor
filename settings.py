# Window Settings
SCREEN_WIDTH = 900 # Made wider for sidebar/instructions
SCREEN_HEIGHT = 700
CAPTION = "Quoridor - Graph Implementation"

# Board Settings
BOARD_SIZE = 9
CELL_SIZE = 50
MARGIN = 10
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 100

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (40, 40, 40)
GRID_COLOR = (200, 200, 200)
WALL_COLOR = (219, 172, 52)
HOVER_COLOR = (255, 255, 255, 100)
PLAYER_1_COLOR = (200, 50, 50)  # Red (Human)
PLAYER_2_COLOR = (50, 50, 200)  # Blue (AI/Human)
VALID_MOVE_COLOR = (50, 200, 50)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (100, 100, 100)

# Wall Specs
WALL_THICKNESS = MARGIN
WALL_LENGTH = (CELL_SIZE * 2) + MARGIN

# AI Settings
AI_DEPTH = 2  # Depth 3 is smarter but slower in Python. Depth 2 is fast.
INF = 999999
