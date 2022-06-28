#!/usr/bin/env python3

import datetime
import os
import json

# from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Important function to authenticate the company account
def authenticate_app(uri, creds):
  """
  Args:
    uri: list of Google Calendar API endpoints
    creds: None if token.json file doesn't exists
  
  Returns:
    creds: Credentials object by Google
  """
  SCOPES = uri

  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
      token.write(creds.to_json())

  return creds


def fetch_upcoming_events(creds, n_events):
  """
  Prints n events on the user's calendar.
  """
  try:
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=n_events, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])

    if not events:
      print('No upcoming events found.')
      return

    # Prints the start and name of the next n_events
    for event in events:
      start = event['start'].get('dateTime', event['start'].get('date'))
      print(start, event['summary'])

  except HttpError as error:
    print('An error occurred: %s' % error)


def create_event(creds, event):
  """
  Creates a calendar event.
  """
  try:
    service = build("calendar", "v3", credentials=creds)

    evt = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {evt.get('htmlLink')}")

  except HttpError as error:
    print(f"An error occurred: {error}")


def main():
  credentials = authenticate_app(["https://www.googleapis.com/auth/calendar"], None)

  # fetch_upcoming_events(creds=credentials, n_events=10)

  with open("test_event.json", "r") as f:
    event = json.load(f)

  # Testing
  start_dateTime, end_dateTime = (event["start"]["dateTime"], event["end"]["dateTime"])

  def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%d %b %Y %H:%M").isoformat()

  start_dateTime = parse_datetime(start_dateTime)
  end_dateTime = parse_datetime(end_dateTime)

  # print(start_dateTime, end_dateTime)

  (event["start"]["dateTime"], event["end"]["dateTime"]) = start_dateTime, end_dateTime
  # print(event["start"]["dateTime"])

  create_event(creds=credentials, event=event)


if __name__ == "__main__":
  main()
