import time

import numpy as np
from pypylon import pylon


class Camera():
    def __init__(self):
        # Calibration parameters
        self.mtx = None
        self.dist = None

        # Physical camera parameters
        self.camera = None
        self.exposure_time = None

        # Image converter to cv2 format (bgr)
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def initialize(self, exposure_time: int):
        # Connect to the first available camera
        try:
            self.camera = pylon.InstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.set_exposure_time(exposure_time)
        except Exception as e:
            raise Exception(f"Camera could not be initialized:\n\n{e}")

    def calibrate(self, mtx, dist):
        self.mtx = np.array(mtx)
        self.dist = np.array(dist)

    def set_exposure_time(self, exposure_time):
        self.exposure_time = exposure_time
        if self.camera is not None:
            self.camera.Open()
            self.camera.ExposureTime.SetValue(self.exposure_time)
            self.camera.Close()

    def start_capture(self):
        if self.camera is not None:
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stop_capture(self):
        if self.camera is not None:
            self.camera.StopGrabbing()

    def grab(self) -> tuple[bool, np.ndarray]:
        img = None
        if self.camera is not None:
            grabResult = self.camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException)
            if grabResult is False:
                return False, None
            image = self.converter.Convert(grabResult)
            img = image.GetArray()
            grabResult.Release()
        else:
            img = np.ones(
                (300, 500, 3)) * 255 / 8 * (2 + np.sin(time.time_ns() * 3.e-9))
            img = img.astype(np.uint8)
        return True, img
