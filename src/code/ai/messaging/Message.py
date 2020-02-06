from src.code.engine.Entity import Entity
from src.code.engine.GameTime import GameTime


class Message:

    @classmethod
    def sendConsole(cls, sender: Entity, message: str):
        # text/color formatting achieved through
        #   https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python/21786287#21786287
        #   https://stackoverflow.com/questions/39473297/how-do-i-print-colored-output-with-python-3
        timeFormatted = '\x1b[1;31m' + '[' + GameTime.timeElapsed() + "] " + '\x1b[0m'
        nameColored = '\x1b[2;34m' + sender.name + '\x1b[0m'
        messageFormatted = '\x1b[3;37m' + message + '\x1b[0m'
        print(timeFormatted + nameColored + ": " + messageFormatted)
