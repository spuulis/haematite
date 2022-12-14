import cv2
import numpy as np


# Calibration board parameters
CHESSBOARD_DIM = (6, 5)     # Number of corners (width, height)
CHESSBOARD_SIZE = 10e-3     # Side length of one square in meters (SI)


# Camera paramters
CAMERA_EXPOSURE_TIME = 10000


# Image parameters
IMAGE_FPS = 10
IMAGE_SCALE = 0.2


# Model paramters
MODEL_FPS = 100


# Coil parameters
COILS_MAX_CURRENT = 5.
COILS_SAMPLE_RATE = 10000

COILS_NAME_OX = 'Dev1/ao1'
COILS_NAME_OY = 'Dev1/ao0'

COILS_T_TO_V_X = 630.3
COILS_T_TO_V_Y = 656.1


# Marker parameters
MARKER_SIZE = 5.08e-3       # Side length of marker in meters (SI)
MARKER_IS_INVERTED = True   # Is the marker black on white
MARKER_DICT = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
MARKER_1X1_SIZE = 5.08e-3
MARKER_2X2_SIZE = 2.032e-3
MARKER_2X2_PADDING = 1.016e-3

MARKER_DETECTION_PARAMS = cv2.aruco.DetectorParameters_create()
MARKER_DETECTION_PARAMS.detectInvertedMarker = True
# Thresholding
MARKER_DETECTION_PARAMS.adaptiveThreshWinSizeMin = 205
MARKER_DETECTION_PARAMS.adaptiveThreshWinSizeMax = 305
MARKER_DETECTION_PARAMS.adaptiveThreshWinSizeStep = 50
# Contour filtering
MARKER_DETECTION_PARAMS.minMarkerPerimeterRate = 0.01
MARKER_DETECTION_PARAMS.maxMarkerPerimeterRate = 0.8
MARKER_DETECTION_PARAMS.polygonalApproxAccuracyRate = 0.08
MARKER_DETECTION_PARAMS.minCornerDistanceRate = 0.01
MARKER_DETECTION_PARAMS.minMarkerDistanceRate = 0.01
# Corner refinement
MARKER_DETECTION_PARAMS.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
MARKER_DETECTION_PARAMS.cornerRefinementWinSize = 5
MARKER_DETECTION_PARAMS.cornerRefinementMaxIterations = 30
MARKER_DETECTION_PARAMS.cornerRefinementMinAccuracy = 0.001


# Cube parameters
CUBE_SIZE = 9.9e-3
CUBE_MARKER_POSITIONS = [
    [   # Marker 0
        [MARKER_SIZE / 2, MARKER_SIZE / 2, -CUBE_SIZE / 2],
        [-MARKER_SIZE / 2, MARKER_SIZE / 2, -CUBE_SIZE / 2],
        [-MARKER_SIZE / 2, -MARKER_SIZE / 2, -CUBE_SIZE / 2],
        [MARKER_SIZE / 2, -MARKER_SIZE / 2, -CUBE_SIZE / 2],
    ],
    [   # Marker 1
        [-MARKER_SIZE / 2, -CUBE_SIZE / 2, MARKER_SIZE / 2],
        [MARKER_SIZE / 2, -CUBE_SIZE / 2, MARKER_SIZE / 2],
        [MARKER_SIZE / 2, -CUBE_SIZE / 2, -MARKER_SIZE / 2],
        [-MARKER_SIZE / 2, -CUBE_SIZE / 2, -MARKER_SIZE / 2],
    ],
    [   # Marker 2
        [-CUBE_SIZE / 2, MARKER_SIZE / 2, -MARKER_SIZE / 2],
        [-CUBE_SIZE / 2, MARKER_SIZE / 2, MARKER_SIZE / 2],
        [-CUBE_SIZE / 2, -MARKER_SIZE / 2, MARKER_SIZE / 2],
        [-CUBE_SIZE / 2, -MARKER_SIZE / 2, -MARKER_SIZE / 2],
    ],
    [   # Marker 3
        [CUBE_SIZE / 2, MARKER_SIZE / 2, MARKER_SIZE / 2],
        [CUBE_SIZE / 2, MARKER_SIZE / 2, -MARKER_SIZE / 2],
        [CUBE_SIZE / 2, -MARKER_SIZE / 2, -MARKER_SIZE / 2],
        [CUBE_SIZE / 2, -MARKER_SIZE / 2, MARKER_SIZE / 2],
    ],
    [   # Marker 4
        [-MARKER_SIZE / 2, CUBE_SIZE / 2, -MARKER_SIZE / 2],
        [MARKER_SIZE / 2, CUBE_SIZE / 2, -MARKER_SIZE / 2],
        [MARKER_SIZE / 2, CUBE_SIZE / 2, MARKER_SIZE / 2],
        [-MARKER_SIZE / 2, CUBE_SIZE / 2, MARKER_SIZE / 2],
    ],
    [   # Marker 5
        [-MARKER_SIZE / 2, MARKER_SIZE / 2, CUBE_SIZE / 2],
        [MARKER_SIZE / 2, MARKER_SIZE / 2, CUBE_SIZE / 2],
        [MARKER_SIZE / 2, -MARKER_SIZE / 2, CUBE_SIZE / 2],
        [-MARKER_SIZE / 2, -MARKER_SIZE / 2, CUBE_SIZE / 2],
    ],
]

CUBE_FACES = [
    {   # Face 0
        'origin': np.array([
            MARKER_SIZE / 2, MARKER_SIZE / 2, -CUBE_SIZE / 2,
        ]),
        'x': np.array([
            0., -1., 0.,
        ]),
        'y': np.array([
            -1., 0., 0.,
        ]),
    },
    {   # Face 1
        'origin': np.array([
            -MARKER_SIZE / 2, -CUBE_SIZE / 2, MARKER_SIZE / 2,
        ]),
        'x': np.array([
            0., 0., -1.,
        ]),
        'y': np.array([
            1., 0., 0.,
        ]),
    },
    {   # Face 2
        'origin': np.array([
            -CUBE_SIZE / 2, MARKER_SIZE / 2, -MARKER_SIZE / 2,
        ]),
        'x': np.array([
            0., -1., 0.,
        ]),
        'y': np.array([
            0., 0., 1.,
        ]),
    },
    {   # Face 3
        'origin': np.array([
            CUBE_SIZE / 2, MARKER_SIZE / 2, MARKER_SIZE / 2,
        ]),
        'x': np.array([
            0., -1., 0.,
        ]),
        'y': np.array([
            0., 0., -1.,
        ]),
    },
    {   # Face 4
        'origin': np.array([
            -MARKER_SIZE / 2, CUBE_SIZE / 2, -MARKER_SIZE / 2,
        ]),
        'x': np.array([
            0., 0., 1.,
        ]),
        'y': np.array([
            1., 0., 0.,
        ]),
    },
    {   # Face 5
        'origin': np.array([
            -MARKER_SIZE / 2, MARKER_SIZE / 2, CUBE_SIZE / 2,
        ]),
        'x': np.array([
            0., -1., 0.,
        ]),
        'y': np.array([
            1., 0., 0.,
        ]),
    },
]


# Data parameters
DATA_PATH = './data/'
CALIBRATION_PATH = DATA_PATH + 'calibration/'
EXPERIMENT_PATH = DATA_PATH + 'experiments/'


# Coil profile parameters
PROFILE_LENGTH = 3.
PROFILE_RESOLUTION = 0.006
PROFILE_AMPLITUDE = 6.
