#!/usr/bin/env python3

import os
import json
from dotenv import load_dotenv
import utils

from event import Event


def main():

  # Load any environment variables (API KEY NOT REQUIRED FOR CALENDAR EVENTS)
  dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
  load_dotenv(dotenv_path)

  # Reads credentials from token.json file
  event = Event()

  # TEST: using JSON a file: test_event.json
  test_event = utils.test_json("test/test_event.json")

  # TEST: Create Event
  event_details = event.create_event(event_object=test_event)

  # TEMP
  # Save event details in a file for reference
  with open("test/save_event_details.json", "w") as details_file:
    json.dump(event_details, details_file, indent=2, sort_keys=True)


  # TODO: Save the event ID mapped with client ID
  # Read file for updated event
  # with open("test/save_event_details.json", "r") as details_file:
  #   test_event_id = json.load(details_file)["id"]

  # TEST: Update Event (Eg: customer reschedules event)
  # event.update_event(test_event_id, new_event_object=test_event)


if __name__ == "__main__":
  main()
