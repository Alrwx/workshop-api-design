"""
Worked example 1 solution: the finished Joke Generator API.

Run:
    python 00-worked-examples/joke-generator/solution.py
Then open http://127.0.0.1:5000
"""

import random

from flask import Flask, jsonify, request

from jokes import JOKES

app = Flask(__name__, static_folder="static", static_url_path="")


@app.get("/")
def home():
    # Serve the finished frontend page.
    return app.send_static_file("index.html")


@app.get("/api/joke")
def random_joke():
    category = request.args.get("category")  # None if not given
    options = JOKES
    if category:
        options = [j for j in JOKES if j["category"] == category]
    if not options:
        return jsonify({"error": f"No jokes in category {category!r}"}), 404
    return jsonify(random.choice(options))


@app.get("/api/categories")
def categories():
    return jsonify(sorted({j["category"] for j in JOKES}))


if __name__ == "__main__":
    app.run(debug=True)
