import os
import streamlit as st
from auth import login_form, logout_button

# 1. Configuración global de la página (DEBE SER LA PRIMERA INSTRUCCIÓN DE STREAMLIT)
st.set_page_config(
    page_title="Sistema Logístico 601 - Mantenimiento de Electrónica",
    page_icon="⚙️",
    layout="wide"
)

# --- CONTROL DE RUTAS ABSOLUTAS Y RECURSOS ---
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
IRECTORIO_ACTUDAL = os.path.dirname(os.path.abspath(__file__))
RUTA_LOGO = os.path.join(DIRECTORIO_ACTUAL, "assets", "escudo_bmant.webp")
RUTA_FONDO = os.path.join(DIRECTORIO_ACTUAL, "assets", "fondo_bamant.webp")



# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    /* Fondo general claro */
    .stApp {
        background-color: #f4f6f9;
    }
    /* Contenedor principal estilizado como tarjeta */
    .block-container {
        background-color: #ffffff;
        padding: 2rem 2.5rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Importación diferida de vistas
from views import consulta_FE, reparacion_FE, revision_FE

def main():
    # --- BARRA LATERAL (SIDEBAR) INSTITUCIONAL ---
    with st.sidebar:
        # 1. Logo institucional
        if os.path.exists(RUTA_LOGO):
            st.image(RUTA_LOGO, width=140)
        else:
            st.title("🛡️")
        
        # 2. Título institucional
        st.title("Sistema de Mantenimiento de Electrónica IA")
        st.caption("Batallón de Mantenimiento de Comunicaciones 601 - DGCICD")
        st.info("Asistente interactivo para gestión de solicitudes y consultas referentes a los efectos de electrónica del Ejército Argentino.")
        
        st.markdown("---")
        
        # 3. Menú de Navegación Principal
        opcion_menu = st.radio(
            "Seleccioná el Módulo:",
            ["📝 Portal Solicitante (Carga/Consulta)", "🔒 Panel de Control (Revisores)"]
        )

    # --- CUERPO PRINCIPAL ---

    # 1. MÓDULO: PORTAL SOLICITANTE
    if opcion_menu == "📝 Portal Solicitante (Carga/Consulta)":
        # La imagen de cabecera SOLO se imprime aquí (una sola vez)
        if os.path.exists(RUTA_FONDO):
            st.image(RUTA_FONDO, use_container_width=True)

        st.subheader("⚙️ Portal Logístico de Mantenimiento de Electrónica")
        st.markdown("---")

        # Pestañas para dividir Consulta y Nueva Carga
        tab_consulta, tab_reparacion = st.tabs(["🔍 Consulta Técnica IA", "📝 Nueva Solicitud de Reparación"])

        with tab_consulta:
            consulta_FE.mostrar_interfaz()

        with tab_reparacion:
            reparacion_FE.mostrar_interfaz()

    # 2. MÓDULO: PANEL DE CONTROL REVISORES
    elif opcion_menu == "🔒 Panel de Control (Revisores)":
        # Sin imagen de fondo para mantener el panel directo y despejado
        if login_form():
            logout_button()
            revision_FE.mostrar_interfaz_revisor()

if __name__ == "__main__":
    main()