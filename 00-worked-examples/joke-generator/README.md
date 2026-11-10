# Worked example 1: Joke Generator

The frontend is finished. It has a button that calls `GET /api/joke`. The API doesn't exist yet, so the page shows a **404**. We'll write it together.

```bash
python 00-worked-examples/joke-generator/app.py
```

Open http://127.0.0.1:5000 and click **Tell me a joke**. 404! Open the **"What just happened?"** panel to see the request and response.

## The contract

Before writing any code, agree on what the API returns. The frontend expects:

```
GET /api/joke                          → 200 {"id": 1, "category": "programming", "setup": "...", "punchline": "..."}
GET /api/joke?category=gator           → 200 a random gator joke
GET /api/joke?category=nope            → 404 {"error": "No jokes in category 'nope'"}
GET /api/categories                    → 200 ["gator", "general", "programming"]
```

This agreement between frontend and backend **is** the API. Either side can be rewritten as long as it keeps the contract.

## Live-coding steps

1. **Add the route.** In `app.py`:

   ```python
   @app.get("/api/joke")
   def random_joke():
       return jsonify(random.choice(JOKES))
   ```

   Save (Flask reloads), click the button. 🎉 Look at the panel: `200 OK` and the JSON.

2. **Try it without the page.** The browser isn't special:

   ```bash
   curl http://127.0.0.1:5000/api/joke
   python -c "import requests; print(requests.get('http://127.0.0.1:5000/api/joke').json())"
   ```

3. **Add a query param.** `request.args.get("category")`, filter `JOKES`, return a 404 with an `error` if nothing matches. Pick a category in the page's dropdown... which is empty. Why?

4. **Add `/api/categories`.** Refresh: the dropdown fills itself. The frontend was calling it all along.

5. **Break it on purpose.** Return a plain string instead of `jsonify(...)`, or misspell `"setup"`. See how the frontend reacts. That's why the contract matters.

Finished version: [`solution.py`](solution.py).

## Ideas to take further

- `POST /api/joke` to submit a new joke
- `GET /api/joke/<id>` for a specific joke
- Swap `jokes.py` for a real database (SQLite)
