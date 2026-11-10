"""
Exercise 3: Sending data with POST and PATCH.

Usage:
    python starter.py
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# Tell the server who we are. Lots of APIs ask you to do this.
HEADERS = {"User-Agent": "uf-acm-api-workshop"}


def list_todos(user_id):
    """GET all of one user's to-dos."""
    # TODO 1: GET f"{BASE_URL}/todos" with params={"userId": user_id},
    #         headers=HEADERS and timeout=10. Call raise_for_status().
    response = None

    # TODO 2: Print the Content-Type header the server sent back.

    # TODO 3: Return the JSON (a list of dicts).
    return []


def create_todo(title, user_id):
    """POST a new to-do. Returns the server's response JSON."""
    new_todo = {"title": title, "completed": False, "userId": user_id}

    # TODO 4: POST to f"{BASE_URL}/todos" with json=new_todo, headers=HEADERS, timeout=10.
    response = None

    # TODO 5: Print f"\nCreated (status {response.status_code})" (should be 201)
    #         and return the JSON.
    return {}


def mark_done(todo_id):
    """PATCH a to-do so completed is True."""
    # TODO 6: PATCH f"{BASE_URL}/todos/{todo_id}" with json={"completed": True}.
    #         Use requests.patch(). Print f"Updated (status {response.status_code})"
    #         and return the JSON.
    return {}


if __name__ == "__main__":
    todos = list_todos(1)

    # TODO 7: Count how many are done (todo["completed"] is True), print
    #         "User 1 has X to-dos, Y done.", then list the ones not done yet.

    created = create_todo("Go to the ACM API workshop", 1)
    print(created)

    updated = mark_done(1)
    print(updated)
