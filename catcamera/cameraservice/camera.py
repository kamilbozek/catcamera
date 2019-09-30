from time import sleep
from picamera import PiCamera


class Camera():
    def __init__(self):
        self.camera = PiCamera()

    def take_photo(self, photoPath):
        camera.start_preview()
        sleep(2)
        camera.capture(photoPath)
        camera.stop_preview()
