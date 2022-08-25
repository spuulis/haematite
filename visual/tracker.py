from queue import Queue
import time

import config
from . import markers as markers


class Tracker():
    def __init__(self, camera):
        self.camera = camera
        self.feed = Queue(1)
        self.measurements = Queue(0)

    def tick(self):
        img = self.camera.grab()
        time_now = time.time_ns()
        ms = markers.find_markers(
            img, config.MARKER_DICT, config.MARKER_DETECTION_PARAMS)
        cubes = markers.pose_cubes(
            self.camera.mtx, self.camera.dist,
            ms, config.CUBE_MARKER_POSITIONS,
        )
        measurement = [dict(cube, **{'time': time_now}) for cube in cubes]
        return measurement, img