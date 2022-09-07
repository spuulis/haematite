import json

import numpy as np

from . import Experiment
from visual.calibration import Chessboard


class CalibrateExperiment(Experiment):
    def __init__(self) -> None:
        super().__init__()
        self.ret = False
        self.corners = None
        self.calibrator = None
        self.image = None
        
        self.calibration_data = {}

    def measure(
        self, time_now: float, field: dict, image: np.ndarray,
        camera_mtx: np.ndarray, camera_dist: np.ndarray
    ) -> None:
        if self.calibrator is not None:
            self.ret, self.corners = self.calibrator.find_corners(image)
            if self.ret is True:
                self.image = image.copy()
        return super().measure(time_now, field, image, camera_mtx, camera_dist)

    def draw(
        self, time_now: float, field: dict, image: np.ndarray,
        camera_mtx: np.ndarray, camera_dist: np.ndarray, scale: float = 1,
    ) -> np.ndarray:
        if self.ret is True:
            self.calibrator.draw_corners(image, self.corners * scale)
        return super().draw(
            time_now, field, image, camera_mtx, camera_dist, scale)

    def initialize_chessboard(
        self, edge_size: float, dimensions: tuple[int, int],
    ) -> None:
        self.calibrator = Chessboard(edge_size, dimensions)

    def capture(self) -> int:
        if self.image is not None:
            self.calibrator.add_image(self.image)
        return len(self.calibrator.imgpoints)

    def calibrate(self) -> float:
        ret, mtx, dist, _, _ = self.calibrator.calibrate()
        self.calibration_data = {
            'ret': ret,
            'mtx': mtx.tolist(),
            'dist': dist.tolist(),
        }
        return ret

    def save_calibration(self) -> None:
        with open('./data/calibration/calibration.json') as json_file:
            json.dump(self.calibration_data, json_file)
