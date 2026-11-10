"""
Exercise 1: Your first request.

Usage:
    python starter.py pikachu
"""

import sys

import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon(name):
    """Return the Pokémon's data as a dict, or None if it doesn't exist."""
    url = BASE_URL + name.lower()

    # TODO 1: Send a GET request to `url` with requests.get(). Use timeout=10.
    response = None

    # TODO 2: If the status code is 404, print a friendly message and return None.
    #         e.g. No Pokémon called 'notapokemon' (status 404)

    # TODO 3: For any other error status, call response.raise_for_status().

    # TODO 4: Return the JSON body as a Python dict.
    return None


def print_pokemon(data):
    """Print a few facts from the Pokémon's data."""
    # TODO 5: Print the name in CAPITALS and its id, e.g. PIKACHU (#25)

    # TODO 6: Print height in meters and weight in kg.
    #         height is in decimeters (divide by 10), weight is in hectograms (divide by 10).

    # TODO 7: Print its types, comma separated. Each item in data["types"]
    #         looks like {"slot": 1, "type": {"name": "electric", "url": "..."}}

    # TODO 8: Print each stat name and its base_stat. Each item in data["stats"]
    #         looks like {"base_stat": 35, "stat": {"name": "hp", "url": "..."}}
    pass


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "pikachu"
    pokemon = get_pokemon(name)
    if pokemon:
        print_pokemon(pokemon)
