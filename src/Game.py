import sys
import pygame
import pygame.freetype
from os import path

from src.Settings import *
from src.code.engine.Entity import Entity
from src.code.Camera import CameraInstance
from src.code.engine.GameTime import GameTime
from src.code.engine.MapLoader import Map
from src.code.ai.behaviour.states.CollectMoney import CollectMoney
from src.code.ai.behaviour.Global import Global
from src.code.ai.behaviour.states.Hangout import Hangout
from src.code.ai.behaviour.states.Purchase import Purchase
from src.code.environment.AllBuildings import getClub, getDrink, getLTU, getHangout, getHotel, getStackHQ, getStore, getResturant
from src.code.engine.Renderer import Renderer


def getRealFilePath(fileName):
    if getattr(sys, 'frozen', False):
        directory = path.dirname(sys.executable)
        folder = "src/resources/"
    else:
        directory = path.dirname(__file__)
        folder = "resources/"

    return path.join(directory, folder + fileName)


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.freetype.init()

        logo = pygame.image.load(getRealFilePath(ICON_PATH))
        pygame.display.set_icon(logo)
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode(RESOLUTION)
        self.font = pygame.freetype.Font(getRealFilePath(FONT_BOLD), int(SCREEN_HEIGHT * 24 / SCREEN_WIDTH))
        self.fontBold = pygame.freetype.Font(getRealFilePath(FONT_BOLD), int(SCREEN_HEIGHT * 38 / SCREEN_WIDTH))

    def load(self):

        self.renderer = Renderer(self.surface)

        self.map = Map(getRealFilePath("map/environment.tmx"))
        self.mapImg = self.map.create()
        self.mapRect = self.mapImg.get_rect()

        GameTime.init()

        self.camera = CameraInstance(self.map.width, self.map.height)

        self.clock = pygame.time.Clock()
        self.paused = False

        self.cursorEnabled = False
        pygame.mouse.set_visible(self.cursorEnabled)
        pygame.event.set_grab(not self.cursorEnabled)

        self.cursor = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.cursorRect = pygame.Rect(self.cursor, (10, 10))

        self.buildings = [getClub(), getDrink(), getResturant(), getStore(),
                          getStackHQ(), getHotel(), getHangout(), getLTU()]

        sensei = pygame.image.load(getRealFilePath('img/sensei.png'))
        hatguy = pygame.image.load(getRealFilePath('img/hat-guy.png'))

        self.entityGroup = pygame.sprite.Group()
        self.characterAlex = Entity("Alex", Hangout(), Global(), self.entityGroup, 495, 405, sensei)
        self.characterWendy = Entity("Wendy", CollectMoney(), Global(), self.entityGroup, 150, 610, hatguy)
        self.characterJohn = Entity("John", Purchase(), Global(), self.entityGroup, 700, 380, sensei)
        self.characterJames = Entity("James", CollectMoney(), Global(), self.entityGroup, 940, 400, hatguy)

        self.entities = [self.characterAlex, self.characterWendy, self.characterJohn, self.characterJames]

        for char in self.entities:
            self.entityGroup.add(char)

    def update(self):

        if not self.paused:
            pygame.display.set_caption(TITLE + " | Speed: " + str(GameTime.timeScale) + " | FPS " + "{:.0f}".format(self.clock.get_fps()) + " | Date: " + GameTime.timeElapsed())

        GameTime.updateTicks()

        if not self.cursorEnabled:
            # this would've been great if I was aware of it earlier.. pygame.math.Vector2(pygame.mouse.get_pos()) // TILESIZE
            (x, y) = pygame.mouse.get_rel()
            self.cursor = (int(self.cursor[0] + x), int(self.cursor[1] + y))
            self.cursorRect = pygame.Rect((self.cursor[0] - 200, self.cursor[1] - 200), (400, 400))

        self.entityGroup.update()

        lastVal = 0
        selected = None
        for character in self.entities:
            distance = character.distanceTo((self.cursorRect.centerx, self.cursorRect.centery))
            if distance < lastVal or lastVal == 0:
                character.update()
                selected = character
                lastVal = character.distanceTo((self.cursorRect.centerx, self.cursorRect.centery))

        if selected:
            self.camera.update(selected)

    def draw(self):

        self.renderer.clear(self.mapImg, self.camera.moveRect(self.mapRect))

        if not self.cursorEnabled:
            self.renderer.renderRect((self.cursorRect.width, self.cursorRect.height),
                                     (self.cursorRect.left, self.cursorRect.top), (37, 37, 38), 80)

            self.renderer.renderRect((10, 10), (self.cursorRect.centerx, self.cursorRect.centery), (37, 37, 38), 200)

        for sprite in self.entityGroup:
            self.surface.blit(sprite.image, self.camera.moveSprite(sprite))

        for char in self.entities:
            (x, y) = (char.position[0], char.position[1] + self.camera.y - TILESIZE - 5)
            self.renderer.renderRect((60, 18), (x - 30, y - 9), (0, 0, 0), 170)
            self.renderer.renderText(char.name, (x, y), self.font)

        for building in self.buildings:
            self.renderer.renderText(building.name, (building.position[0], building.position[1] + self.camera.y - TILESIZE * 5), self.fontBold)

        self.drawEntitiesInfo()

        self.clock.tick(FPS)

    def drawEntitiesInfo(self):

        count = 0
        for i in range(len(self.entities)):

            entity = self.entities[i]
            relativePosition = (entity.position[0] + self.camera.x, entity.position[1] + self.camera.y + TILESIZE)

            if not self.cursorRect.collidepoint(relativePosition[0], relativePosition[1]):
                continue

            if not self.cursorEnabled:
                pygame.draw.line(self.surface, (220, 220, 220), (self.cursorRect.centerx + 5, self.cursorRect.centery + 5), relativePosition, 3)

            self.renderer.renderRect((150, 150), (count * 150, 50), (0, 0, 0), 160)

            self.renderer.append(entity.name + " (" + str(entity.stateMachine.currentState) + ")")
            self.renderer.append("Fatigue: {0}%".format("{:.0f}".format(float(entity.fatigue))))
            self.renderer.append("Hunger: {0}%".format("{:.0f}".format(float(entity.hunger))))
            self.renderer.append("Thirst: {0}%".format("{:.0f}".format(float(entity.thirst))))
            self.renderer.append("Bank: {0}$".format("{:.0f}".format(float(entity.bank))))
            self.renderer.renderTexts((25 + SCREEN_WIDTH * 0.05 + 150 * count, SCREEN_HEIGHT * 0.10), self.font, (255, 255, 255))

            count += 1
