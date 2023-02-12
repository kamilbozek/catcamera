from time import sleep
from picamera import PiCamera


class Camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.ISO = 800
        self.camera.resolution = (2592, 1944)

    def take_photo(self, photoPath):
        self.camera.start_preview()
        sleep(2)
        self.camera.capture(photoPath)
        self.camera.stop_preview()
