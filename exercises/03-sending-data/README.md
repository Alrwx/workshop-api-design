# Exercise 3: Sending data

**Goal:** Use a to-do list API. Read a user's to-dos, then create a new one and mark it done.

**You'll learn:** `POST` and `PATCH`, sending a JSON body, `201 Created`, and headers.

**API:** [JSONPlaceholder](https://jsonplaceholder.typicode.com/guide/), a fake API for practice. No key needed.

> JSONPlaceholder **pretends** to save your changes. It answers exactly like a real API would, but nothing is actually stored, so you can't break anything.

## The endpoints

| Method | URL | What it does |
| --- | --- | --- |
| `GET` | `/todos?userId=1` | List user 1's to-dos |
| `GET` | `/todos/5` | Get to-do #5 |
| `POST` | `/todos` | Create a to-do (send JSON in the body) |
| `PATCH` | `/todos/5` | Change some fields of to-do #5 |
| `DELETE` | `/todos/5` | Delete to-do #5 |

Base URL: `https://jsonplaceholder.typicode.com`

## Step 0: POST from the terminal

You can't send a POST by typing in the browser bar, but `curl` can:

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish COP3530 project", "completed": false, "userId": 1}'
```

Look at the first line of the reply: `HTTP/2 201`. **201 means Created.** The body echoes your to-do back with a new `id`.

## Step 1: fill in `starter.py`

```bash
python exercises/03-sending-data/starter.py
```

Expected output:

```
Server says it's sending: application/json; charset=utf-8
User 1 has 20 to-dos, 11 done.
Not done yet:
  [ ] delectus aut autem
  ...

Created (status 201)
{'title': 'Go to the ACM API workshop', 'completed': False, 'userId': 1, 'id': 201}
Updated (status 200)
{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': True}
```

## Hints

- `requests.post(url, json=my_dict)` turns your dict into JSON **and** sets the `Content-Type: application/json` header for you.
- Response headers are in `response.headers`, which works like a dict: `response.headers["Content-Type"]`.
- You can send your own headers with `headers={"User-Agent": "acm-workshop"}`.

## Bonus

- Delete a to-do and print the status code.
- Try `GET /todos/9999`. What status do you get?
- Use `GET /users/1` to print the user's name above their to-dos.
