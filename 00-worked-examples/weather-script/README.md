# Extra example: Gator Forecast (weather script)

Before writing any code yourself, run and read a complete API program.

```bash
python 00-worked-examples/weather-script/gator_forecast.py
python 00-worked-examples/weather-script/gator_forecast.py --city Tampa
python 00-worked-examples/weather-script/gator_forecast.py --city Notarealplace
```

Sample output:

```
🐊 Weather for Gainesville, Florida
----------------------------------------
Right now: 78.4°F (feels like 80.1°F)
           Partly cloudy ⛅
           Wind 6.2 mph

Next 3 days:
  2026-11-10   61.2°F to  81.5°F    5% rain  Mainly clear 🌤️
  ...
```

## What's happening

It chains **two API calls**, using the answer from the first in the second:

```
"Gainesville" ──▶ Geocoding API ──▶ (29.65, -82.32) ──▶ Forecast API ──▶ weather JSON ──▶ pretty output
```

1. `find_city()` sends `GET https://geocoding-api.open-meteo.com/v1/search?name=Gainesville&count=1`
2. `get_forecast()` sends `GET https://api.open-meteo.com/v1/forecast?latitude=29.65&longitude=-82.32&current=...`
3. `print_forecast()` digs the numbers out of the JSON

## Look for these patterns

Every API program you write will use them:

- `requests.get(url, params=..., timeout=10)` to make the request
- `response.raise_for_status()` to stop if the status code is an error
- `response.json()` to turn the body into Python dicts and lists
- `try / except requests.RequestException` so a network problem prints a message instead of a crash

## See the raw data

Paste these into your browser to see exactly what the code receives:

- https://geocoding-api.open-meteo.com/v1/search?name=Gainesville&count=1
- https://api.open-meteo.com/v1/forecast?latitude=29.65&longitude=-82.32&current=temperature_2m,weather_code&temperature_unit=fahrenheit

## Try changing it

- Add `relative_humidity_2m` to the `current` fields and print it.
- Change `forecast_days` to 7.
- Make it print in Celsius with a `--celsius` flag.
