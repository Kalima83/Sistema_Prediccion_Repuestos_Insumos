import streamlit as st
import requests

def mostrar_interfaz():
    # Título original de tu diseño
    st.subheader("Nueva Solicitud de Mantenimiento")
    st.write("Cargá los datos del equipo seleccionando desde los catálogos oficiales para validar la unidad y generar tu Número de Control.")

    # 1. Traer datos desde el Backend (Tus archivos de Excel)
    try:
        unidades = requests.get("http://127.0.0.1:8000/reparacion/unidades").json()
        equipos = requests.get("http://127.0.0.1:8000/reparacion/equipos").json()
        fallas = requests.get("http://127.0.0.1:8000/reparacion/fallas").json()
    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar al Backend. Asegurate de que Uvicorn esté corriendo.")
        unidades, equipos, fallas = ["Error"], ["Error"], ["Error"]

    # 2. Formulario Estructurado (Selectboxes en lugar de texto libre)
    col1, col2 = st.columns(2)
    with col1:
        unidad_sel = st.selectbox("Unidad Solicitante", unidades)
    with col2:
        equipo_sel = st.selectbox("Equipo / Efecto", equipos)
    
    falla_sel = st.selectbox("Código de Falla Estándar", fallas)

    st.markdown("---")

    # 3. Traductor IA (Human-in-the-loop)
    st.write("**Descripción de la Falla**")
    descripcion_libre = st.text_area("Describa el problema (Texto Libre):", 
                                     placeholder="Ej: El equipo TRAN HARRIS HF RF tiene el ROE alto y se apaga...")

    if "traduccion_confirmada" not in st.session_state:
        st.session_state.traduccion_confirmada = False
        st.session_state.texto_traducido = ""

    if st.button("Procesar Descripción Técnica"):
        if descripcion_libre:
            with st.spinner("Procesando con IA..."):
                res = requests.post("http://127.0.0.1:8000/reparacion/traducir_falla", json={"texto_libre": descripcion_libre})
                if res.status_code == 200:
                    st.session_state.texto_traducido = res.json()["texto_traducido"]
                    st.session_state.traduccion_confirmada = True
        else:
            st.warning("Escribí una descripción antes de procesar.")

    # 4. Confirmación y Guardado Final
    if st.session_state.traduccion_confirmada:
        st.warning("⚠️ Revisá la sugerencia técnica antes de registrar:")
        st.info(st.session_state.texto_traducido)
        
        # Botón original de tu diseño
        if st.button("Registrar Solicitud", type="primary"):
            payload = {
                "unidad": unidad_sel,
                "equipo": equipo_sel,
                "codigo_falla": falla_sel,
                "descripcion_procesada": st.session_state.texto_traducido
            }
            res_guardar = requests.post("http://127.0.0.1:8000/reparacion/solicitud", json=payload)
            if res_guardar.status_code == 200:
                data_res = res_guardar.json()
                st.success(f"¡Solicitud guardada con éxito! Nro de Control: **{data_res['nro_control']}**")
                st.session_state.traduccion_confirmada = False