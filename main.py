import sys
from os import path

import pygame

from src.Game import Game
from src.code.engine.GameTime import GameTime
from src.code.engine.UserInput import UserInput

# Only executes the main method if this module is executed as the main script
from src.code.pathfinding.PathManager import PathManager

if __name__ == "__main__":

    folder = "resources/"
    if getattr(sys, 'frozen', False):
        directory = path.dirname(sys.executable)
    else:
        directory = path.dirname(__file__)

    GameTime.init()

    instance = Game(directory, folder)
    instance.loadMap(1)

    userInput = UserInput(instance)

    while True:

        # Core
        GameTime.updateTicks()
        instance.update()
        instance.draw()
        userInput.update()

        # Lessen CPU usage of the app
        if not pygame.key.get_focused():
            pygame.time.wait(100)
