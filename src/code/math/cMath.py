from src.code.engine.GameTime import GameTime
from src.code.math.vec2 import vec2


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def mapped(start: float, inMin: float, inMax: float, outMin: float, outMax: float):
    return (start - inMin) * (outMax - outMin) / (inMax - inMin) + outMin


def tween(a, b, t):
    if a != b:
        if abs(b - a) > 1.0:
            a = lerp(a, b, t * GameTime.deltaTime)
        else:
            a = b
    return a


def getLerpValue(start, end, ratio):
    rl = abs(start - end)
    return rl / max(0.1, ratio)


def lerp(start, end, t):
    return start * (1 - t) + end * t


def lerpColor(c1, c2, t):
    return (lerp(c1[0], c2[0], t),
            lerp(c1[1], c2[1], t),
            lerp(c1[2], c2[2], t))
