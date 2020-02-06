import numbers
import math


class vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, tuple):
            return vec2(self.x + other[0], self.y + other[1])
        if isinstance(other, vec2):
            return vec2(self.x + other.x, self.y + other.y)
        if isinstance(other, numbers.Number):
            return vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, tuple):
            return vec2(self.x - other[0], self.y - other[1])
        if isinstance(other, vec2):
            return vec2(self.x - other.x, self.y - other.y)
        if isinstance(other, numbers.Number):
            return vec2(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, tuple):
            return vec2(self.x * other[0], self.y * other[1])
        if isinstance(other, vec2):
            return vec2(self.x * other.x, self.y * other.y)
        if isinstance(other, numbers.Number):
            return vec2(self.x * other, self.y * other)

    def distance(self, other):
        return math.sqrt( (self.x - other.x) ** 2 + (self.y - other.y) ** 2 )

    def __eq__(self, other):
        if isinstance(other, vec2):
            if self.x != other.x:
                return False
            if self.y != other.y:
                return False
            return True

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y

    @property
    def lengthSquared(self):
        return self.x * self.x + self.y * self.y

    @property
    def length(self):
        return math.sqrt(self.lengthSquared)

    @property
    def normalized(self):
        length = self.length
        if length != 0:
            return vec2(self.x / length, self.y / length)
        return self

    @property
    def tuple(self):
        return (self.x, self.y)
