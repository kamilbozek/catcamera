from time import sleep
from picamera import PiCamera


class Camera():
    def __init__(self):
        self.camera = PiCamera()

    def take_photo(self, photoPath):
        self.camera.start_preview()
        sleep(2)
        self.camera.capture(photoPath)
        self.camera.stop_preview()
