# Application settings
from src.code.math.Vector import vec2


class SETTINGS:
    TITLE = "S0006D - Laboration 1 - Philip Lindh"

    # for 4:3 ratio map needs to be in that format, unless built in pygame
    #   Note: these gets overriden in Game.py
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None
    SCREEN_RESOLUTION = None

    TILE_SIZE = None
    TILE_SCALE = None
    TILE_WIDTH = None
    TILE_HEIGHT = None

    GRID_BOUNDS = None

    FPS = 200
    MAP_LEVEL = 1

    # Global lists
    PathTiles = []
    ObstacleTiles = []

    # Resource files direct path
    MAP_OLD = "map/map_old.tmx"
    MAP_1 = "map/map1.tmx"
    MAP_2 = "map/map2.tmx"
    MAP_3 = "map/map3.tmx"
    MAP_REF1 = "map/ref/Map1.txt"
    MAP_REF2 = "map/ref/Map2.txt"
    MAP_REF3 = "map/ref/Map3.txt"

    TILE_OBSTACLE = "tiles/wall.png"
    TILE_START = "tiles/start.png"
    TILE_GOAL = "tiles/goal.png"

    ENTITY_SENSEI = "img/sensei.png"

    ICON_PATH = "icon/Game.png"
    FONT_BLACK = "fonts/Roboto-Black.ttf"
    FONT_BOLD = "fonts/Roboto-Bold.ttf"
    FONT_REGULAR = "fonts/Roboto-Regular.ttf"
