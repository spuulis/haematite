import time


class FrameRate():
    def __init__(self, weight=.5, target_dt=0.):
        self.dt = 0
        self.weight = weight
        self.target_dt = target_dt
        self.last_time = None

    def add_dt(self, dt):
        self.dt = (self.dt + self.weight * dt) / (1 + self.weight)

    def add_time(self, time_now):
        if self.last_time is not None:
            self.add_dt(time_now - self.last_time)
        self.last_time = time_now

    def throttle(self, start_time):
        time.sleep(self.calculate_throttle(start_time))

    def calculate_throttle(self, start_time):
        return max(0, self.target_dt - (time.time_ns() * 1.e-9 - start_time))

    def set_target_dt(self, dt):
        self.target_dt = dt

    def set_target_fps(self, fps):
        self.target_dt = 1. / fps

    @property
    def fps(self):
        if self.dt == 0:
            return 0.
        return 1. / self.dt
