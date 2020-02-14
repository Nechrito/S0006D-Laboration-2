from .Building import Building
from ..math.Vector import vec2


def getLTU():
    return Building(vec2(515, 277), "LTU", "Student")


def getClub():
    return Building(vec2(615, 295), "Club", "Bartender")


def getStackHQ():
    return Building(vec2(608, 291), "Stackoverflow HQ", "Smartass")


def getDrink():
    return Building(vec2(540, 438), "Bar")


def getResturant():
    return Building(vec2(590, 582), "Resturant")


def getStore():
    return Building(vec2(340, 630), "Store")


def getHotel():
    return Building(vec2(230, 510), "Home")


def getHangout():
    return Building(vec2(90, 440), "Hangout")
