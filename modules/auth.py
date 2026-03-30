import streamlit as st

# =====================
# USERS
# =====================
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "user1": {
        "password": "user123",
        "role": "user"
    }
}

# =====================
# ROLE PERMISSIONS
# =====================
ROLE_PERMISSIONS = {
    "admin": [
        "view_dashboard",
        "view_data",
        "crud_master",
        "crud_qc",
        "crud_km",
        "delete"
    ],
    "user": [
        "view_dashboard",
        "view_data"
    ]
}

# =====================
# LOGIN
# =====================
def login(username, password):

    user = USERS.get(username)

    if user and user["password"] == password:
        return True, user["role"]

    return False, None


# =====================
# CHECK PERMISSION
# =====================
def has_permission(permission):

    role = st.session_state.get("role")

    if not role:
        return False

    return permission in ROLE_PERMISSIONS.get(role, [])