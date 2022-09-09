import time


class FrameRate():
    def __init__(self):
        self.throttle_time = None
        self.dt = None
        self.last_time = None

    def add_time(self, time_now):
        if self.last_time is not None:
            self.dt = time_now - self.last_time
        self.last_time = time_now

    def throttle(self):
        self.add_time(time.time_ns() * 1.e-9)
        time.sleep(self.throttle_time)

    def imitate_throttle(self):
        self.add_time(time.time_ns() * 1.e-9)
        return self.throttle_time

    def set_target_fps(self, fps):
        self.throttle_time = 1. / fps

    @property
    def fps(self):
        if self.dt is None or self.dt == 0:
            return 0.
        return 1. / self.dt

    @property
    def usage(self):
        if self.dt is None:
            return 1.
        return 1. - self.throttle_time / self.dt


class GridCounter():
    def __init__(self) -> None:
        self.row = -1
        self.column = -1

    def get_row(self) -> int:
        return self.row

    def get_column(self) -> int:
        return self.column

    def next_row(self) -> int:
        self.column = -1
        self.row += 1
        return self.row

    def next_column(self) -> int:
        self.column += 1
        return self.column
