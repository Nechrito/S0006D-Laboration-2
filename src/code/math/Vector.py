import numbers
import math


class vec2:
    def __init__(self, X=0, Y=0):
        self.X = X
        self.Y = Y

    def __getitem__(self, item):
        if item == 0:
            return self.X
        if item == 1:
            return self.Y

    def __getattr__(self, name):
        return self[name]

    def __add__(self, other: 'vec2'):
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
            return vec2(self.X / other.X, self.Y / other.Y)
        if isinstance(other, float):
            return vec2(self.X / other, self.Y / other)
        if isinstance(other, numbers.Number):
            return vec2(self.X / other, self.Y / other)

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
        return math.sqrt((self.X - other.X) ** 2 + (self.Y - other.Y) ** 2)

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
