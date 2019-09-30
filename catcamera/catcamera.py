from mailservice.gmailservice import GmailService
from cameraservice.camera import Camera
import time
from datetime import datetime
import json
import os


def process_unread_messages(mail_service, camera):
    messages = mail_service.list_messages_matching_query("me", "label:unread")
    for message in messages:
        msg = mail_service.get_message("me", message['id'])
        print("MESSAGE: %s" % msg['payload']['headers'])

        subject = next(
            header['value'] for header in msg['payload']['headers'] if header['name'].lower() == "subject")
        print(subject)

        if subject == "foto":
            fromAddress = next(
                header['value'] for header in msg['payload']['headers'] if header['name'].lower() == "from")
            # fromAddress = "kamil.bozek@gmail.com"
            fromAddressParsed = fromAddress.split('<')[1].split('>')[0]
            print(fromAddressParsed)
            response = mail_service.create_message("Emma Eternal Magic", fromAddressParsed, 'Wiadomosc od Emmy',
                                           'Wiadomosc')

            photos_dir = os.environ['PICAMERA_DIR']
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            photo_name = "catcamera_%s" % timestamp
            photo_path = "%s/%s" % (photos_dir, photo_name)
            print("Taking new photo at: '%s'" % photo_path)
            camera.take_photo(photo_path)

            response2 = mail_service.create_message_with_attachment("Emma Eternal Magic", fromAddressParsed, "Ja", "",
                                                            photos_dir,
                                                            photo_name)

            mail_service.send_message("me", response2)

            mail_service.modify_message('me', message['id'], mail_service.create_read_labels())


def main():
    credentials_dir = os.environ['CREDS_DIR']
    gmail_service = GmailService(credentials_dir)
    camera = Camera()
    sleep_time = 10
    while True:
        process_unread_messages(gmail_service)
        print("Sleeping %d seconds..." % sleep_time)
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()

