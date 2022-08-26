import time

import numpy as np
from pypylon import pylon


class Camera():
    def __init__(self):
        self.exposure_time = None

        # Calibration parameters
        self.mtx = None
        self.dist = None

        self.camera = None

        # Image converter to cv2 format (bgr)
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def initialize(self, exposure_time: int):
        self.exposure_time = exposure_time
        # Connect to the first available camera
        try:
            self.camera = pylon.InstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.camera.Open()
            self.camera.ExposureTime.SetValue(self.exposure_time)
            self.camera.Close()
        except Exception:
            raise Exception("Camera is not found")

    def calibrate(self, mtx, dist):
        self.mtx = mtx
        self.dist = dist

    def start_capture(self):
        if self.camera is not None:
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stop_capture(self):
        if self.camera is not None:
            self.camera.StopGrabbing()

    def grab(self):
        img = None
        if self.camera is not None:
            grabResult = self.camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException)
            image = self.converter.Convert(grabResult)
            img = image.GetArray()
            grabResult.Release()
        else:
            img = np.ones(
                (300, 500, 3)) * 255 / 8 * (2 + np.sin(time.time_ns() * 3.e-9))
            img = img.astype(np.uint8)
        return img
