import streamlit as st
import requests

def mostrar_interfaz_revisor():
    st.title("🎛️ Centro de Control y Asignación de Taller")

    try:
        res = requests.get("http://127.0.0.1:8000/reparacion/solicitudes")
        solicitudes = res.json() if res.status_code == 200 else []
    except Exception:
        st.error("No se pudo conectar con el servidor.")
        solicitudes = []

    if not solicitudes:
        st.info("No existen solicitudes en la base de datos.")
        return

    # MÉTRICAS DEL SUPERVISOR GENERAL
    total = len(solicitudes)
    sin_asignar = sum(1 for s in solicitudes if s.get("operador_asignado") == "Sin Asignar")
    en_proceso = sum(1 for s in solicitudes if s.get("estado") == "En Proceso")
    cerrados = sum(1 for s in solicitudes if s.get("estado") == "Cerrado")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", total)
    col2.metric("⚠️ Sin Operario Asignado", sin_asignar, delta_color="inverse")
    col3.metric("En Taller", en_proceso)
    col4.metric("Resueltos", cerrados)

    st.markdown("---")

    # Filtros para el Supervisor
    filtro_op = st.selectbox(
        "Filtrar lista por asignación:",
        ["Todos los Tickets", "⚠️ Solo Sin Operario Asignado", "En Proceso / Asignados"]
    )

    tickets_filtrados = solicitudes
    if filtro_op == "⚠️ Solo Sin Operario Asignado":
        tickets_filtrados = [s for s in solicitudes if s.get("operador_asignado") == "Sin Asignar"]
    elif filtro_op == "En Proceso / Asignados":
        tickets_filtrados = [s for s in solicitudes if s.get("operador_asignado") != "Sin Asignar"]

    for tk in tickets_filtrados:
        nro_ctl = tk.get("nro_control")
        operario = tk.get("operador_asignado", "Sin Asignar")
        estado = tk.get("estado", "Pendiente")

        alerta_icono = "🔴" if operario == "Sin Asignar" else "🟢"
        
        with st.expander(f"{alerta_icono} Ticket **{nro_ctl}** | Operario: **{operario}** | Estado: **{estado}**"):
            c1, c2 = st.columns([2, 1])

            with c1:
                st.write(f"**Unidad:** {tk.get('unidad_nombre')}")
                st.write(f"**Equipo:** {tk.get('equipo_nombre')}")
                # Muestra la falla (ej: Roto)
                st.write(f"**Tipo de Falla:** {tk.get('falla_tipo')}")  
                st.write(f"**Fecha Registro:** {tk.get('fecha_creacion')}")
                # Muestra el detalle procesado por IA
                st.write(f"**Descripción de la Falla:** {tk.get('descripcion_procesada')}")    
            

            with c2:
                st.subheader("Asignación de Gestión")
                
                taller_sel = st.selectbox(
                    "Taller / Laboratorio",
                    ["Compania Manteniemiento A", "Compania de Mantenimiento B", "Compania Modernización"],
                    key=f"tal_{nro_ctl}"
                )

                operador_input = st.text_input(
                    "Asignar a Operario / Técnico:", 
                    value="" if operario == "Sin Asignar" else operario,
                    placeholder="Ej: CB Perez",
                    key=f"op_{nro_ctl}"
                )

                estado_sel = st.selectbox(
                    "Estado del Ticket",
                    ["Pendiente", "En Proceso", "Cerrado"],
                    index=0 if estado == "Pendiente" else (1 if estado == "En Proceso" else 2),
                    key=f"est_{nro_ctl}"
                )

                if st.button("Guardar / Asignar Operario", key=f"btn_{nro_ctl}", type="primary", width="stretch"):
                    op_final = operador_input.strip() if operador_input.strip() else "Sin Asignar"
                    payload = {
                        "nro_control": nro_ctl,
                        "taller_asignado": taller_sel,
                        "operador_asignado": op_final,
                        "estado": estado_sel
                    }
                    res_upd = requests.put("http://127.0.0.1:8000/reparacion/solicitud/asignar", json=payload)
                    if res_upd.status_code == 200:
                        st.success(f"Ticket {nro_ctl} actualizado.")
                        st.rerun()
                    else:
                        st.error("Error al actualizar la asignación.")