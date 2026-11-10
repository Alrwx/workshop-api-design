"""
Exercise 2 solution. "Do I need an umbrella?"

Usage:
    python solution.py
"""

import requests

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Marston Library, more or less
GAINESVILLE = {"latitude": 29.65, "longitude": -82.32}


def get_rain_chances(latitude, longitude, hours=12):
    """Return a list of (time, percent) pairs for the next `hours` hours."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation_probability",
        "forecast_hours": hours,
        "timezone": "America/New_York",
    }
    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()
    print(f"Asked: {response.url}")

    data = response.json()
    times = data["hourly"]["time"]
    chances = data["hourly"]["precipitation_probability"]
    # Replace any missing values (null in JSON, None in Python) with 0
    chances = [c if c is not None else 0 for c in chances]
    return list(zip(times, chances))


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
        hour = time.split("T")[1]
        print(f"  {hour}  {chance:>3}% {'#' * (chance // 5)}")

    worst_time, worst_chance = max(pairs, key=lambda pair: pair[1])
    print(f"Highest chance: {worst_chance}% at {worst_time.split('T')[1]}")
    print(f"Verdict: {verdict(worst_chance)}")
