# Exercise 1: Your first request

**Goal:** Ask PokéAPI about a Pokémon and print a few facts about it.

**You'll learn:** `GET`, status codes, and reading values out of JSON.

**API:** [PokéAPI](https://pokeapi.co/docs/v2#pokemon), no key needed.

## Step 0: look at the data first

Open this in your browser: https://pokeapi.co/api/v2/pokemon/pikachu

It's a lot! Use your browser's JSON viewer (Firefox has one built in; in Chrome, tick "Pretty-print"). Find:

- `name`
- `height` (in decimeters) and `weight` (in hectograms)
- `types`, a **list** of objects. The type name is at `types[0]["type"]["name"]`
- `stats`, a list of objects with `base_stat` and `stat.name`

Now try a Pokémon that doesn't exist: https://pokeapi.co/api/v2/pokemon/notapokemon. What happens?

## Step 1: fill in `starter.py`

```bash
python exercises/01-first-request/starter.py pikachu
```

Expected output:

```
PIKACHU (#25)
Height: 0.4 m
Weight: 6.0 kg
Types: electric
Stats:
  hp               35
  attack           55
  ...
```

and for a bad name:

```
$ python exercises/01-first-request/starter.py notapokemon
No Pokémon called 'notapokemon' (status 404)
```

## Hints

- `response.status_code` is a number like `200` or `404`.
- To turn a list of type objects into names: `[t["type"]["name"] for t in data["types"]]`
- Pokémon names in the URL must be lowercase.

## Bonus

- Print the URL of its picture: `data["sprites"]["front_default"]`. Open it in your browser.
- Print its abilities.
- Take two names and print which one has the higher total of base stats.
