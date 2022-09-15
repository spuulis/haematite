import cv2
import numpy as np
from scipy.spatial.transform import Rotation

import config


class CubeMarkers1x1():
    def __init__(self) -> None:
        self.markers = self.generate_positions()

    def get_cube(self, id: int) -> int:
        return id // 6

    def get_position(self, id: int) -> list:
        return self.markers[id % 6]

    def generate_positions(self) -> list:
        markers = []
        for face in config.CUBE_FACES:
            markers.append([
                face['origin'],
                face['origin'] + face['y'] * config.MARKER_1X1_SIZE,
                (
                    face['origin']
                    + face['y'] * config.MARKER_1X1_SIZE
                    + face['x'] * config.MARKER_1X1_SIZE
                ),
                face['origin'] + face['x'] * config.MARKER_1X1_SIZE,
            ])
        return markers


class CubeMarkers2x2():
    def __init__(self) -> None:
        self.markers = self.generate_positions()

    def get_cube(self, id: int) -> int:
        return id // 24

    def get_position(self, id: int) -> list:
        return self.markers[id % 24]

    def generate_positions(self) -> list:
        markers = []
        for face in config.CUBE_FACES:
            marker_positions = [
                face['origin'],
                (
                    face['origin']
                    + face['x']
                    * (config.MARKER_2X2_SIZE + config.MARKER_2X2_PADDING)
                ),
                (
                    face['origin']
                    + face['y']
                    * (config.MARKER_2X2_SIZE + config.MARKER_2X2_PADDING)
                ),
                (
                    face['origin']
                    + face['x']
                    * (config.MARKER_2X2_SIZE + config.MARKER_2X2_PADDING)
                    + face['x']
                    * (config.MARKER_2X2_SIZE + config.MARKER_2X2_PADDING)
                ),
            ]
            for marker_position in marker_positions:
                markers.append([
                    marker_position,
                    marker_position + face['y'] * config.MARKER_2X2_SIZE,
                    (
                        marker_position
                        + face['y'] * config.MARKER_2X2_SIZE
                        + face['x'] * config.MARKER_2X2_SIZE
                    ),
                    marker_position + face['x'] * config.MARKER_2X2_SIZE,
                ])
        return markers


def find_markers(img, aruco_dict, aruco_params):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (corners, ids, _) = cv2.aruco.detectMarkers(
        gray, aruco_dict, parameters=aruco_params)
    if corners is None or ids is None:
        return []
    return [
        {'id': id_[0], 'corners': corners_[0]}
        for id_, corners_ in zip(ids, corners)
    ]


def draw_marker(img: np.ndarray, scale: float, corners: np.ndarray) -> None:
    cv2.aruco.drawDetectedMarkers(img, corners * scale)


def pose_markers(
        mtx, dist, markers, marker_size, all_solutions=False):
    poses = []
    shape = np.array([
        [-.5, .5, 0.], [.5, .5, 0.],
        [.5, -.5, 0.], [-.5, -.5, 0.],
    ]) * marker_size

    for marker in markers:
        # Estimate the pose of markers
        n_sol, rvecs, tvecs, err = cv2.solvePnPGeneric(
            shape, marker['corners'], mtx, dist,
            flags=cv2.SOLVEPNP_IPPE_SQUARE,
        )

        if not all_solutions:
            n_sol = 1
        # Go through all (both) returned solutions
        for j in range(n_sol):
            # Save data
            poses.append({
                'id': marker['id'],
                'tvec': tvecs[j].reshape(3),
                'rvec': rvecs[j].reshape(3),
                'rep_err': err[j][0],
            })

    return poses


def pose_cubes_new(mtx, dist, markers, marker_positions):
    poses = []
    cube_ids = np.unique([
        marker_positions.get_cube(marker['id']) for marker in markers
    ])
    for cube_id in cube_ids:
        cube_markers = [
            marker for marker in markers
            if marker_positions.get_cube(marker['id']) == cube_id
        ]

        objpoints = np.array([])
        imgpoints = np.array([])
        for marker in cube_markers:
            objpoints = np.vstack([
                objpoints,
                marker_positions.get_position(marker['id']),
            ]) if objpoints.size else np.array(
                marker_positions.get_position(marker['id']))
            imgpoints = np.vstack([
                imgpoints,
                marker['corners'],
            ]) if imgpoints.size else np.array(marker['corners'])

        # Estimate and save pose
        _, rvec, tvec = cv2.solvePnP(
            objpoints, imgpoints,
            mtx, dist,  # flags=cv2.SOLVEPNP_ITERATIVE,
        )
        poses.append({
            'cube_id': cube_id,
            'rvec': rvec.reshape(3),
            'tvec': tvec.reshape(3),
        })
    return poses


