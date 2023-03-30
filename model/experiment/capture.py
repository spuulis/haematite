from datetime import datetime
import os

import cv2
import numpy as np
import pandas as pd

from . import Experiment
import config


class CaptureExperiment(Experiment):
    def __init__(self) -> None:
        super().__init__()

        self.index = 0
        self.data = pd.DataFrame(
            columns=['index', 'time', 'field_x', 'field_y'],
        )
        self.image = None
        self.field = None
        self.time_now = None
        self.experiment_id = None

    def capture(self, experiment_id: str) -> None:
        self.append_data(self.time_now, self.field)
        self.save_data(experiment_id)
        self.save_image(experiment_id, self.image, self.index)
        self.index += 1

    def measure(
        self, time_now: float, field: dict, image: np.ndarray,
        camera_mtx: np.ndarray, camera_dist: np.ndarray,
    ) -> None:
        self.time_now = time_now
        self.field = field.copy()
        self.image = image.copy()
        if self.recording:
            self.append_data(time_now, field)
            self.save_image(self.experiment_id, image, self.index)
            self.index += 1
        return super().measure(time_now, field, image, camera_mtx, camera_dist)

    def start_recording(self, experiment_id: str = None) -> None:
        self.experiment_id = experiment_id
        if experiment_id is None:
            self.experiment_id = (
                f'{datetime.now().strftime("%Y.%m.%d, %H.%M.%S")}'
                ' - capture'
            )
        return super().start_recording()

    def stop_recording(self, experiment_id: str = None) -> None:
        self.save_data(self.experiment_id)
        return super().stop_recording(self.experiment_id)

    def append_data(self, time_now: float, field: dict) -> None:
        self.data = pd.concat([
            self.data,
            pd.DataFrame([{
                'index': self.index,
                'time': time_now,
                'field_x': field['x'],
                'field_y': field['y'],
            }]),
        ], ignore_index=True)

    def save_data(self, experiment_id: str) -> None:
        os.makedirs(
            config.EXPERIMENT_PATH + experiment_id + '/', exist_ok=True)
        self.data.to_csv(
            config.EXPERIMENT_PATH + experiment_id + '/data.csv',
            index=False,
            sep='\t',
        )
        return super().save_data(experiment_id)

    def save_image(
        self, experiment_id: str, image: np.ndarray, index: int,
    ) -> None:
        os.makedirs(
            config.EXPERIMENT_PATH + experiment_id + '/images/', exist_ok=True)
        cv2.imwrite((
            config.EXPERIMENT_PATH
            + experiment_id
            + '/images/'
            + f'{str(index).zfill(6)}.jpg'
        ), image)
