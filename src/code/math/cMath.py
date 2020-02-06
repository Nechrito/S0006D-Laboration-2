class cMath:
    def colorLerp(self, a, b, c, t):
        if t < 0.5:
            return self.lerp(a, b, t / 0.5)
        else:
            return self.lerp(b, c, (t - 0.5) / 0.5)

    @staticmethod
    def lerp(start, end, t):
        return start * (1 - t) + end * t