def pose_cubes(mtx, dist, markers, marker_positions):
    poses = []
    # Find which cubes have at least one marker visible
    cube_ids = np.unique([marker['id'] // 6 for marker in markers])
    for cube_id in cube_ids:
        # Find markers belonging to the cube
        cube_markers = [
            marker for marker in markers if marker['id'] // 6 == cube_id
        ]

        # Match points on the cube and the image
        objpoints = np.array([])
        imgpoints = np.array([])
        for marker in cube_markers:
            objpoints = np.vstack([
                objpoints,
                marker_positions[marker['id'] % 6],
            ]) if objpoints.size else np.array(
                marker_positions[marker['id'] % 6])
            imgpoints = np.vstack([
                imgpoints,
                marker['corners'],
            ]) if imgpoints.size else np.array(marker['corners'])

        # Estimate and save pose
        _, rvec, tvec = cv2.solvePnP(
            objpoints, imgpoints,
            mtx, dist,  # flags=cv2.SOLVEPNP_ITERATIVE,
        )
        print(np.linalg.norm(tvec))
        poses.append({
            'cube_id': cube_id,
            'rvec': rvec.reshape(3),
            'tvec': tvec.reshape(3),
        })

    return poses


def camera_to_aboslute_ref_frame(tvec, rvec, repos, euler="zyx"):
    a_tvec = tvec
    a_reul = rvec_to_reul(rvec, euler)
    return a_tvec, a_reul


def rvec_to_reul(rvec, euler="zyx"):
    r_matrix = cv2.Rodrigues(rvec.reshape(3))[0]
    r = Rotation.from_matrix(r_matrix)
    return r.as_euler(euler, degrees=True)


def draw_marker_axis(mtx, dist, img, markers, axis_length):
    for marker in markers:
        cv2.drawFrameAxes(
            img, mtx, dist,
            np.array(
                [marker['rvecs_x'], marker['rvecs_y'], marker['rvecs_z']]),
            np.array(
                [marker['tvecs_x'], marker['tvecs_y'], marker['tvecs_z']]),
            axis_length
        )


def draw_cubes(mtx, dist, img, scale, cubes, cube_size):
    vertices = np.float32([
        [-.5, -.5, .5], [-.5, .5, .5], [.5, .5, .5], [.5, -.5, .5],
        [-.5, -.5, -.5], [-.5, .5, -.5], [.5, .5, -.5], [.5, -.5, -.5],
    ]) * cube_size

    for cube in cubes:
        imgpts, _ = cv2.projectPoints(
            vertices, cube['rvec'], cube['tvec'], mtx, dist)
        imgpts = np.int32(imgpts * scale).reshape(-1, 2)
        # Draw the cube
        thickness = int(10 * scale)
        img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), thickness)
        for i, j in zip(range(4), range(4, 8)):
            img = cv2.line(
                img, tuple(imgpts[i]), tuple(imgpts[j]),
                (0, 0, 255), thickness)
        img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 0, 255), thickness)


def draw_marker_cube(mtx, dist, img, markers, marker_size):
    axis = np.float32([
        [-.5, -.5, 0], [-.5, .5, 0], [.5, .5, 0], [.5, -.5, 0],
        [-.5, -.5, -1], [-.5, .5, -1], [.5, .5, -1], [.5, -.5, -1],
    ]) * marker_size

    for marker in markers:
        # Project 3D points to image plane
        imgpts, _ = cv2.projectPoints(
            axis, marker['rvecs'], marker['tvecs'], mtx, dist)
        imgpts = np.int32(imgpts).reshape(-1, 2)
        # Draw the cube
        img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 0, 100), 3)
        for i, j in zip(range(4), range(4, 8)):
            img = cv2.line(
                img, tuple(imgpts[i]), tuple(imgpts[j]),
                (0, 0, 200), 5)
        img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 0, 255), 7)
