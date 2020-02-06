from enum import Enum


class AgentStates(Enum):
    CollectMoney = 0  # Work w/ 2 different locations & Buissiness
    Purchase = 1
    Sleep = 2
    Eat = 3
    Drink = 4
    Hangout = 5
