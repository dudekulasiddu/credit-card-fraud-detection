import json
import os

# File where user info will be stored
USER_FILE = "users.json"

# Load users from the file
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

# Save users to the file
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Authenticate user during login
def authenticate_user(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

# Register new user during signup
def register_user(username, password, email):
    users = load_users()
    if username in users:
        return False  # user already exists
    users[username] = {
        "password": password,
        "email": email
    }
    save_users(users)
    return True
