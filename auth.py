import hashlib
import streamlit as st
from supabase import create_client, Client

# Inicializamos la conexión con Supabase usando los Secrets seguros
import hashlib
import streamlit as st
from supabase import create_client, Client

# 1. Definimos la variable vacía para evitar el "NameError"
supabase = None

# 2. Intentamos conectar e inyectamos un mensaje de error claro si falla
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    # Esto aparecerá arriba en tu app si Streamlit no encuentra el archivo
    st.error(f"Fallo crítico: No se pudo conectar a la base de datos. Motivo: {str(e)}")

# Admin password desde secrets
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
    ADMIN_PASSWORD_HASH = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
except Exception as e:
    ADMIN_PASSWORD_HASH = None

# Admin password desde secrets
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
    ADMIN_PASSWORD_HASH = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
except KeyError:
    st.error("Falta configurar ADMIN_PASSWORD en los secretos.")
    ADMIN_PASSWORD_HASH = None

def init_auth():
    # Ya no creamos carpetas ni archivos JSON locales
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

    # Consultamos a Supabase si el usuario ya existe
    try:
        response = supabase.table("users").select("username").eq("username", username).execute()
        if response.data:
            return False, "Ese nombre de usuario ya está en uso."
        
        # Si no existe, lo insertamos en la base de datos en la nube
        new_user = {
            "username": username,
            "password_hash": hash_password(password)
        }
        supabase.table("users").insert(new_user).execute()
        return True, "¡Registro exitoso!"
    except Exception as e:
        return False, f"Error al registrar: {str(e)}"

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

    # Buscamos el usuario en Supabase
    try:
        response = supabase.table("users").select("*").eq("username", username).execute()
        
        if not response.data:
            return False, "El usuario no existe."

        user_data = response.data[0]
        
        # Comparamos el hash de la contraseña ingresada con el de la base de datos
        if user_data["password_hash"] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_admin = False
            return True, "Login exitoso."
        
        return False, "Contraseña incorrecta."
    except Exception as e:
        return False, f"Error en el servidor: {str(e)}"

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.is_admin = False
    st.rerun()

def get_all_registered_users():
    try:
        response = supabase.table("users").select("username").execute()
        return [user["username"] for user in response.data]
    except:
        return []