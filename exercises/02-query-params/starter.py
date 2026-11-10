"""
Exercise 2: Query parameters. "Do I need an umbrella?"

Usage:
    python starter.py
"""

import requests

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Marston Library, more or less
GAINESVILLE = {"latitude": 29.65, "longitude": -82.32}


def get_rain_chances(latitude, longitude, hours=12):
    """Return a list of (time, percent) pairs for the next `hours` hours."""

    # TODO 1: Build a params dict with these keys:
    #   latitude, longitude, hourly="precipitation_probability",
    #   forecast_hours=hours, timezone="America/New_York"
    params = {}

    # TODO 2: GET FORECAST_URL with params=params and timeout=10,
    #         then call raise_for_status().
    response = None

    # TODO 3: Print response.url to see the URL requests built for you.

    # TODO 4: Get the JSON, then pull out data["hourly"]["time"] and
    #         data["hourly"]["precipitation_probability"].

    # TODO 5: Return them paired up: list(zip(times, chances))
    return []


def verdict(max_chance):
    """Turn the highest rain chance into advice."""
    if max_chance >= 60:
        return "Bring an umbrella. ☔"
    if max_chance >= 30:
        return "Maybe toss an umbrella in your bag. 🌂"
    return "You're good, leave it at home. 😎"


if __name__ == "__main__":
    pairs = get_rain_chances(GAINESVILLE["latitude"], GAINESVILLE["longitude"])

    print("\nRain chance in Gainesville, next 12 hours:")
    for time, chance in pairs:
        # time looks like "2026-11-10T14:00". The hour is everything after the "T".
        # TODO 6: Print the hour, the percent, and a little bar: "#" * (chance // 5)
        pass

    # TODO 7: Find the pair with the highest chance and print it, then print verdict().
    #         Hint: max(pairs, key=lambda pair: pair[1])
