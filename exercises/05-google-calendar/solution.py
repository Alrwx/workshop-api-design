"""
Exercise 5 solution: list upcoming events from a public Google Calendar.

Setup: see SETUP.md. Needs GOOGLE_API_KEY and GOOGLE_CALENDAR_ID in .env

Usage:
    python solution.py
    python solution.py 5        # show 5 events
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
    params = {
        "key": API_KEY,
        "timeMin": datetime.now(timezone.utc).isoformat(),
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": max_results,
    }
    response = requests.get(url, params=params, timeout=10)

    if not response.ok:
        # Google puts a human-readable reason in the error body. Show it.
        message = response.json().get("error", {}).get("message", response.text)
        print(f"Google said {response.status_code}: {message}")
        print("See the Troubleshooting table in SETUP.md.")
        sys.exit(1)

    return response.json().get("items", [])


def format_event(event):
    """One line per event. Handles timed and all-day events."""
    start = event["start"]
    title = event.get("summary", "(no title)")
    location = f"  ({event['location']})" if event.get("location") else ""

    if "dateTime" in start:  # timed event, e.g. "2026-11-10T13:55:00-05:00"
        # (.replace handles a trailing "Z", which older Pythons can't parse)
        when = datetime.fromisoformat(start["dateTime"].replace("Z", "+00:00")).strftime("%a %b %d  %I:%M %p")
    else:  # all-day event, e.g. "2026-11-11"
        when = datetime.fromisoformat(start["date"]).strftime("%a %b %d") + "  all day "

    return f"  {when}  {title}{location}"


if __name__ == "__main__":
    if not API_KEY or not CALENDAR_ID:
        print("Missing GOOGLE_API_KEY or GOOGLE_CALENDAR_ID. Copy .env.example to .env and fill it in.")
        sys.exit(1)

    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    events = get_upcoming_events(count)

    if not events:
        print("No upcoming events.")
    else:
        print(f"Next {len(events)} events:")
        for event in events:
            print(format_event(event))
