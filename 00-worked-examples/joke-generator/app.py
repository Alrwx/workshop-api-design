"""
Worked example 1: Joke Generator. We build the API together, live.

The frontend (static/index.html) is already done. It calls GET /api/joke
and expects JSON like:
    {"id": 1, "category": "programming", "setup": "...", "punchline": "..."}

Run:
    python 00-worked-examples/joke-generator/app.py
Then open http://127.0.0.1:5000 and click the button. It fails until we
write the route below!
"""

import random

from flask import Flask, jsonify, request

from jokes import JOKES

app = Flask(__name__, static_folder="static", static_url_path="")


@app.get("/")
def home():
    # Serve the finished frontend page.
    return app.send_static_file("index.html")


# ---------------------------------------------------------------
# Let's build this together:
#
#   1. A route for GET /api/joke
#   2. Pick a random joke from JOKES and return it as JSON
#   3. Bonus: support /api/joke?category=programming
#      (return 404 with {"error": "..."} if no jokes match)
#   4. Bonus: GET /api/categories returns the list of categories
# ---------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
