import json

import cv2

from visual.calibration import Chessboard
from visual.camera import Camera

calibrator = Chessboard(1, (10, 7))
ret, mtx, dist, rvecs, tvecs = None, None, None, None, None

cam = Camera()
cam.initialize(10000)
cam.start_capture()

calib = {}
while True:
    img = cam.grab()
    img_s = img.copy()
    ret, corners = calibrator.find_corners(img)
    if ret is True:
        calibrator.draw_corners(img_s, corners)
    cv2.imshow("Webcam", img_s)  # This will open an independent window
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('a'):
        calibrator.add_image(img)
        print(len(calibrator.imgpoints))
    if key == ord('c'):
        ret, mtx, dist, rvecs, tvecs = calibrator.calibrate()
        calib = {
            'ret': ret,
            'mtx': mtx.tolist(),
            'dist': dist.tolist(),
        }
        print(ret)

cv2.destroyAllWindows()
cv2.waitKey(1)

with open('calibration.json', 'w') as json_file:
    json.dump(calib, json_file)

cam.stop_capture()
