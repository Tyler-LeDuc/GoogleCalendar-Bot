from __future__ import print_function
import datetime
import pickle
import os.path
import sys
from dateutil import parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Go to gmail bot and type this in:
# source env/bin/activate
# deactivate
# You might have to delete pickle file

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('CalendarBot/token.pickle'):
        with open('CalendarBot/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'CalendarBot/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('CalendarBot/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    # argv[1] is is the date, everything after goes into summary
    # data = ' '.join(sys.argv[2:])
    # summary = " "
    # for x in data:
    #   if (x != ','):
    #     summary += x
    summary = sys.argv[2]
    print(summary)

    date = parser.parse(sys.argv[1]).strftime('%Y-%m-%d')
    print(date)

    newEvent = {
      'summary': summary,
      'location': '',
      'description': '',
      'start': {
        'date': date,
        'timeZone': 'America/Phoenix',
      },
      'end': {
        'date': date,
        'timeZone': 'America/Phoenix',
      },
    }
    page_token = None
    updated = 0
    while True:
      events = service.events().list(calendarId='9tjiheele3hvldg0dr3gc6omb0@group.calendar.google.com', pageToken=page_token).execute()
      for event in events['items']:
        if (event['summary'] == summary):
            updated = 1
            print("Calendar event: '"+ summary +" "+ event['start']['date'] + " ' rescheduled to: " + date)
            updated_event = service.events().update(calendarId='9tjiheele3hvldg0dr3gc6omb0@group.calendar.google.com', eventId=event['id'], body=newEvent).execute()

      page_token = events.get('nextPageToken')
      if not page_token:
        break
        
    if (updated == 0):
        event = service.events().insert(calendarId='9tjiheele3hvldg0dr3gc6omb0@group.calendar.google.com', body=newEvent).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    main()