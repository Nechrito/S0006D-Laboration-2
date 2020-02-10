import sys

import pygame

from src.code.engine.GameTime import GameTime
from src.code.pathfinding.PathManager import PathManager


class UserInput:
    def __init__(self, game):
        self.instance = game
        self.timeScaleCurrent = GameTime.timeScale

    def update(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                # Exit
                if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Load different map
                if event.key == pygame.K_1:
                    self.instance.loadMap(1)
                    return
                if event.key == pygame.K_2:
                    self.instance.loadMap(2)
                    return
                if event.key == pygame.K_3:
                    self.instance.loadMap(3)
                    return
                if event.key == pygame.K_4:
                    self.instance.loadMap(4)
                    return

                # Toggle mouse
                if event.key == pygame.K_LALT:
                    self.instance.realCursorEnabled = not self.instance.realCursorEnabled
                    pygame.mouse.set_visible(self.instance.realCursorEnabled)
                    pygame.event.set_grab(not self.instance.realCursorEnabled)

                # Pause game
                if event.key == pygame.K_SPACE:
                    if self.instance.paused:
                        GameTime.setScale(self.timeScaleCurrent)
                    else:
                        GameTime.setScale(0.00001)

                    self.instance.paused = not self.instance.paused

                # Speed up
                if not self.instance.paused and event.key == pygame.K_LSHIFT:
                    self.timeScaleCurrent = GameTime.setScale(self.timeScaleCurrent * 2)
                # Slow down
                if not self.instance.paused and event.key == pygame.K_LCTRL:
                    self.timeScaleCurrent = GameTime.setScale(self.timeScaleCurrent / 2)

            if event.type == pygame.MOUSEBUTTONDOWN:
                square = self.instance.selectedTile()  # nearest square to mouse
                if square:

                    if event.button == 1 and not self.instance.isObstacle(square):  # LEFT-CLICK
                        self.instance.setStart(square.position)
                    elif event.button == 2:  # MIDDLE-CLICK
                        self.instance.setObstacle()
                    elif event.button == 3 and not self.instance.isObstacle(square):  # RIGHT CLICK
                        self.instance.setEnd(square.position)

                    # update the path
                    self.instance.updatePaths()
