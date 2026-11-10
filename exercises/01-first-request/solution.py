"""
Exercise 1 solution.

Usage:
    python solution.py pikachu
"""

import sys

import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon(name):
    """Return the Pokémon's data as a dict, or None if it doesn't exist."""
    url = BASE_URL + name.lower()
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        print(f"No Pokémon called {name!r} (status 404)")
        return None

    response.raise_for_status()
    return response.json()


def print_pokemon(data):
    """Print a few facts from the Pokémon's data."""
    print(f"{data['name'].upper()} (#{data['id']})")
    print(f"Height: {data['height'] / 10} m")
    print(f"Weight: {data['weight'] / 10} kg")

    types = [t["type"]["name"] for t in data["types"]]
    print(f"Types: {', '.join(types)}")

    print("Stats:")
    for s in data["stats"]:
        print(f"  {s['stat']['name']:<16} {s['base_stat']}")

    # Bonus
    print(f"Picture: {data['sprites']['front_default']}")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "pikachu"
    pokemon = get_pokemon(name)
    if pokemon:
        print_pokemon(pokemon)
