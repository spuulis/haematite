import cv2
import numpy as np
from tqdm import tqdm

def focus_measure(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()


class Chessboard():
    def __init__(self, edge_size, dimensions):
        # Dimensions of the chessboard
        self.dimensions = dimensions

        # Image resolution
        self.resolution = None

        # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((dimensions[0] * dimensions[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:dimensions[0], 0:dimensions[1]].T.reshape(-1,2)

        # Resize objp to match given units
        self.objp = self.objp * edge_size

        # Arrays to store object points and image points from all the images.
        self.objpoints = []  # 3d point in real world space
        self.imgpoints = []  # 2d points in image plane.

    def add_image(self, img):
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Check and save image resolution
        if self.resolution == None:
            self.resolution = gray.shape[::-1]
        if self.resolution != gray.shape[::-1]:
            return False, []
        
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, self.dimensions, None)

        # If found, add object points, image points
        if ret == True:
            # TODO: Refine image points with cornerSubPix?
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners)
        return ret, corners
        
    def add_images(self, images, verbose=False):
        ret = False
        for i in tqdm(range(len(images)), disable=not verbose):
            img = cv2.imread(images[i])
            ret = self.add_image(img)[0] or ret
        return ret

    def calibrate(self):
        return cv2.calibrateCamera(
            self.objpoints,
            self.imgpoints,
            self.resolution,
            None,
            None
        )
    
    def draw_corners(self, img, corners, inplace=True):
        if inplace:
            cv2.drawChessboardCorners(img, (6, 5), corners, True)
        else:
            temp = img.copy()
            cv2.drawChessboardCorners(temp, (6, 5), corners, True)
            return temp
        return True