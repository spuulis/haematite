import threading
import time

import numpy as np

import config
from visual import markers


class Controller(threading.Thread):
    def __init__(self, camera, coils):
        threading.Thread.__init__(self)
        self.daemon = True
        self._stopper = threading.Event()

        self.camera = camera
        self.coils = coils

        self._field = None
        self._img = np.ones((1, 1, 3), np.uint8)
        self._measurement = None

    def stop(self):
        self._stopper.set()

    @property
    def field(self):
        return self._field.copy()

    @property
    def img(self):
        return self._img.copy()

    @property
    def measurement(self):
        return self._measurement.copy()

    def tick(self):
        time_now = time.time_ns()
        self._field = self.coils.field
        self._img = self.camera.grab()
        ms = markers.find_markers(
            self._img, config.MARKER_DICT, config.MARKER_DETECTION_PARAMS)
        cubes = markers.pose_cubes(
            self.camera.mtx, self.camera.dist,
            ms, config.CUBE_MARKER_POSITIONS,
        )
        self._measurement = [
            dict(cube, **{
                'time': time_now,
                'coil_x': self._field['x'],
                'coil_y': self._field['y'],
            }) for cube in cubes
        ]

    def run(self):
        while not self._stopper.is_set():
            self.tick()
