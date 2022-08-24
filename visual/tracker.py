import cv2
import numpy as np
from scipy.spatial.transform import Rotation

aruco_params = cv2.aruco.DetectorParameters_create()
# Thresholding
aruco_params.adaptiveThreshWinSizeMin = 35
aruco_params.adaptiveThreshWinSizeMax = 85
aruco_params.adaptiveThreshWinSizeStep = 10
# Contour filtering
aruco_params.minMarkerPerimeterRate = 0.08
aruco_params.maxMarkerPerimeterRate = 0.32
aruco_params.polygonalApproxAccuracyRate = 0.05
aruco_params.minCornerDistanceRate = 0.05
aruco_params.minMarkerDistanceRate = 0.05
# Corner refinement
aruco_params.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
aruco_params.cornerRefinementWinSize = 5
aruco_params.cornerRefinementMaxIterations = 30
aruco_params.cornerRefinementMinAccuracy = 0.001


def find_markers(img, aruco_dict, inverted=False):
    aruco_params.detectInvertedMarker = inverted
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)


def pose_markers(
        mtx, dist, corners, ids, marker_size,
        euler='zyx', all_solutions=False):
    markers = []
    shape = np.array([
        [-.5, .5, 0.], [.5, .5, 0.],
        [.5, -.5, 0.], [-.5, -.5, 0.],
    ]) * marker_size

    for i in range(len(corners)):
        # Estimate the pose of markers
        n_sol, rvecs, tvecs, err = cv2.solvePnPGeneric(
            shape, corners[i], mtx, dist,
            flags=cv2.SOLVEPNP_IPPE_SQUARE,
        )

        if not all_solutions:
            n_sol = 1

        # Go through all (both) returned solutions
        for j in range(n_sol):
            # Format rotation angles as Euler angles
            r_matrix = cv2.Rodrigues(rvecs[j].reshape(3))[0]
            r = Rotation.from_matrix(r_matrix)
            [rx, ry, rz] = r.as_euler(euler, degrees=True)

            # Save data
            markers.append({
                'id': ids[i][0],
                'tvecs_x': tvecs[j].reshape(3)[0],
                'tvecs_y': tvecs[j].reshape(3)[1],
                'tvecs_z': tvecs[j].reshape(3)[2],
                'rvecs_x': rvecs[j].reshape(3)[0],
                'rvecs_y': rvecs[j].reshape(3)[1],
                'rvecs_z': rvecs[j].reshape(3)[2],
                'reulr_x': rx,
                'reulr_y': ry,
                'reulr_z': rz,
                'rep_err': err[j][0],
            })

    return markers


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
