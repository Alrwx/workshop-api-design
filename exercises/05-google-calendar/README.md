# Exercise 5: Google Calendar

**Goal:** List the next 10 events from a real Google Calendar.

**You'll learn:** API keys, reading real-world API docs, keeping secrets out of your code.

**API:** [Google Calendar API, Events: list](https://developers.google.com/workspace/calendar/api/v3/reference/events/list). **Needs a free API key.**

**Why this one?** It's how the ACM website will show upcoming club events. See [`docs/calendar-integration-plan.md`](../../docs/calendar-integration-plan.md).

## Step 0: setup

Follow [SETUP.md](SETUP.md) to get an API key and a calendar ID into your `.env` file. If you're short on time in the workshop, watch the demo and do this part at home.

## Step 1: read the docs

Open the [Events: list reference](https://developers.google.com/workspace/calendar/api/v3/reference/events/list). Real API docs are long, so look for these:

- **HTTP request:** `GET https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events`
- **Parameters** we'll use:
  - `key`: your API key
  - `timeMin`: only events ending after this time (format: `2026-11-10T18:00:00Z`)
  - `singleEvents=true`: expand repeating events (like a class every MWF) into separate events
  - `orderBy=startTime`: sort by start (only allowed with `singleEvents=true`)
  - `maxResults`: how many to return
- **Response:** a JSON object whose `items` is a list of [Event](https://developers.google.com/workspace/calendar/api/v3/reference/events#resource) objects

One gotcha: an event's start is **either** `start["dateTime"]` (a timed event) **or** `start["date"]` (an all-day event). Your code needs to handle both.

## Step 2: fill in `starter.py`

```bash
python exercises/05-google-calendar/starter.py
```

Expected output:

```
Next 10 events:
  Tue Nov 10  1:55 PM  COP3530 Lecture  (CSE E119)
  Tue Nov 10  6:30 PM  ACM: Intro to APIs
  Wed Nov 11  all day  Veterans Day
  ...
```

## Hints

- The calendar ID can contain `#` and `@`, which mean special things in URLs. Wrap it with `urllib.parse.quote(calendar_id, safe="")`.
- Current time in the right format: `datetime.now(timezone.utc).isoformat()`
- Turn `"2026-11-10T13:55:00-05:00"` into a datetime with `datetime.fromisoformat(...)`, then format it with `.strftime("%a %b %d  %I:%M %p")`.

## Bonus

- Only show events in the next 7 days (`timeMax`).
- Search with the `q` parameter, e.g. only events containing "ACM".
- Print the `htmlLink` so you can click through to the event.

## Going further: private calendars and OAuth

An API key can only read **public** calendars. To read someone's **private** calendar, or to **create** events, you need **OAuth**: the "Sign in with Google" screen where the user agrees to let your app see their calendar. Google's [Python quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python) walks through it. The ACM site doesn't need this, because our events are public.
