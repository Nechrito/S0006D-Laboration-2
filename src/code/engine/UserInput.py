import sys

import pygame

from src.code.engine.GameTime import GameTime


class UserInput:
    def __init__(self, game):
        self.instance = game
        self.timeScaleCurrent = GameTime.timeScale

    def update(self):
        for event in pygame.event.get():
            # Exit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Toggle mouse
            if event.type == pygame.KEYUP and event.key == pygame.K_LALT:
                self.instance.realCursorEnabled = not self.instance.realCursorEnabled
                pygame.mouse.set_visible(self.instance.realCursorEnabled)
                pygame.event.set_grab(not self.instance.realCursorEnabled)

            # Pause game
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.instance.paused:
                    GameTime.setScale(self.timeScaleCurrent)
                else:
                    GameTime.setScale(0.00001)

                self.instance.paused = not self.instance.paused

            # Speed up
            if not self.instance.paused and event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                self.timeScaleCurrent = GameTime.setScale(self.timeScaleCurrent * 2)
            # Slow down
            if not self.instance.paused and event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
                self.timeScaleCurrent = GameTime.setScale(self.timeScaleCurrent / 2)

            # Belongs in Game.py but i'm lazy
            if event.type == pygame.MOUSEBUTTONDOWN:
                square = self.instance.selectedTile()  # nearest square to mouse
                if square:
                    if event.button == 1 and not self.instance.isObstacle(square):  # LEFT-CLICK
                        self.instance.startPos = square.position
                    if event.button == 2:  # MIDDLE-CLICK
                        self.instance.setObstacle()
                    if event.button == 3 and not self.instance.isObstacle(square):  # RIGHT CLICK
                        self.instance.goalPos = square.position

                    # update the path
                    self.instance.updateMap()