import streamlit as st

# USER SEMENTARA (bisa kamu ganti)
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}


def login(username, password):

    if username in USERS and USERS[username]["password"] == password:
        return True, USERS[username]["role"]

    return False, None