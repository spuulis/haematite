import threading
import time

import numpy as np
import pandas as pd

import config
from visual import markers


class Controller(threading.Thread):
    def __init__(self, camera, coils):
        threading.Thread.__init__(self)
        self.daemon = True
        self._stopper = threading.Event()

        self.frame_rate = FrameRate()
        self.time_last = None

        self.camera = camera
        self.coils = coils

        self._field = None
        self._img = np.ones((1, 1, 3), np.uint8)
        self._measurement = None

        self.recording = False
        self.data = None
        self.clear_data()

    def stop(self):
        self._stopper.set()

    def clear_data(self):
        self.data = pd.DataFrame(columns=[
            'time',
            'coil_x',
            'coil_y',
            'cube_id',
            'tvec',
            'reul',
        ])

    def start_recording(self):
        self.clear_data()
        self.recodring = True

    def stop_recording(self, filename):
        # TODO: Remake this part thread-safe (right now it is questionable)
        self.recording = False
        self.data.to_csv(filename)
        self.clear_data()

    @property
    def field(self):
        return self._field.copy()

    @property
    def img(self):
        return self._img.copy()

    @property
    def measurement(self):
        return self._measurement.copy()

    def read_camera(self, time_now):
        img = self.camera.grab()
        ms = markers.find_markers(
            self._img, config.MARKER_DICT, config.MARKER_DETECTION_PARAMS)
        cubes = markers.pose_cubes(
            self.camera.mtx, self.camera.dist,
            ms, config.CUBE_MARKER_POSITIONS,
        )
        measurement = [
            dict(cube, **{
                'time': time_now,
                'coil_x': self._field['x'],
                'coil_y': self._field['y'],
            }) for cube in cubes
        ]
        return img, measurement

    def append_data(self, measurement):
        tvec, reul = markers.camera_to_aboslute_ref_frame(
            measurement['tvec'],
            measurement['rvec'],
            [],
        )
        self.data.append({
            'time': measurement['time'],
            'coil_x': measurement['coil_x'],
            'coil_y': measurement['coil_y'],
            'cube_id': measurement['cube_id'],
            'tvec': tvec,
            'reul': reul,
        }, ignore_index=True)

    def tick(self):
        time_now = time.time_ns()
        self.frame_rate.add_dt((time_now - self.time_last) * 1.e-9)
        self.time_last = time_now

        self._field = self.coils.field
        self._img, self._measurement = self.read_camera(time_now)

        """
        TODO: Remake the following part thread-safe (right now it is
        questionable)
        """
        if self.recording:
            self.append_data(self._measurement)

    def run(self):
        self.time_last = time.time_ns()
        while not self._stopper.is_set():
            self.tick()


class FrameRate():
    def __init__(self, weight=.5):
        self.dt = 0
        self.weight = weight

    def add_dt(self, dt):
        self.dt = (self.dt + self.weight * dt) / (1 + self.weight)

    @property
    def fps(self):
        return 1. / self.dt
