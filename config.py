import cv2

# Calibration board parameters
CHESSBOARD_DIM = (6, 5)     # Number of corners (width, height)
CHESSBOARD_SIZE = 10e-3     # Side length of one square in meters (SI)

# Marker parameters
MARKER_SIZE = 5.08e-3       # Side length of marker in meters (SI)
MARKER_IS_INVERTED = True   # Is the marker black on white
MARKER_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)