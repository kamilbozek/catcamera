from cameraservice.camera import Camera
from datetime import datetime
from google.cloud import vision
import io
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

def image_labels(photo_path):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath(photo_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print(labels)

    print('Labels:')
    for label in labels:
        print(label.description)

    return labels

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
        logger.info("Getting image labels")
        labels = image_labels(photo_path)
        logger.info("Success!")
    else:
        error_message = "{} directory doesn't exist".format(PICTURES_DIR)
        logger.error(error_message)
        sys.exit(error_message)

if __name__ == '__main__':
    main()

