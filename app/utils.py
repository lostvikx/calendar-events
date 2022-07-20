import datetime
import json

def parse_datetime(datetime_string):
  return datetime.datetime.strptime(datetime_string, "%d %b %Y %H:%M").isoformat()

# Simple data testing using a JSON file.
def test_json(json_filename):

  with open(json_filename, "r") as f:
    event = json.load(f)

  event["start"]["dateTime"] = parse_datetime(event["start"]["dateTime"])
  event["end"]["dateTime"] = parse_datetime(event["end"]["dateTime"])

  return event
