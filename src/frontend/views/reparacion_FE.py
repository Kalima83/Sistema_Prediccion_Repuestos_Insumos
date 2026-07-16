import streamlit as st
import requests

def mostrar_interfaz():
    st.subheader("📝 Nueva Solicitud de Mantenimiento")
    st.write("Completá los datos del equipo y describí el problema. Al presionar 'Procesar Descripción Técnica', se generará el borrador oficial para su revisión.")

    # 1. Traer datos estructurados desde el Backend
    try:
        unidades_raw = requests.get("http://127.0.0.1:8000/reparacion/unidades").json()
        equipos_raw = requests.get("http://127.0.0.1:8000/reparacion/equipos").json()
        fallas_raw = requests.get("http://127.0.0.1:8000/reparacion/fallas").json()
    except Exception:
        st.error("No se pudo conectar al Backend. Asegurate de que Uvicorn esté encendido.")
        unidades_raw, equipos_raw, fallas_raw = [], [], []

    # Mapeos para los selectbox
    dict_unidades = {u["nombre"]: u for u in unidades_raw if "nombre" in u} if unidades_raw else {}
    dict_equipos = {e["nombre"]: e for e in equipos_raw if "nombre" in e} if equipos_raw else {}
    dict_fallas = {f["tipo_falla"]: f for f in fallas_raw if "tipo_falla" in f} if fallas_raw else {}

    # 2. Formulario en Pantalla con Placeholders Militares
    col1, col2 = st.columns(2)
    with col1:
        unidad_nombre_sel = st.selectbox(
            "Unidad Solicitante *", 
            options=list(dict_unidades.keys()),
            index=None, 
            placeholder="Ej: COMPAÑIA DE COMUNICACIONES MECANIZADA 10"
        )
        unidad_info = dict_unidades.get(unidad_nombre_sel) if unidad_nombre_sel else None
    
    with col2:
        equipo_nombre_sel = st.selectbox(
            "Equipo / Efecto (INE) *", 
            options=list(dict_equipos.keys()),
            index=None,
            placeholder="Ej: TRAN HARRIS HF RF"
        )
        equipo_info = dict_equipos.get(equipo_nombre_sel) if equipo_nombre_sel else None

    col_nne, col_ni = st.columns(2)
    with col_nne:
        nne_mostrar = equipo_info["nne"] if equipo_info else ""
        st.text_input("Número Nacional de Efecto (NNE)", value=nne_mostrar, disabled=True, placeholder="Se autocompleta con el equipo")
    with col_ni:
        ni_usuario = st.text_input("Número de Identificación (NI) del equipo", placeholder="Ej: NI-4500")

    falla_tipo_sel = st.selectbox(
        "Descripción de la Falla Estándar *", 
        options=list(dict_fallas.keys()),
        index=None,
        placeholder="Ej: Falla de potencia de salida (255)"
    )
    falla_info = dict_fallas.get(falla_tipo_sel) if falla_tipo_sel else None

    st.markdown("---")

    # 3. Procesador IA de Texto Libre
    st.write("**Descripción Detallada de la Falla**")
    descripcion_libre = st.text_area(
        "Describa detalladamente el problema: *", 
        placeholder="Ej: El transceptor presenta ROE alto en la banda de HF..."
    )

    # Control de estados en Streamlit
    if "traduccion_confirmada" not in st.session_state:
        st.session_state.traduccion_confirmada = False
        st.session_state.texto_traducido = ""

    # Botón para Procesar
    if st.button("Procesar Descripción Técnica con IA", width="stretch"):
        # Validación de campos obligatorios antes de procesar
        if not unidad_info:
            st.error("Por favor, seleccione una Unidad Solicitante.")
        elif not equipo_info:
            st.error("Por favor, seleccione un Equipo o Efecto (INE).")
        elif not falla_info:
            st.error("Por favor, seleccione un código de Falla Estándar.")
        elif not descripcion_libre.strip():
            st.warning("Escribí una descripción detallada antes de procesar.")
        else:
            with st.spinner("Procesando con IA..."):
                try:
                    res = requests.post("http://127.0.0.1:8000/reparacion/traducir_falla", json={"texto_libre": descripcion_libre})
                    if res.status_code == 200:
                        st.session_state.texto_traducido = res.json()["texto_traducido"]
                        st.session_state.traduccion_confirmada = True
                    else:
                        st.error("Hubo un problema al conectar con el motor de IA.")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
