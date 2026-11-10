# Exercise 4: Build your own API

**Goal:** Switch sides. Instead of calling an API, you'll **be** the server: a tiny ACM events API.

**You'll learn:** routes (endpoints), returning JSON, reading query params and request bodies, and choosing the right status code.

**Tool:** [Flask](https://flask.palletsprojects.com/), a small Python web framework.

This is the same shape of data the ACM website's events section will use, so you're building a mini version of the real thing.

## Step 1: run the starter

```bash
python exercises/04-build-your-own-api/starter.py
```

You'll see `Running on http://127.0.0.1:5000`. Leave it running and open a **second terminal**.

```bash
curl http://127.0.0.1:5000/
```

You just called your own API! 🎉

## Step 2: fill in the TODOs

Make these endpoints work:

| Method | URL | Returns |
| --- | --- | --- |
| `GET` | `/events` | All events, `200` |
| `GET` | `/events?type=workshop` | Only events of that type, `200` |
| `GET` | `/events/2` | One event, `200`, or `{"error": "..."}` with `404` |
| `POST` | `/events` | Creates an event, `201`. Missing `title` or `date` gives `400` |

Flask restarts on its own when you save the file (that's what `debug=True` does).

## Step 3: test it

```bash
curl http://127.0.0.1:5000/events
curl "http://127.0.0.1:5000/events?type=workshop"
curl -i http://127.0.0.1:5000/events/2
curl -i http://127.0.0.1:5000/events/999          # should be 404

curl -i -X POST http://127.0.0.1:5000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Resume Review", "date": "2026-11-20", "type": "career"}'   # 201

curl -i -X POST http://127.0.0.1:5000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "No date"}'                         # should be 400
```

Or call it from Python, just like exercises 1 to 3:

```python
import requests
print(requests.get("http://127.0.0.1:5000/events").json())
```

## Hints

- `request.args.get("type")` reads a query param (or `None` if missing).
- `request.get_json()` reads the JSON body as a dict.
- Return a tuple to set the status: `return jsonify({"error": "Not found"}), 404`

## Bonus

- Add `DELETE /events/<id>`, returning `204` with an empty body.
- Point your exercise 1 to 3 skills at it: write a `client.py` that lists events and creates one.
- Events disappear when you restart. Why? How would a real API fix that?
