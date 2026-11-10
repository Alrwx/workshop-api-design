"""
Exercise 4 solution: a tiny ACM events server.

Run:
    python solution.py
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


def find_event(event_id):
    return next((e for e in EVENTS if e["id"] == event_id), None)


@app.get("/")
def home():
    return jsonify({"message": "Welcome to the ACM events API!", "try": "/events"})


@app.get("/events")
def list_events():
    event_type = request.args.get("type")
    events = EVENTS
    if event_type:
        events = [e for e in EVENTS if e["type"] == event_type]
    return jsonify(events)


@app.get("/events/<int:event_id>")
def get_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event)


@app.post("/events")
def create_event():
    data = request.get_json(silent=True) or {}

    if not data.get("title") or not data.get("date"):
        return jsonify({"error": "title and date are required"}), 400

    new_event = {
        "id": max((e["id"] for e in EVENTS), default=0) + 1,
        "title": data["title"],
        "date": data["date"],
        "type": data.get("type", "other"),
    }
    EVENTS.append(new_event)
    return jsonify(new_event), 201


# Bonus
@app.delete("/events/<int:event_id>")
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    EVENTS.remove(event)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
