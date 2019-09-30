from mailservice.gmailservice import GmailService
from cameraservice.camera import Camera
import time
from datetime import datetime
import json
import os


def process_unread_messages(mail_service, camera, secret):
    messages = mail_service.list_messages_matching_query("me", "label:unread")
    for message in messages:
        msg = mail_service.get_message("me", message['id'])
        #print("MESSAGE: %s" % msg['payload']['headers'])

        subject = next(
            header['value'] for header in msg['payload']['headers'] if header['name'].lower() == "subject")
        #print(subject)

        if subject == secret:
            fromAddress = next(
                header['value'] for header in msg['payload']['headers'] if header['name'].lower() == "from")
            print
            print("New photo request from: %s" % fromAddress)
            fromAddressParsed = fromAddress.split('<')[1].split('>')[0]

            photos_dir = os.environ['CATCAMERA_PHOTOS_DIR']
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            photo_name = "catcamera_%s.jpg" % timestamp
            photo_path = "%s/%s" % (photos_dir, photo_name)
            print("Taking new photo at: '%s'" % photo_path)
            camera.take_photo(photo_path)

            response = mail_service.create_message_with_attachment("Emma Eternal Magic", fromAddressParsed, "Ja", "",
                                                            photos_dir,
                                                            photo_name)

            print("Sending new photo to: %s" % fromAddressParsed)
            mail_service.send_message("me", response)

            mail_service.modify_message('me', message['id'], mail_service.create_read_labels())
            print


def main():
    credentials_dir = os.environ['CATCAMERA_CREDS_DIR']
    secret = os.environ['CATCAMERA_SECRET']
    gmail_service = GmailService(credentials_dir)
    camera = Camera()
    sleep_time = 20
    while True:
        process_unread_messages(gmail_service, camera, secret)
        print("Sleeping %d seconds..." % sleep_time)
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()

