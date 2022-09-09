import threading
import time

import numpy as np
import cv2

from .experiment import Experiment
from .experiment.cubes import CubeExperiment
from .experiment.calibrate import CalibrateExperiment
from coils.coils import Coils
import config
from utils import FrameRate
from visual.camera import Camera


class Model(threading.Thread):
    def __init__(self, camera: Camera, coils: Coils) -> None:
        threading.Thread.__init__(self)
        self.daemon = True
        self._stopper = threading.Event()

        self.frame_rate = FrameRate()
        self.frame_rate.set_target_fps(config.MODEL_FPS)

        self.camera = camera
        self.coils = coils

        self._field = None
        self._img = np.ones((1, 1, 3), np.uint8)

        self.experiment = Experiment()

    def stop(self):
        self._stopper.set()

    def change_experiment(self, experiment_name: str) -> None:
        match experiment_name:
            case 'Calibrate':
                self.experiment = CalibrateExperiment()
                self.experiment.initialize_chessboard(0.5, (7, 10))
            case 'Cubes':
                self.experiment = CubeExperiment()
            case _:
                raise Exception(f'''
                    Experiment "{experiment_name}" is not recognised.
                ''')

    @property
    def field(self):
        return self._field.copy()

    @property
    def img(self):
        return self._img.copy()

    def tick(self):
        # Get time, field in the coils, and image from the camera
        time_now = time.time_ns()
        # TODO: Replace the following with actual reading from coils
        self._field = {'x': 0., 'y': 0.}
        ret, image = self.camera.grab()

        if ret is True:
            # Do measurements on the image
            self.experiment.measure(
                time_now, self._field, image, self.camera.mtx,
                self.camera.dist,
            )

            # Rescale the image for drawing on canvas
            scale = config.IMAGE_SCALE
            image = cv2.resize(
                image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            # Append drawings on the image
            self.experiment.draw(
                time_now, self._field, image, self.camera.mtx,
                self.camera.dist, scale,
            )
            # Save image as the current one
            self._img = image

        # Force specified framerate
        self.frame_rate.throttle()

    def run(self):
        while not self._stopper.is_set():
            self.tick()
