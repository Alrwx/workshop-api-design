# Intro to APIs

A hands-on workshop from UF ACM. By the end you will know what an API is, how to call one from the terminal and from Python, how to send data to one, how to build a tiny one yourself, and how we plan to use the Google Calendar API on the ACM website.

## Setup (5 minutes)

You need Python 3.9 or newer.

```bash
git clone https://github.com/Alrwx/workshop-api-design.git
cd workshop-api-design
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Check it works:

```bash
python 00-working-example/gator_forecast.py
```

## What is an API?

An **API** (Application Programming Interface) is a way for one program to ask another program for something. A **web API** does it over HTTP, the same protocol your browser uses.

Think of a restaurant. You (the **client**) don't walk into the kitchen. You give the waiter (the **API**) an order from the menu (the **documentation**), and the kitchen (the **server**) sends back your food (the **response**).

```
  client (your code)                         server (pokeapi.co)
  ┌───────────────┐   GET /api/v2/pokemon/pikachu   ┌───────────────┐
  │               │ ──────────────────────────────▶ │               │
  │               │                                  │               │
  │               │ ◀────────────────────────────── │               │
  └───────────────┘   200 OK  {"name": "pikachu"…}   └───────────────┘
```

### The parts of a request

| Part | Example | What it means |
| --- | --- | --- |
| **Method** | `GET`, `POST`, `PUT`, `DELETE` | What you want to do: read, create, update, delete |
| **URL** | `https://pokeapi.co/api/v2/pokemon/pikachu` | Where the thing lives (base URL + **endpoint**) |
| **Query params** | `?latitude=29.65&longitude=-82.32` | Options for the request |
| **Headers** | `Authorization: Bearer abc123` | Extra info: who you are, what format you want |
| **Body** | `{"title": "Study for COP3530"}` | Data you are sending (usually with `POST`/`PUT`) |

### The parts of a response

| Part | Example | What it means |
| --- | --- | --- |
| **Status code** | `200`, `201`, `404`, `401`, `500` | Did it work? |
| **Headers** | `Content-Type: application/json` | Info about the response |
| **Body** | `{"name": "pikachu", "height": 4}` | The data, almost always **JSON** |

### Status codes cheat sheet

- **2xx, it worked.** `200 OK`, `201 Created`
- **4xx, you messed up.** `400 Bad Request`, `401 Unauthorized` (missing or bad key), `403 Forbidden`, `404 Not Found`, `429 Too Many Requests`
- **5xx, they messed up.** `500 Internal Server Error`, `503 Service Unavailable`

### JSON in one minute

JSON is text that looks like Python dicts and lists. `requests` turns it into real dicts and lists for you with `response.json()`.

```json
{
  "name": "pikachu",
  "types": [{ "slot": 1, "type": { "name": "electric" } }]
}
```

In Python: `data["types"][0]["type"]["name"]` gives `"electric"`.

## Try it without code first

Paste this into your browser. That's a GET request!

https://pokeapi.co/api/v2/pokemon/pikachu

Or from the terminal:

```bash
curl https://pokeapi.co/api/v2/pokemon/pikachu
curl -i https://pokeapi.co/api/v2/pokemon/notapokemon   # -i shows the status code: 404
```

## The workshop

Start with the **working example**, then do the exercises in order. Each exercise has a `README.md` with the goal, a `starter.py` with `TODO`s for you to fill in, and a `solution.py` if you get stuck. No peeking for at least 5 minutes!

| | Folder | You'll learn | API used | Key needed? |
| --- | --- | --- | --- | --- |
| ⭐ | [`00-working-example`](00-working-example) | What a full API program looks like | Open-Meteo | No |
| 1 | [`01-first-request`](exercises/01-first-request) | GET, status codes, reading JSON | PokéAPI | No |
| 2 | [`02-query-params`](exercises/02-query-params) | Query parameters, nested JSON | Open-Meteo | No |
| 3 | [`03-sending-data`](exercises/03-sending-data) | POST, request bodies, headers | JSONPlaceholder | No |
| 4 | [`04-build-your-own-api`](exercises/04-build-your-own-api) | Being the server: routes, JSON, status codes | Your own (Flask) | No |
| 5 | [`05-google-calendar`](exercises/05-google-calendar) | API keys, real-world docs, Google Calendar | Google Calendar | Yes |

Exercise 5 is the one we'll use on the ACM website. Setting up a Google Cloud API key takes about 15 minutes, so it's fine to do it after the workshop. See [`docs/calendar-integration-plan.md`](docs/calendar-integration-plan.md) for how it fits into the site.

## Suggested agenda (about 90 minutes)

| Time | What |
| --- | --- |
| 0:00 | What is an API? (whiteboard) |
| 0:15 | Try it in the browser and with `curl` |
| 0:20 | Walk through the working example |
| 0:30 | Exercise 1 |
| 0:40 | Exercise 2 |
| 0:50 | Exercise 3 |
| 1:00 | Exercise 4 |
| 1:15 | Exercise 5 demo + how the ACM site will use it |
| 1:30 | Done |

## Good habits

- **Read the docs.** Every API has them. The docs are the menu.
- **Check the status code** before you trust the body (`response.raise_for_status()`).
- **Set a timeout** (`requests.get(url, timeout=10)`) so your program doesn't hang forever.
- **Never commit API keys.** Put them in a `.env` file (already in `.gitignore`) or an environment variable.
- **Be nice to free APIs.** Don't call them in a tight loop. Many have rate limits (`429`).

## APIs to play with afterwards

- [PokéAPI](https://pokeapi.co/docs/v2): Pokémon data, no key
- [Open-Meteo](https://open-meteo.com/en/docs): weather, no key
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/): fake data for practice, no key
- [Open Library](https://openlibrary.org/developers/api): books, no key
- [NASA APIs](https://api.nasa.gov/): space photos, free key
- [GitHub REST API](https://docs.github.com/en/rest): repos and users, key optional
- [public-apis list](https://github.com/public-apis/public-apis): hundreds more
