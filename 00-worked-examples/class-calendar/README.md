# Worked example 2: Where's Alvin?

A slightly cheeky page that shows whether Alvin is in class right now and his week of classes, pulled live from his public **Classes** Google Calendar.

```bash
python 00-worked-examples/class-calendar/app.py
```

Open http://127.0.0.1:5000.

**No API key yet?** It runs in **demo mode** with made-up classes, so you can still see it work. To use the real calendar, put `GOOGLE_API_KEY` (and optionally `GOOGLE_CALENDAR_ID`) in `.env`. See [exercise 5's SETUP.md](../../exercises/05-google-calendar/SETUP.md). Want it to be about you? Set `CALENDAR_OWNER=YourName` and point `GOOGLE_CALENDAR_ID` at your own public calendar.

## How it works

```
 browser                          our Flask server (app.py)                 Google
┌──────────────┐  GET /api/classes  ┌──────────────────────┐  GET .../events?key=SECRET  ┌──────────┐
│ index.html   │ ─────────────────▶ │ /api/classes         │ ──────────────────────────▶ │ Calendar │
│              │ ◀───────────────── │ simplify() the data  │ ◀────────────────────────── │   API    │
└──────────────┘  {"events": [...]}  └──────────────────────┘   lots of Google JSON        └──────────┘
```

Two APIs here:

1. **Google's API**, which we *use*. `fetch_google_events()` calls it with our key.
2. **Our own API** (`/api/classes`), which we *build*. `simplify()` throws away the Google JSON we don't need and returns a small, clean shape the page understands.

## Read through it together

- `fetch_google_events()`: the same request as exercise 5, but with `timeMax` so we only get this week.
- `simplify()`: why not just send Google's JSON straight to the browser? (Smaller, and the frontend doesn't care that it came from Google. We could switch calendars without touching the page.)
- The error handling in `classes()`: if Google fails, we return **502 Bad Gateway** ("the server behind me failed") with Google's reason.
- `index.html`: `fetch("/api/classes")`, then plain JavaScript decides "in class", "free for 2h", or "done for the day".

## Why the key stays on the server

If the page called Google directly, the key would be in the JavaScript, and anyone could open DevTools and copy it. Going through our server keeps it secret. The ACM website will do the same thing: see [`docs/calendar-integration-plan.md`](../../docs/calendar-integration-plan.md).
