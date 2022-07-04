#!/usr/bin/env python3

import datetime
import os
import json
from dotenv import load_dotenv

from event import Event


# Simple data testing using a JSON file.
def test_json(json_filename):

  with open(json_filename, "r") as f:
    event = json.load(f)

  def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%d %b %Y %H:%M").isoformat()

  event["start"]["dateTime"] = parse_datetime(event["start"]["dateTime"])
  event["end"]["dateTime"] = parse_datetime(event["end"]["dateTime"])

  return event


def main():

  # Load any environment variables
  dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
  load_dotenv(dotenv_path)

  # Reads credentials from token.json file
  event = Event()

  # TEST: using JSON a file: test_event.json
  test_event = test_json("test_event.json")

  # TEST: Create Event
  event_details = event.create_event(event_object=test_event)

  # TEMP
  # Save event details in a file for reference
  with open("event_details.json", "w") as details_file:
    json.dump(event_details, details_file, indent=2, sort_keys=True)


  # TODO: Save the event ID mapped with client ID
  # Read file for updated event
  # with open("event_details.json", "r") as details_file:
  #   test_event_id = json.load(details_file)["id"]

  # TEST: Update Event (Eg: customer reschedules event)
  # event.update_event(test_event_id, new_event_object=test_event)


if __name__ == "__main__":
  main()
