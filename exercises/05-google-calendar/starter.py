"""
Exercise 5: list upcoming events from a public Google Calendar.

Setup: see SETUP.md. Needs GOOGLE_API_KEY and GOOGLE_CALENDAR_ID in .env

Usage:
    python starter.py
"""

import os
import sys
from datetime import datetime, timezone
from urllib.parse import quote

import requests
from dotenv import load_dotenv

# Read .env and put its values into os.environ. The key never appears in this file.
load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")
CALENDAR_ID = os.environ.get("GOOGLE_CALENDAR_ID")


def get_upcoming_events(max_results=10):
    """Return a list of upcoming events from the calendar."""
    # The calendar ID can contain "#" and "@", so escape it for the URL.
    url = f"https://www.googleapis.com/calendar/v3/calendars/{quote(CALENDAR_ID, safe='')}/events"

    # TODO 1: Build params with: key, timeMin (now, in UTC, ISO format),
    #         singleEvents="true", orderBy="startTime", maxResults=max_results
    params = {}

    # TODO 2: GET the url with params and timeout=10.
    response = None

    # TODO 3: If the response isn't ok (response.ok is False), print the status code
    #         and Google's message, response.json()["error"]["message"], then sys.exit(1).

    # TODO 4: Return the "items" list from the JSON (use .get("items", []) in case it's missing).
    return []


def format_event(event):
    """Return one line describing the event."""
    start = event["start"]
    title = event.get("summary", "(no title)")

    # TODO 5: Timed events have start["dateTime"], all-day events have start["date"].
    #         Turn whichever one exists into a readable string, e.g. "Tue Nov 10  01:55 PM"
    #         Hint: datetime.fromisoformat(...).strftime("%a %b %d  %I:%M %p")
    when = "???"

    # TODO 6 (bonus): add the event's location if it has one.
    return f"  {when}  {title}"


if __name__ == "__main__":
    if not API_KEY or not CALENDAR_ID:
        print("Missing GOOGLE_API_KEY or GOOGLE_CALENDAR_ID. Copy .env.example to .env and fill it in.")
        sys.exit(1)

    events = get_upcoming_events()
    print(f"Next {len(events)} events:")
    for event in events:
        print(format_event(event))
