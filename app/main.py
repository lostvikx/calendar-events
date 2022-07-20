#!/usr/bin/env python3

import os
import json
from dotenv import load_dotenv
import utils

from argparse import ArgumentParser
from event import Event

def parse_args():
  parser = ArgumentParser(description="Interact with the Google Calendar API")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-c", "--create-event", help="create a calendar event", action="store_true")
  group.add_argument("-u", "--update-event", help="update a calendar event using a client id")

  args = parser.parse_args()
  return args

def main():

  # Load any environment variables (API KEY NOT REQUIRED FOR CALENDAR EVENTS)
  dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
  load_dotenv(dotenv_path)

  # Reads credentials from token.json file
  event = Event()
  # TEST: using JSON a file
  test_event = utils.test_json("test/test_event.json")

  args = parse_args()
  # Simulating create event scenario
  if args.create_event:
    # Create Event
    event_details = event.create_event(event_object=test_event)

    # NOTE: Save a temp file!
    with open("test/save_event_details.json", "w") as details_file:
      json.dump(event_details, details_file, indent=2, sort_keys=True)


  # TODO: Save the event ID mapped with client ID: can be a database
  # TODO: Update event to be done using event_id
  # Simulating update event scenario
  if args.update_event:
    # TEST: Read file for updated event
    with open("test/save_event_details.json", "r") as details_file:
      test_event_id = json.load(details_file)["id"]

    # TEST: Update Event (Eg: customer reschedules event)
    event.update_event(test_event_id, new_event_object=test_event)


if __name__ == "__main__":
  main()
