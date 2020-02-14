
class SETTINGS:
    TITLE = "S0006D - Laboration 1 - Philip Lindh"

    SCREEN_WIDTH = 768
    SCREEN_HEIGHT = 768

    MAP_WIDTH = None
    MAP_HEIGHT = None

    # Outer bounds of window
    GRID_BOUNDS = None

    TILE_SCALE = None

    MAX_FPS = 200
    CURRENT_LEVEL = 1

    # Global accessors
    Graph = {}
    PathTiles = []
    ObstacleTiles = []
    BackgroundTIles = []
    TilesAll = []
    #BuildingObjects = []

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

    @classmethod
    def configure(cls, mapWidth, mapHeight):
        cls.MAP_WIDTH = mapWidth
        cls.MAP_HEIGHT = mapHeight

        cls.SCREEN_RESOLUTION = [cls.SCREEN_WIDTH, cls.SCREEN_HEIGHT]

        # upscaled tilesize
        scalex = SETTINGS.SCREEN_WIDTH // (cls.MAP_WIDTH // 16)
        scaley = SETTINGS.SCREEN_HEIGHT // (cls.MAP_HEIGHT // 16)
        cls.TILE_SCALE = (scalex, scaley)

        cls.GRID_BOUNDS = (cls.SCREEN_WIDTH + scalex // 2, cls.SCREEN_HEIGHT + scaley // 2)

    @classmethod
    def getNode(cls, position):

        try:
            return cls.Graph[position.LocalX-1][position.LocalY-1]
        except IndexError:
            pass
            print("-1")

        #for col in range(len(SETTINGS.Graph)):
        #    for row in range(len(SETTINGS.Graph[col])):
        #        current = SETTINGS.Graph[col][row]
        #        if current.position == position:
        #            return current

    @classmethod
    def index2D(cls, data, search):
        for i, e in enumerate(data):
            try:
                return i, e.index(search)
            except ValueError:
                pass
        raise ValueError("{} is not in list".format(repr(search)))