# 4. MUESTRA EL TICKET Y OPCIONES DE ACEPTAR/CANCELAR SÓLO SI SE PROCESÓ CON ÉXITO
    if st.session_state.traduccion_confirmada and unidad_info and equipo_info and falla_info:
        st.markdown("---")
        st.subheader("📋 Previsualización del Ticket de Control")
        
        # Datos finales limpios
        unidad_abrev_vis = f"<b>{unidad_info['abreviatura']}</b>"
        unidad_cod_vis = f"<b>{unidad_info['codigo']}</b>"
        unidad_nom_vis = f"<b>{unidad_info['nombre']}</b>"
        equipo_nom_vis = f"<b>{equipo_info['nombre']}</b>"
        equipo_nne_vis = f"<b>{equipo_info['nne']}</b>"
        ni_visual = f"<b>{ni_usuario}</b>" if ni_usuario.strip() else "<b>S/NI</b>"
        falla_tipo_vis = f"{falla_info['tipo_falla']}"
        falla_cod_vis = f"{falla_info['codigo_falla']}"
        descripcion_visual = f"<b>{st.session_state.texto_traducido}</b>"

        # Maquetado del Ticket de Control definitivo (Comillas triples perfectamente alineadas)
        ticket_html = f"""<div style="border: 2px dashed #0E8388; padding: 22px; border-radius: 8px; background-color: #f9fbfb; font-family: monospace; color: #2C3E50;">
<h4 style="text-align: center; margin-top: 0; color: #0E8388; letter-spacing: 1px; font-weight: bold;">SOLICITUD DE MANTENIMIENTO DE ELECTRÓNICA</h4>
<hr style="border-top: 1px dashed #0E8388;">
<p><b>NRO DE SOLICITUD:</b> 26/0001 <span style="color: #E74C3C; font-weight: bold; font-size: 0.85em;">[BORRADOR REVISIÓN]</span></p>
<p><b>UNIDAD SOLICITANTE:</b> {unidad_abrev_vis} | <b>CÓDIGO:</b> {unidad_cod_vis}</p>
<p><b>NOMBRE UNIDAD:</b> {unidad_nom_vis}</p>
<hr style="border-top: 1px dashed #0E8388;">
<p><b>DATOS DEL EQUIPO:</b></p>
<ul style="margin-top: 5px;">
<li><b>Efecto (INE):</b> {equipo_nom_vis}</li>
<li><b>NNE:</b> {equipo_nne_vis}</li>
<li><b>NI (Identificación):</b> {ni_visual}</li>
</ul>
<hr style="border-top: 1px dashed #0E8388;">
<p><b>BLOQUE DE FALLA:</b></p>
<p style="margin-left: 15px;"><b>Tipo de Falla:</b> {falla_tipo_vis}</p>
<p style="margin-left: 15px;"><b>Código Asociado:</b> <span style="background-color: #EAECEE; padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #2C3E50;">{falla_cod_vis}</span></p>
<hr style="border-top: 1px dashed #0E8388;">
<p><b>DESCRIPCIÓN TÉCNICA (IA):</b><br>{descripcion_visual}</p>
</div>"""

        st.markdown(ticket_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Botones de Aceptar o Cancelar distribuidos de forma horizontal
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("Confirmar y Dar de Alta Solicitud", type="primary", width="stretch"):
                payload = {
                    "unidad_nombre": unidad_info["nombre"],
                    "unidad_abreviatura": unidad_info["abreviatura"],
                    "unidad_codigo": str(unidad_info["codigo"]),
                    "equipo_nombre": equipo_info["nombre"],
                    "equipo_nne": str(equipo_info["nne"]),
                    "equipo_ni": ni_usuario if ni_usuario.strip() else "S/NI",
                    "falla_tipo": falla_info["tipo_falla"],
                    "falla_codigo": str(falla_info["codigo_falla"]),
                    "descripcion_procesada": st.session_state.texto_traducido
                }
                
                try:
                    res_guardar = requests.post("http://127.0.0.1:8000/reparacion/solicitud", json=payload)
                    if res_guardar.status_code == 200:
                        data_res = res_guardar.json()
                        st.balloons()
                        st.success(f"¡Solicitud registrada con éxito! Número de Control oficial asignado: **{data_res['nro_control']}**")
                        
                        # Reseteamos el estado para una nueva carga limpia
                        st.session_state.traduccion_confirmada = False
                        st.session_state.texto_traducido = ""
                        st.rerun()
                    else:
                        st.error(f"Error {res_guardar.status_code} en el servidor: {res_guardar.text}")
                except Exception as e:
                    st.error(f"Error de conexión con el servidor backend: {e}")

        with btn_col2:
            if st.button("Cancelar / Modificar Borrador", type="secondary", width="stretch"):
                # Limpiamos el procesamiento para volver al formulario sin ticket en pantalla
                st.session_state.traduccion_confirmada = False
                st.session_state.texto_traducido = ""
                st.warning("Borrador cancelado. Puede corregir los datos arriba y volver a procesar.")
                st.rerun()