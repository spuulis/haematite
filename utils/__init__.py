import time


class FrameRate():
    def __init__(self, weight=2., target_dt=0.):
        self.dt = 0
        self.fps_dt = 0
        self.usage_dt = 0
        self.weight = weight
        self.target_dt = None
        self.set_target_dt(target_dt)

        self.last_time = None
        self.start_time = None

    def add_time(self):
        time_now = time.time_ns() * 1.e-9
        if self.start_time is not None:
            self.dt = time_now - self.start_time
            self.usage_dt = (
                (time_now - self.start_time + self.weight * self.usage_dt)
                / (1 + self.weight)
            )
        if self.last_time is not None:
            self.fps_dt = (
                (time_now - self.last_time + self.weight * self.fps_dt)
                / (1 + self.weight)
            )
        self.last_time = time_now

    def throttle(self):
        time.sleep(self.calculate_throttle())
        self.begin()

    def begin(self):
        self.start_time = time.time_ns() * 1.e-9

    def calculate_throttle(self):
        self.add_time()
        sleep = max(0., self.target_dt - self.dt)
        # print((
        #     f'{self.dt} '
        #     f'{self.target_dt} '
        #     f'{sleep} '
        #     f'{self.fps_dt} '
        # ))
        return sleep

    def set_target_dt(self, dt):
        self.target_dt = dt
        self.dt = self.target_dt
        self.fps_dt = self.target_dt

    def set_target_fps(self, fps):
        self.set_target_dt(1. / fps)

    @property
    def fps(self):
        if self.fps_dt == 0:
            return 0.
        return 1. / self.fps_dt

    @property
    def usage(self):
        return self.usage_dt / self.target_dt


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
