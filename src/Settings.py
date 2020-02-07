
# Application settings
from src.code.math.vec2 import vec2

TITLE = "S0006D - Laboration 1 - Philip Lindh"
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 768
SCREEN_RESOLUTION = [SCREEN_WIDTH, SCREEN_HEIGHT]

TILE_SIZE = 48
GRID_SIZE = TILE_SIZE + int(TILE_SIZE / 2)
FPS = 200

# Global lists
Walkables = []
Obstacles = []

# Resource files direct path
MAP_OLD = "map/map_old.tmx"
MAP_1 = "map/map1.tmx"
MAP_2 = "map/map2.tmx"
MAP_3 = "map/map3.tmx"

TILE_OBSTACLE = "tiles/wall.png"
TILE_START = "tiles/start.png"
TILE_GOAL = "tiles/goal.png"

ICON_PATH = "icon/Game.png"
FONT_BLACK = "fonts/Roboto-Black.ttf"
FONT_BOLD = "fonts/Roboto-Bold.ttf"
FONT_REGULAR = "fonts/Roboto-Regular.ttf"

