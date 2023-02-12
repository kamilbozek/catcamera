from google.cloud import vision
import csv  
import io
import os


class Labels():
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def image_labels(self, photo_path):
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

        return labels
    
    def export_csv(self, file_path, labels):
        with open(file_path, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            header = ['mid', 'description', 'score', 'topicality']
            writer.writerow(header)
            for label in labels:
                print(label.description)
                data = [label.mid, label.description, label.score, label.topicality]
                writer.writerow(data)
