from __future__ import print_function
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('gmailBot/token.pickle'):
        with open('gmailBot/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmailBot/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('gmailBot/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)


    subject = "subject"
    msgPlain = ""
    with open('/Users/tylerleduc/Documents/FultonBot/log.txt', 'r') as file:
        for line in file:
            msgPlain += line
        # content = [line.strip() for line in file]
    print(msgPlain)
    # Call the Gmail API
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sys.argv[1]
    msg['From'] = sys.argv[2]
    msg['To'] = "testfultonbot123@gmail.com"        # TODO: change email
    msg.attach(MIMEText(msgPlain, 'plain'))
    message = {'raw': base64.urlsafe_b64encode(msg.as_string())}


    try:
        message = (service.users().messages().send(userId="me", body=message).execute())
        print('Message Id: %s' % message['id'])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()