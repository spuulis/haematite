import threading
import time

import cv2
from pypylon import pylon

from . import tracker
import config

class Camera(threading.Thread):
    def __init__(self, fps):
        threading.Thread.__init__(self)
        self.daemon = True

        self.fps = fps

        self._stopper = threading.Event()

    def stopit(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def run(self):
        # conecting to the first available camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        while not self.stopped() and camera.IsGrabbing():
            time_now = time.time_ns() * 1e-9

            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray()
                cv2.namedWindow('title', cv2.WINDOW_NORMAL)
                cv2.imshow('title', img)
                k = cv2.waitKey(1)
                if k == 27:
                    break
            grabResult.Release()

            # Limit frame rate
            time.sleep(max(1./self.fps - (time.time_ns() * 1e-9 - time_now), 0))

        # Releasing the resource    
        camera.StopGrabbing()

        cv2.destroyAllWindows()