import numpy as np
import pandas as pd

from . import Experiment
import config
import visual.markers as markers


class CubeExperiment(Experiment):
    def __init__(self) -> None:
        super().__init__()
        self.measurement = []

        self.data = pd.DataFrame()
        self.clear_data()

    def measure(
        self, time_now: float, field: dict, image: np.ndarray,
        camera_mtx: np.ndarray, camera_dist: np.ndarray,
    ) -> None:
        if camera_mtx is not None and camera_dist is not None:
            ms = markers.find_markers(
                image, config.MARKER_DICT, config.MARKER_DETECTION_PARAMS)
            cubes = markers.pose_cubes(
                camera_mtx, camera_dist,
                ms, config.CUBE_MARKER_POSITIONS,
            )
            self.measurement = [
                dict(cube, **{
                    'time': time_now,
                    'coil_x': field['x'],
                    'coil_y': field['y'],
                }) for cube in cubes
            ]
            self.append_data()
        return super().measure(time_now, field, image, camera_mtx, camera_dist)

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

    def append_data(self):
        if self.recording:
            for cube in self.measurement:
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

    def start_recording(self) -> None:
        self.clear_data()
        return super().start_recording()

    def stop_recording(self, experiment_id: str) -> None:
        super().stop_recording(experiment_id)
        self.data.to_csv(
            config.EXPERIMENT_PATH + experiment_id + '/data.csv',
            index=False,
            sep='\t',
        )
        self.clear_data()

    def draw(
        self, time_now: float, field: dict, image: np.ndarray,
        camera_mtx: np.ndarray, camera_dist: np.ndarray, scale: float = 1.
    ) -> np.ndarray:
        return super().draw(
            time_now, field, image, camera_mtx, camera_dist, scale)
