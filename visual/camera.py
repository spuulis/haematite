from pypylon import pylon


class Camera():
    def __init__(self, fps: int, exposure_time: int):
        self.fps = fps
        self.exposure_time = exposure_time

        # Connect to the first available camera
        self.camera = pylon.InstantCamera(
            pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.camera.ExposureTime.SetValue(self.exposure_time)
        self.camera.Close()

        # Image converter to cv2 format (bgr)
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # Calibration parameters
        self.mtx = None
        self.dist = None
    
    def calibrate(self, mtx, dist):
        self.mtx = mtx
        self.dist = dist

    def start_capture(self):
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stop_capture(self):
        self.camera.StopGrabbing()

    def grab(self):
        grabResult = self.camera.RetrieveResult(
            5000, pylon.TimeoutHandling_ThrowException)
        image = self.converter.Convert(grabResult)
        img = image.GetArray()
        grabResult.Release()
        return img
