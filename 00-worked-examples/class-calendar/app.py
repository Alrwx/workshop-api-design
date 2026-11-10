"""
Worked example 2: "Where's Alvin?", a class calendar powered by the Google Calendar API.

How it works:
    browser (static/index.html)  --GET /api/classes-->  this Flask server
    this Flask server            --GET events?key=...-->  Google Calendar API

The browser never talks to Google directly, so the API key stays secret on the
server. This is exactly how the ACM website's events section will work.

Setup: GOOGLE_API_KEY and GOOGLE_CALENDAR_ID in .env (see exercises/05-google-calendar/SETUP.md)
No key yet? It runs in demo mode with made-up classes.

Run:
    python 00-worked-examples/class-calendar/app.py
Then open http://127.0.0.1:5000
"""

import os
from datetime import datetime, timedelta
from urllib.parse import quote
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")
CALENDAR_ID = os.environ.get("GOOGLE_CALENDAR_ID")
OWNER = os.environ.get("CALENDAR_OWNER", "Alvin")
GAINESVILLE = ZoneInfo("America/New_York")

app = Flask(__name__, static_folder="static", static_url_path="")


def fetch_google_events(start, end):
    """Ask Google for every event between start and end. Returns Google's raw items."""
    url = f"https://www.googleapis.com/calendar/v3/calendars/{quote(CALENDAR_ID, safe='')}/events"
    params = {
        "key": API_KEY,
        "timeMin": start.isoformat(),
        "timeMax": end.isoformat(),
        "singleEvents": "true",  # expand "every MWF" into separate events
        "orderBy": "startTime",
        "maxResults": 100,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("items", [])


def simplify(event):
    """Keep only what the frontend needs. Our API, our shape."""
    start, end = event["start"], event["end"]
    return {
        "title": event.get("summary", "(no title)"),
        "location": event.get("location", ""),
        "start": start.get("dateTime", start.get("date")),
        "end": end.get("dateTime", end.get("date")),
        "allDay": "dateTime" not in start,
    }


def demo_events(start):
    """Made-up classes for this week, so the page works without an API key."""
    schedule = {
        0: [("COP3530 Data Structures", "CSE E119", 10, 40, 11, 30), ("MAC2313 Calc 3", "Little 101", 13, 55, 14, 45)],
        1: [("CEN3031 Software Engineering", "NEB 100", 11, 45, 13, 40)],
        2: [("COP3530 Data Structures", "CSE E119", 10, 40, 11, 30), ("MAC2313 Calc 3", "Little 101", 13, 55, 14, 45)],
        3: [("CEN3031 Software Engineering", "NEB 100", 11, 45, 13, 40), ("ACM GBM", "Marston L136", 18, 30, 19, 30)],
        4: [("COP3530 Data Structures", "CSE E119", 10, 40, 11, 30)],
    }
    events = []
    for offset in range(7):
        day = start + timedelta(days=offset)
        for title, place, sh, sm, eh, em in schedule.get(day.weekday(), []):
            events.append({
                "title": title,
                "location": place,
                "start": day.replace(hour=sh, minute=sm).isoformat(),
                "end": day.replace(hour=eh, minute=em).isoformat(),
                "allDay": False,
            })
    return events


@app.get("/")
def home():
    return app.send_static_file("index.html")


@app.get("/api/classes")
def classes():
    # This week: from midnight today, 7 days ahead, in Gainesville time.
    today = datetime.now(GAINESVILLE).replace(hour=0, minute=0, second=0, microsecond=0)
    week_later = today + timedelta(days=7)

    if not API_KEY or not CALENDAR_ID or request.args.get("demo"):
        return jsonify({"owner": OWNER, "demo": True, "events": demo_events(today)})

    try:
        items = fetch_google_events(today, week_later)
    except requests.HTTPError as error:
        # Pass Google's reason along so the page can show something useful.
        status = error.response.status_code
        reason = error.response.json().get("error", {}).get("message", "unknown error")
        return jsonify({"error": f"Google said {status}: {reason}"}), 502
    except requests.RequestException as error:
        return jsonify({"error": f"Couldn't reach Google: {error}"}), 502

    return jsonify({"owner": OWNER, "demo": False, "events": [simplify(e) for e in items]})


if __name__ == "__main__":
    app.run(debug=True)
