import threading
import time

import cv2
import numpy as np
import pandas as pd

import config
from utils import FrameRate
from visual import markers


class Model(threading.Thread):
    def __init__(self, camera, coils):
        threading.Thread.__init__(self)
        self.daemon = True
        self._stopper = threading.Event()

        self.frame_rate = FrameRate()
        self.frame_rate.set_target_fps(100)

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
            'tvec_x',
            'tvec_y',
            'tvec_z',
            'reul_x',
            'reul_y',
            'reul_z',
        ])

    def start_recording(self):
        self.clear_data()
        self.recording = True

    def stop_recording(self, filename):
        # TODO: Remake this part thread-safe (right now it is questionable)
        self.recording = False
        self.data.to_csv(
            filename,
            index=False,
            sep='\t',
        )
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
        measurement = []
        if self.camera.mtx is not None and self.camera.dist is not None:
            ms = markers.find_markers(
                self._img, config.MARKER_DICT, config.MARKER_DETECTION_PARAMS)
            cubes = markers.pose_cubes(
                self.camera.mtx, self.camera.dist,
                ms, config.CUBE_MARKER_POSITIONS,
            )
            measurement = [
                dict(cube, **{
                    'time': time_now * 1.e-9,
                    'coil_x': self._field['x'],
                    'coil_y': self._field['y'],
                }) for cube in cubes
            ]
            cv2.aruco.drawDetectedMarkers(
                img,
                [
                    np.array([list(marker['corners'])])
                    for marker in ms
                ]
            )
        return img, measurement

    def append_data(self, measurement):
        for cube in measurement:
            tvec, reul = markers.camera_to_aboslute_ref_frame(
                cube['tvec'],
                cube['rvec'],
                [],
            )
            self.data = pd.concat([
                self.data,
                pd.DataFrame([{
                    'time': cube['time'],
                    'coil_x': cube['coil_x'],
                    'coil_y': cube['coil_y'],
                    'cube_id': cube['cube_id'],
                    'tvec_x': tvec[0],
                    'tvec_y': tvec[1],
                    'tvec_z': tvec[2],
                    'reul_x': reul[0],
                    'reul_y': reul[1],
                    'reul_z': reul[2],
                }]),
            ], ignore_index=True)

    def tick(self):
        time_now = time.time_ns()

        self._field = self.coils.field
        self._img, self._measurement = self.read_camera(time_now)

        """
        TODO: Remake the following part thread-safe (right now it is
        questionable)
        """
        if self.recording:
            self.append_data(self._measurement)

        self.frame_rate.throttle()

    def run(self):
        while not self._stopper.is_set():
            self.tick()
