#!/usr/bin/env python3

import datetime
import os
import json

from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Important function to authenticate the enterprise account
def authenticate_app(uri, creds):
  """
  Authenticate dev account.

  Args:
    uri: list of Google Calendar API endpoints
    creds: None if token.json file doesn't exists
  
  Returns:
    creds: Credentials object by Google API
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


def create_event(creds, event):
  """
  Creates a calendar event.

  Args:
    creds: Credentials for authentication
    event: dict with certain attributes specified in the docs

  Returns:
    An event object, details returned from the API call.
  """
  try:
    service = build("calendar", "v3", credentials=creds)
    # TODO: sendUpdates="all": send email & notification on phone
    evt = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {evt.get('htmlLink')}")
    return evt
  except HttpError as error:
    print(f"An error occurred: {error}")


# Simple data testing using a JSON file.
def test_json(json_filename):

  with open(json_filename, "r") as f:
    event = json.load(f)

  def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%d %b %Y %H:%M").isoformat()

  event["start"]["dateTime"] = parse_datetime(event["start"]["dateTime"])
  event["end"]["dateTime"] = parse_datetime(event["end"]["dateTime"])

  return event


def update_event(event_id, creds, new_event):
  """
  Updates a calendar event.

  Args:
    event_id: string
    creds: Credentials object
    new_event: Object conforming to the event object structure
  
  Returns:
    None
  """
  try:
    service = build("calendar", "v3", credentials=creds)

    updated_event = service.events().update(calendarId="primary", eventId=event_id, body=new_event).execute()

    print(f"Event updated: {updated_event['updated']}")
  except HttpError as error:
    print(f"An error occurred: {error}")


def main():

  # Load any env vars
  dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
  load_dotenv(dotenv_path)

  # Authenticate enterprise application
  credentials = authenticate_app(["https://www.googleapis.com/auth/calendar"], None)

  # TESTING using JSON a file
  test_event = test_json("test_event.json")
  event_details = create_event(creds=credentials, event=test_event)

  # TEMPORARY
  # Save event details in a file for reference
  with open("event_details.json", "w") as details_file:
    json.dump(event_details, details_file, indent=2, sort_keys=True)

  # Save event_id with customer's client ID
  # Read file for updated event
  with open("event_details.json", "r") as details_file:
    test_event_id = json.load(details_file)["id"]

  # Update Event (Eg: customer reschedules event)
  # update_event(test_event_id, creds=credentials, new_event=test_event)


if __name__ == "__main__":
  main()
