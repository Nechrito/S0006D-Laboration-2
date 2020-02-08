
def truncate(n):
    return int(n * 1000) / 1000


def clamp(minimum, maximum, x):
    return max(minimum, min(x, maximum))


def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


def lerp(start, end, t):
    return start * (1 - t) + end * t


def lerpColor(c1, c2, t):
    return (lerp(c1[0], c2[0], t),
            lerp(c1[1], c2[1], t),
            lerp(c1[2], c2[2], t))
