import numpy as np


class Experiment():
    def __init__(self) -> None:
        self.recording = False

    def start_recording(self) -> None:
        self.recording = True

    def stop_recording(self, experiment_id: str) -> None:
        self.recording = False
        self.save_data(experiment_id)

    def save_data(self, experiment_id: str) -> None:
        pass

    def load_data(self, experiment_id: str) -> None:
        pass

    def measure(
        self, time_now: float, field: dict, image: np.ndarray,
        camera_mtx: np.ndarray, camera_dist: np.ndarray,
    ) -> None:
        pass

    def draw(
        self, time_now: float, field: dict, image: np.ndarray,
        camera_mtx: np.ndarray, camera_dist: np.ndarray, scale: float = 1.,
    ) -> np.ndarray:
        return image
