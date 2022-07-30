from __future__ import print_function

from datetime import datetime, timezone
import pytz
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def local_to_utc(local_dt):
    return local_dt.astimezone(pytz.utc)


class Calendar:
    def __init__(self, tz='US/Pacific'):
        # Init credentials
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None
        if os.path.exists('credentials/calendar_token.json'):
            creds = Credentials.from_authorized_user_file('credentials/calendar_token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/calendar_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('credentials/calendar_token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('calendar', 'v3', credentials=creds)
        self.tz = pytz.timezone(tz)

    def get_today_events(self):
        # get current datetime
        now_local = datetime.now(tz=self.tz)

        # create local datetime for start and end of day
        start_local = now_local
        start_utc = local_to_utc(start_local).replace(tzinfo=None).isoformat() + 'Z'
        end_local = now_local.replace(hour=23, minute=59, second=0)
        end_utc = local_to_utc(end_local).replace(tzinfo=None).isoformat() + 'Z'

        # get today calendar events
        events_result = self.service.events().list(calendarId='primary', timeMin=start_utc, timeMax=end_utc,
                                                   singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        # Prints the start and name of the next 10 events
        event_summaries = []
        event_times = []

        for event in events:
            try:
                dt = datetime.strptime(event['start']['dateTime'], "%Y-%m-%dT%H:%M:%S%z" )
                event_times.append(dt.strftime("%H:%M"))
            except: #Time is not provided with event, its just an all day event
                event_times.append("23:59")
            event_summaries.append(event['summary'])


        return event_times, event_summaries


if __name__ == '__main__':
    cal = Calendar()
    cal.get_today_events()