from cameraservice.camera import Camera
from datetime import datetime
import logging
import os
import sys


logger = logging.getLogger("default_logger")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
ch.setFormatter(formatter)
logger.addHandler(ch)

def main():
    PICTURES_DIR = "pictures"
    logger.info("Starting catcamera")
    camera = Camera()
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    if (os.path.exists(PICTURES_DIR)):
        photo_path = "{}/picture-{}.jpg".format(PICTURES_DIR, timestamp)
        logger.info("Taking a picture: {}".format(photo_path))
        camera.take_photo(photo_path)
        logger.info("Success!")
    else:
        error_message = "{} directory doesn't exist".format(PICTURES_DIR)
        logger.error(error_message)
        sys.exit(error_message)

if __name__ == '__main__':
    main()

