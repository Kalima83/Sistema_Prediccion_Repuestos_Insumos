import streamlit as st

# Base de usuarios (En producción se reemplaza por consulta al Backend / DB)
USUARIOS_PERMITIDOS = {
    "admin": "admin123",
    "supervisor": "mantenimiento2026",
    "revisor1": "control2026"
}

def inicializar_estado_auth():
    """Asegura que las variables de sesión existan."""
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if "usuario_actual" not in st.session_state:
        st.session_state.usuario_actual = ""

def verificar_credenciales(usuario, contrasena) -> bool:
    """Valida las credenciales contra el diccionario o servicio."""
    return USUARIOS_PERMITIDOS.get(usuario) == contrasena

def login_form() -> bool:
    """Muestra el formulario de inicio de sesión y gestiona el acceso."""
    inicializar_estado_auth()

    if st.session_state.autenticado:
        return True

    st.subheader("🔐 Acceso Restringido - Personal Revisor")
    
    with st.form("form_login"):
        user_input = st.text_input("Usuario")
        pass_input = st.text_input("Contraseña", type="password")
        btn_submit = st.form_submit_button("Ingresar al Panel de Gestión", width="stretch")

        if btn_submit:
            if verificar_credenciales(user_input, pass_input):
                st.session_state.autenticado = True
                st.session_state.usuario_actual = user_input
                st.success("Acceso concedido.")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

    return False

def logout_button():
    """Muestra el usuario activo y botón para cerrar sesión en la barra lateral."""
    inicializar_estado_auth()
    if st.session_state.autenticado:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"👤 **Usuario:** `{st.session_state.usuario_actual}`")
        if st.sidebar.button("🚪 Cerrar Sesión", width="stretch"):
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.rerun()