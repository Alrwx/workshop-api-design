"""
Gator Forecast: a complete, working API program.

Run it:
    python 00-working-example/gator_forecast.py
    python 00-working-example/gator_forecast.py --city Miami

What it does:
    1. Asks a geocoding API "where is this city?" (city name -> latitude/longitude)
    2. Asks a weather API "what's the weather there?" (latitude/longitude -> forecast)
    3. Prints it nicely

Both APIs are from https://open-meteo.com and need no API key.
Read this top to bottom: every step is commented. The exercises
ask you to write each of these pieces yourself.
"""

import argparse
import sys

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo returns a number for the weather ("weather code"). This turns it into words.
# Full list: https://open-meteo.com/en/docs (scroll to "WMO Weather interpretation codes")
WEATHER_CODES = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Fog 🌫️",
    48: "Fog 🌫️",
    51: "Light drizzle 🌦️",
    53: "Drizzle 🌦️",
    55: "Heavy drizzle 🌧️",
    61: "Light rain 🌧️",
    63: "Rain 🌧️",
    65: "Heavy rain 🌧️",
    80: "Rain showers 🌦️",
    81: "Rain showers 🌧️",
    82: "Violent rain showers ⛈️",
    95: "Thunderstorm ⛈️",
    96: "Thunderstorm with hail ⛈️",
    99: "Thunderstorm with hail ⛈️",
}


def find_city(name):
    """Step 1: turn a city name into coordinates using the geocoding API."""
    # Query params go in a dict. requests builds "?name=Gainesville&count=1" for us.
    params = {"name": name, "count": 1, "country_code": "US"}

    # Always set a timeout so a slow server can't freeze your program.
    response = requests.get(GEOCODING_URL, params=params, timeout=10)

    # If the status code is 4xx or 5xx, this raises an error instead of
    # letting us continue with bad data.
    response.raise_for_status()

    # The body is JSON. .json() turns it into Python dicts and lists.
    data = response.json()

    # This API leaves out "results" entirely when nothing matches.
    if not data.get("results"):
        return None

    place = data["results"][0]
    return {
        "name": place["name"],
        "state": place.get("admin1", ""),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
    }


def get_forecast(latitude, longitude):
    """Step 2: get current weather and a 3-day forecast for a location."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        # Ask only for the fields we need. Lists become "a,b,c" in the URL.
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "America/New_York",
        "forecast_days": 3,
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def print_forecast(city, forecast):
    """Step 3: pull the pieces we want out of the JSON and print them."""
    current = forecast["current"]
    daily = forecast["daily"]

    print(f"\n🐊 Weather for {city['name']}, {city['state']}")
    print("-" * 40)
    print(f"Right now: {current['temperature_2m']}°F "
          f"(feels like {current['apparent_temperature']}°F)")
    print(f"           {WEATHER_CODES.get(current['weather_code'], 'Unknown')}")
    print(f"           Wind {current['wind_speed_10m']} mph")
    print("\nNext 3 days:")

    # "daily" is a dict of parallel lists: daily["time"][0] goes with
    # daily["temperature_2m_max"][0], and so on. zip() walks them together.
    for day, code, high, low, rain in zip(
        daily["time"],
        daily["weather_code"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["precipitation_probability_max"],
    ):
        rain = "?" if rain is None else rain  # APIs sometimes send null for missing data
        print(f"  {day}  {low:>5.1f}°F to {high:>5.1f}°F  "
              f"{rain:>3}% rain  {WEATHER_CODES.get(code, 'Unknown')}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Get the weather for a US city.")
    parser.add_argument("--city", default="Gainesville", help="City name (default: Gainesville)")
    args = parser.parse_args()

    try:
        city = find_city(args.city)
        if city is None:
            print(f"Couldn't find a city called {args.city!r}.")
            sys.exit(1)
        forecast = get_forecast(city["latitude"], city["longitude"])
    except requests.RequestException as error:
        # Covers no internet, timeouts, and 4xx/5xx from raise_for_status().
        print(f"Something went wrong talking to the API: {error}")
        sys.exit(1)

    print_forecast(city, forecast)


if __name__ == "__main__":
    main()
