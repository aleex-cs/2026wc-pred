# auth.py
import hashlib
import json
import os
import streamlit as st

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
# Admin password: qt5Xq6Lr5%
# Obtenemos la contraseña desde los secretos de Streamlit
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
    ADMIN_PASSWORD_HASH = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
except KeyError:
    # Por si se te olvida configurarlo, la app no crasheará y te avisará
    st.error("Falta configurar ADMIN_PASSWORD en los secretos.")
    ADMIN_PASSWORD_HASH = None

def init_auth():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.is_admin = False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    username = username.strip().lower()
    if not username or not password:
        return False, "Usuario o contraseña inválidos."
    if username == "admin":
        return False, "Nombre de usuario reservado."

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    if username in users:
        return False, "Ese nombre de usuario ya está en uso."

    users[username] = hash_password(password)

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f)

    return True, "¡Registro exitoso!"

def login_user(username, password):
    username = username.strip().lower()

    if username == "admin":
        if hash_password(password) == ADMIN_PASSWORD_HASH:
            st.session_state.logged_in = True
            st.session_state.username = "admin"
            st.session_state.is_admin = True
            return True, "Login exitoso como administrador."
        else:
            return False, "Contraseña incorrecta."

    if not os.path.exists(USERS_FILE):
        return False, "No hay usuarios registrados."

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    if username not in users:
        return False, "El usuario no existe."

    if users[username] == hash_password(password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.is_admin = False
        return True, "Login exitoso."

    return False, "Contraseña incorrecta."

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.is_admin = False
    st.rerun()

def get_all_registered_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    return list(users.keys())
