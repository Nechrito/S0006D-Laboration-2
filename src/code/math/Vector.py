import numbers
import math

from src.Settings import SETTINGS


class vec2:
    def __init__(self, X=0, Y=0):
        if isinstance(X, tuple) or isinstance(X, vec2):
            self.X = X[0]
            self.Y = X[1]
        else:
            self.X = X
            self.Y = Y

    @property
    def LocalX(self):
        return self.X // (SETTINGS.TILE_SCALE[0] - 1)

    @property
    def LocalY(self):
        return self.Y // (SETTINGS.TILE_SCALE[1] - 1)

    def __getitem__(self, item):
        if item == 0:
            return self.X
        if item == 1:
            return self.Y

    def __getattr__(self, name):
        return self[name]

    def __add__(self, other):
        if isinstance(other, tuple):
            return vec2(self.X + other[0], self.Y + other[1])
        if isinstance(other, vec2):
            return vec2(self.X + other.X, self.Y + other.Y)
        if isinstance(other, int):
            return vec2(int(self.X + other), int(self.Y + other))
        if isinstance(other, numbers.Number):
            return vec2(self.X + other, self.Y + other)

    def __sub__(self, other):
        if isinstance(other, tuple):
            return vec2(self.X - other[0], self.Y - other[1])
        if isinstance(other, vec2):
            return vec2(self.X - other.X, self.Y - other.Y)
        if isinstance(other, numbers.Number):
            return vec2(self.X - other, self.Y - other)

    def __truediv__(self, other):
        if isinstance(other, tuple):
            return vec2(self.X / other[0], self.Y / other[1])
        if isinstance(other, vec2):
            return vec2(self.X // other.X, self.Y // other.Y)
        if isinstance(other, float):
            return vec2(self.X // other, self.Y // other)
        if isinstance(other, numbers.Number):
            return vec2(self.X // other, self.Y // other)

    def __mul__(self, other):
        if isinstance(other, tuple):
            return vec2(self.X * other[0], self.Y * other[1])
        if isinstance(other, vec2):
            return vec2(self.X * other.X, self.Y * other.Y)
        if isinstance(other, float):
            return vec2(self.X * other, self.Y * other)
        if isinstance(other, numbers.Number):
            return vec2(self.X * other, self.Y * other)

    def distance(self, other):
        return math.sqrt(((self.X - other[0]) ** 2) + ((self.Y - other[1]) ** 2))

    def log(self, local=False):
        if local:
            print("Local: " + str(self.LocalX) + " | " + str(self.LocalY))
        else:
            print(str(self.X) + " | " + str(self.Y))

    def break_tie(self, start, goal):
        dx1 = self.X - goal.X
        dy1 = self.Y - goal.Y
        dx2 = start.X - goal.X
        dy2 = start.Y - goal.Y
        return abs(dx1 * dy2 - dx2 * dy1) * 0.001

    def __eq__(self, other):
        if isinstance(other, vec2):
            if self.X != other.X:
                return False
            if self.Y != other.Y:
                return False
            return True

    def __hash__(self):
        return hash(self.X) + hash(self.Y)

    @property
    def toInt(self):
        x = int(self.X)
        y = int(self.Y)
        return vec2(x, y)

    @property
    def lengthSquared(self):
        return self.X * self.X + self.Y * self.Y

    @property
    def length(self):
        return math.sqrt(self.lengthSquared)

    @property
    def normalized(self):
        length = self.length
        if length != 0:
            return vec2(self.X / length, self.Y / length)
        return self

    @property
    def tuple(self):
        return self.X, self.Y
