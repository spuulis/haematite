import cv2
import numpy as np
from scipy.spatial.transform import Rotation


def find_markers(img, aruco_dict, aruco_params):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (corners, ids, _) = cv2.aruco.detectMarkers(
        gray, aruco_dict, parameters=aruco_params)
    return [
        {'id': id_[0], 'corners': corners_}
        for id_, corners_ in zip(ids, corners)
    ]


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


def pose_cubes(mtx, dist, markers, marker_positions):
    poses = []
    # Find which cubes have at least one marker visible
    cube_ids = np.unique([marker['id'] // 6 for marker in markers])
    for cube_id in cube_ids:
        # Find markers belonging to the cube
        cube_markers = [
            marker for marker in markers if marker['id'] // 6 is cube_id
        ]

        # Match points on the cube and the image
        objpoints = []
        imgpoints = []
        for marker in cube_markers:
            objpoints = np.concatenate((
                objpoints,
                marker_positions[marker['id'] % 6],
            ))
            imgpoints = np.concatenate((
                imgpoints,
                marker['corners'],
            ))
        
        # Estimate and save pose
        rvec, tvec = cv2.solvePnP(
            objpoints, imgpoints, mtx, dist, flags=cv2.SOLVEPNP_EPNP
        )
        poses.append({
            'id': cube_id,
            'rvec': rvec,
            'tvec': tvec,
        })

    return poses


def camera_to_aboslute_ref_frame(tvec, rvec, repos, euler="zyx"):
    pass


def rvec_to_relr(rvec, euler="zyx"):
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
