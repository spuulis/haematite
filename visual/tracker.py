import cv2
from scipy.spatial.transform import Rotation

aruco_params = cv2.aruco.DetectorParameters_create()

def find_markers(img, aruco_dict, inverted=False):
    aruco_params.detectInvertedMarker = inverted
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

def pose_markers(mtx, dist, corners, ids, marker_size, euler='zyx'):
    markers = []
    for i in range(len(corners)):
        # Estimate the pose of markers
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], marker_size, mtx, dist)
        
        # Format rotation angles as Euler angles
        r_matrix = cv2.Rodrigues(rvecs[0])[0]
        r = Rotation.from_matrix(r_matrix)
        [rx, ry, rz] = r.as_euler(euler, degrees=True)

        # Save data
        markers.append({
            'id': ids[i],
            'tvecs': tvecs[0][0],
            'rvecs': rvecs[0][0],
            'reuler': [rx, ry, rz],
        })

    return markers