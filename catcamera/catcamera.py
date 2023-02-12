from service.camera import Camera
from service.label import Labels
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

def __file_path_prefix(dir):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    prefix = "{}/picture-{}".format(dir, timestamp)
    return prefix

def main():
    PICTURES_DIR = "pictures"
    logger.info("Starting catcamera")
    camera = Camera()
    labels = Labels()
    if (os.path.exists(PICTURES_DIR)):
        prefix = __file_path_prefix(PICTURES_DIR)
        photo_path = "{}.jpg".format(prefix)
        logger.info("Taking a picture: {}".format(photo_path))
        camera.take_photo(photo_path)
        logger.info("Getting image labels")
        photo_labels = labels.image_labels(photo_path)
        csv_path = "{}.csv".format(prefix)
        logger.info("Saving labels: {}".format(csv_path))
        labels.export_csv(csv_path, photo_labels)
        logger.info("Success!")
    else:
        error_message = "{} directory doesn't exist".format(PICTURES_DIR)
        logger.error(error_message)
        sys.exit(error_message)

if __name__ == '__main__':
    main()

