from mailservice.gmailservice import GmailService
import time
import json
import os


def process_unread_messages(service):
    messages = service.list_messages_matching_query("me", "label:unread")
    for message in messages:
        msg = service.get_message("me", message['id'])
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
            response = service.create_message("Emma Eternal Magic", fromAddressParsed, 'Wiadomosc od Emmy',
                                           'Wiadomosc')
            response2 = service.create_message_with_attachment("Emma Eternal Magic", fromAddressParsed, "Ja", "",
                                                            "/home/kamil/tmp",
                                                            "emma.jpg")

            service.send_message("me", response2)

            service.modify_message('me', message['id'], service.create_read_labels())


def main():
    credentials_dir = os.environ['CREDS_DIR']
    gmail_service = GmailService(credentials_dir)
    sleep_time = 10
    while True:
        process_unread_messages(gmail_service)
        print("Sleeping %d seconds..." % sleep_time)
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()

