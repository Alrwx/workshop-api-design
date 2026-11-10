"""
Exercise 3 solution.

Usage:
    python solution.py
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# Tell the server who we are. Lots of APIs ask you to do this.
HEADERS = {"User-Agent": "uf-acm-api-workshop"}


def list_todos(user_id):
    """GET all of one user's to-dos."""
    response = requests.get(
        f"{BASE_URL}/todos", params={"userId": user_id}, headers=HEADERS, timeout=10
    )
    response.raise_for_status()
    print(f"Server says it's sending: {response.headers['Content-Type']}")
    return response.json()


def create_todo(title, user_id):
    """POST a new to-do. Returns the server's response JSON."""
    new_todo = {"title": title, "completed": False, "userId": user_id}
    response = requests.post(f"{BASE_URL}/todos", json=new_todo, headers=HEADERS, timeout=10)
    response.raise_for_status()
    print(f"\nCreated (status {response.status_code})")
    return response.json()


def mark_done(todo_id):
    """PATCH a to-do so completed is True."""
    response = requests.patch(
        f"{BASE_URL}/todos/{todo_id}", json={"completed": True}, headers=HEADERS, timeout=10
    )
    response.raise_for_status()
    print(f"Updated (status {response.status_code})")
    return response.json()


if __name__ == "__main__":
    todos = list_todos(1)

    done = [t for t in todos if t["completed"]]
    print(f"User 1 has {len(todos)} to-dos, {len(done)} done.")
    print("Not done yet:")
    for t in todos:
        if not t["completed"]:
            print(f"  [ ] {t['title']}")

    created = create_todo("Go to the ACM API workshop", 1)
    print(created)

    updated = mark_done(1)
    print(updated)
