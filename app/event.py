#!/usr/bin/env python3

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Event:

  def __init__(self, creds=None):
    """
    Contructing an `Event` object, authenticates the application automatically.

    Args:
      `creds`: Google API credentials | default is `None`
    """

    # Authenticate the enterprise dev account

    self.creds = creds

    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    if os.path.exists('token.json'):
      self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        self.creds = flow.run_local_server(port=0)

      # Save the credentials for the next run
      with open('token.json', 'w') as token:
        token.write(self.creds.to_json())

    # Serivce object:
    self.service = build("calendar", "v3", credentials=self.creds)


  def create_event(self, event_object:dict)->dict:
    """
    Creates a calendar event.

    Args:
      * `event_object`: Basic `dict` with certain attributes specified in the API [docs](https://developers.google.com/calendar/api/v3/reference/events#resource)

    Returns:
      An event object, `event_details` from the API.
    """
    try:
      # Use sendUpdates="all" kwarg to send email & UI notification on creation of the event.
      event_details = self.service.events().insert(
        calendarId="primary", body=event_object, sendUpdates="all").execute()

      print(f"Event created: {event_details.get('htmlLink')}")
      return event_details

    except HttpError as error:
      print(f"An error occurred: {error}")


  def update_event(self, event_id:str, new_event_object:dict)->None:
    """
    Updates a calendar event.

    Args:
      * `event_id`: string associated with the event
      * `new_event_object`: Object conforming to the event object structure
    """
    try:
      updated_event = self.service.events().update(
        calendarId="primary", eventId=event_id, body=new_event_object).execute()

      print(f"Event updated: {updated_event['updated']}")

    except HttpError as error:
      print(f"An error occurred: {error}")

