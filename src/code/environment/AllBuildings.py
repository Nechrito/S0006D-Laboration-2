from .Building import Building
from ..math.Vector import vec2


def getLTU():
    return Building(vec2(144, 596), "LTU", "Student")


def getClub():
    return Building(vec2(336, 692), "Club", "Bartender")


def getStackHQ():
    return Building(vec2(484, 836), "Stackoverflow HQ", "Smartass")


def getDrink():
    return Building(vec2(736, 596), "Bar")


def getResturant():
    return Building(vec2(496, 404), "Resturant")


def getStore():
    return Building(vec2(704, 372), "Store")


def getHotel():
    return Building(vec2(852, 404), "Home")


def getHangout():
    return Building(vec2(944, 788), "Hangout")
