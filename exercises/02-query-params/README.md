# Exercise 2: Query parameters

**Goal:** Build "Do I need an umbrella?" for walking to class. Get the hourly rain chance in Gainesville for the next 12 hours and give a verdict.

**You'll learn:** query parameters, the `params=` argument, and digging through nested JSON.

**API:** [Open-Meteo forecast](https://open-meteo.com/en/docs), no key needed.

## Step 0: build the URL by hand

Query parameters go after a `?`, separated by `&`:

```
https://api.open-meteo.com/v1/forecast?latitude=29.65&longitude=-82.32&hourly=precipitation_probability&forecast_hours=12&timezone=America/New_York
```

Open it in your browser. Then change things:

- Swap `precipitation_probability` for `temperature_2m`. What changes?
- Add `&temperature_unit=fahrenheit`.
- Remove `latitude`. What status code and error message do you get?

> **Tip:** The [Open-Meteo docs page](https://open-meteo.com/en/docs) has checkboxes that build the URL for you. Most good APIs have something like this.

## Step 1: fill in `starter.py`

Instead of gluing strings together, pass a dict to `params=` and let `requests` build the URL (and escape any spaces or symbols for you).

```bash
python exercises/02-query-params/starter.py
```

Expected output (your numbers will differ):

```
Asked: https://api.open-meteo.com/v1/forecast?latitude=29.65&longitude=-82.32&hourly=...

Rain chance in Gainesville, next 12 hours:
  14:00   5% #
  15:00  10% ##
  16:00  45% #########
  ...
Highest chance: 45% at 16:00
Verdict: Maybe toss an umbrella in your bag. 🌂
```

## The JSON shape

```json
{
  "hourly": {
    "time": ["2026-11-10T14:00", "2026-11-10T15:00", ...],
    "precipitation_probability": [5, 10, ...]
  }
}
```

The two lists line up: item 0 of `time` goes with item 0 of `precipitation_probability`. Use `zip()` to walk them together.

## Bonus

- Take the city as a command line argument and look up its coordinates with the geocoding API from `00-worked-examples/weather-script`.
- Add `temperature_2m` to `hourly` and print it next to the rain chance.
