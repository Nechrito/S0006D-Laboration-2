from .Building import Building
from ..math.Vector import vec2


def getLTU():
    return Building(vec2(850, 415), "LTU", "Student")


def getClub():
    return Building(vec2(342, 705), "Club", "Bartender")


def getStackHQ():
    return Building(vec2(483, 844), "Stackoverflow HQ", "Smartass")


def getDrink():
    return Building(vec2(150, 610), "Bar")


def getResturant():
    return Building(vec2(500, 415), "Resturant")


def getStore():
    return Building(vec2(707, 385), "Store")


def getHotel():
    return Building(vec2(735, 603), "Home")


def getHangout():
    return Building(vec2(945, 800), "Hangout")
