import time


class FrameRate():
    def __init__(self, weight=2., target_dt=0.):
        self.dt = 0
        self.weight = weight
        self.target_dt = None
        self.set_target_dt(target_dt)

        self.last_time = None
        self.sleep = 0.

    def add_dt(self, dt):
        self.dt = (dt + self.weight * self.dt) / (1 + self.weight)

    def add_time(self):
        time_now = time.time_ns() * 1.e-9
        if self.last_time is not None:
            self.add_dt(time_now - self.last_time)
        self.last_time = time_now

    def throttle(self):
        time.sleep(self.calculate_throttle())

    def calculate_throttle(self):
        self.add_time()
        self.sleep = max(0., self.sleep + self.target_dt - self.dt)
        return self.sleep

    def set_target_dt(self, dt):
        self.target_dt = dt
        self.dt = self.target_dt

    def set_target_fps(self, fps):
        self.set_target_dt(1. / fps)

    @property
    def fps(self):
        if self.dt == 0:
            return 0.
        return 1. / self.dt


class GridCounter():
    def __init__(self) -> None:
        self.row = 0
        self.column = 0

    def get_row(self) -> int:
        return self.row

    def get_column(self) -> int:
        return self.column

    def next_row(self, row_span: int = 1) -> int:
        self.column = 0
        self.row += row_span
        return self.row - row_span

    def next_column(self, column_span: int = 1) -> int:
        self.column += column_span
        return self.column - column_span