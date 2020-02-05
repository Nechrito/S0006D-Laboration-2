import sys
import pygame

from src.Game import Game
from src.code.engine.GameTime import GameTime

# Only executes the main method if this module is executed as the main script
if __name__ == "__main__":

    instance = Game()
    instance.load()

    timeScaleCached = 1
    timeScaleActive = timeScaleCached
    GameTime.setScale(timeScaleActive)

    while True:

        for event in pygame.event.get():
            # Exit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP and event.key == pygame.K_LALT:
                instance.realCursorEnabled = not instance.realCursorEnabled
                pygame.mouse.set_visible(instance.realCursorEnabled)
                pygame.event.set_grab(not instance.realCursorEnabled)

            # Pause game
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if instance.paused:
                    GameTime.setScale(timeScaleActive)
                else:
                    GameTime.setScale(0.00001)

                instance.paused = not instance.paused

            # Speed up
            if not instance.paused and event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
                timeScaleActive = GameTime.setScale(timeScaleActive * 2)
            # Slow down
            if not instance.paused and event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
                timeScaleActive = GameTime.setScale(timeScaleActive / 2)

        # Core
        instance.update()
        instance.draw()

        # Lessen CPU usage of the app
        if not pygame.key.get_focused():
            pygame.time.wait(100)
