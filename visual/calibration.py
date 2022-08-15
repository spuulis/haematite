import cv2
import numpy as np
from tqdm import tqdm

def chessboard(images, size, dim, verbose=False):
    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((dim[0] * dim[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:dim[0], 0:dim[1]].T.reshape(-1,2)

    # Resize objp to match given units
    objp = objp * size

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    for i in tqdm(range(len(images)), disable=not verbose):
        img = cv2.imread(images[i])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (6, 5), None)

        # If found, add object points, image points
        if ret == True:
            # TODO: Refine image points with cornerSubPix?
            objpoints.append(objp)
            imgpoints.append(corners)
    
    img = cv2.imread(images[0])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


def focus_measure(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()