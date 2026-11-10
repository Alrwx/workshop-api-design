"""
Exercise 4: Build your own API, a tiny ACM events server.

Run:
    python starter.py
Then, in another terminal:
    curl http://127.0.0.1:5000/events
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Our "database". It's just a list in memory, so it resets when you restart.
EVENTS = [
    {"id": 1, "title": "GBM #4", "date": "2026-11-12", "type": "meeting"},
    {"id": 2, "title": "Intro to APIs", "date": "2026-11-10", "type": "workshop"},
    {"id": 3, "title": "Hack Night", "date": "2026-11-14", "type": "social"},
    {"id": 4, "title": "Git & GitHub", "date": "2026-11-17", "type": "workshop"},
]


@app.get("/")
def home():
    return jsonify({"message": "Welcome to the ACM events API!", "try": "/events"})


@app.get("/events")
def list_events():
    # TODO 1: Read the optional "type" query param with request.args.get("type").
    # TODO 2: If it was given, keep only events whose "type" matches.
    # TODO 3: Return the (maybe filtered) list with jsonify().
    return jsonify([])


@app.get("/events/<int:event_id>")
def get_event(event_id):
    # TODO 4: Find the event whose "id" equals event_id and return it.
    # TODO 5: If there isn't one, return jsonify({"error": "Event not found"}), 404
    return jsonify({})


@app.post("/events")
def create_event():
    data = request.get_json(silent=True) or {}

    # TODO 6: If "title" or "date" is missing from data, return
    #         jsonify({"error": "title and date are required"}), 400

    # TODO 7: Build the new event. Its id is one more than the biggest existing id.
    #         "type" is optional; default it to "other".

    # TODO 8: Append it to EVENTS and return it with status 201.
    return jsonify({}), 501  # 501 means "Not Implemented". Replace this!


if __name__ == "__main__":
    app.run(debug=True)
