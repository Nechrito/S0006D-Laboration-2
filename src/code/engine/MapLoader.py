import pygame
import pytmx


class Map:
    def __init__(self, filename):
        self.instance = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.instance.width * self.instance.tilewidth
        self.height = self.instance.height * self.instance.tileheight

    def render(self, surface):
        tileImg = self.instance.get_tile_image_by_gid  # Fetches the image represented by the ID
        for layer in self.instance.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tileImg(gid)
                    if tile:
                        surface.blit(tile, (x * self.instance.tilewidth,
                                            y * self.instance.tileheight))

    def create(self):
        surface = pygame.Surface((self.width, self.height))
        self.render(surface)
        return surface
