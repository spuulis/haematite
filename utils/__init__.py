class FrameRate():
    def __init__(self, weight=.5):
        self.dt = 0
        self.weight = weight

    def add_dt(self, dt):
        self.dt = (self.dt + self.weight * dt) / (1 + self.weight)

    @property
    def fps(self):
        if self.dt == 0:
            return 0.
        return 1. / self.dt
