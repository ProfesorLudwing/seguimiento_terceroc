import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Conexión central a la base de datos SQL de DBeaver
engine = create_engine("sqlite:///clase")

# 2. Menú de navegación lateral
st.sidebar.title("🎒 Panel Escolar 3°D")
opcion_pagina = st.sidebar.radio(
    "Selecciona la sección que deseas consultar:",
    ["📋 Seguimiento de Tareas", "📆 Alertas de Asistencia DGETI"]
)

# ==========================================
# PÁGINA 1: SEGUIMIENTO DE TAREAS
# ==========================================
if opcion_pagina == "📋 Seguimiento de Tareas":
    st.title("📊 Sistema de Seguimiento Académico")
    st.write("Portal oficial de entrega de actividades.")
    
    df_tareas = pd.read_sql("SELECT * FROM seguimiento", engine)
    alumno_sel = st.selectbox("Selecciona tu nombre:", df_tareas["nombre"].unique(), key="tareas_sel")
    
    datos_fil = df_tareas[df_tareas["nombre"] == alumno_sel]
    tabla_final = datos_fil[["tarea", "estado", "calificacion", "fecha_limite"]]
    
    st.subheader(f"Estado de entregas de: {alumno_sel}")
    st.table(tabla_final)

# ==========================================
# PÁGINA 2: CONTROL DE ASISTENCIAS DGETI
# ==========================================
elif opcion_pagina == "📆 Alertas de Asistencia DGETI":
    st.title("📆 Control de Horas de Clase y Asistencias")
    st.write("Conforme al reglamento de la DGETI, el 21% de inasistencias en horas acumuladas causa baja automática.")
    
    # Leer la tabla completa de asistencias de SQL (las 72 filas)
    df_asist = pd.read_sql("SELECT * FROM asistencias", engine)
    
    alumno_sel = st.selectbox("Selecciona tu nombre para verificar tu estatus:", df_asist["nombre"].unique(), key="asistencias_sel")
    
    # 🧮 FILTRADO ACUMULATIVO: Obtenemos todas las semanas que le pertenecen a ese alumno
    registros_alumno = df_asist[df_asist["nombre"] == alumno_sel]
    
    # 🧠 TRUCO DE CALIBRACIÓN: Rellenamos los vacíos de 'asis_max' en la memoria antes de sumar
    df_asist["asis_max"] = df_asist["asis_max"].ffill()
    maximos_limpios = df_asist[df_asist["nombre"] == alumno_sel]["asis_max"]

    # 🔄 SUMATORIA TOTAL DINÁMICA: Python calcula las horas de todas las semanas que han transcurrido
    horas_maximas_acumuladas = int(maximos_limpios.sum())
    horas_asistidas_totales = int(registros_alumno["asistencia"].sum())
    
    # Resta analítica sobre el total real del semestre transcurrido hasta hoy (16 horas actuales)
    horas_faltas_totales = horas_maximas_acumuladas - horas_asistidas_totales
    
    # Porcentaje de faltas real y calibrado (Faltas Totales / Horas Transcurridas Totales)
    porcentaje_faltas_real = (horas_faltas_totales / horas_maximas_acumuladas) * 100 if horas_maximas_acumuladas > 0 else 0
    
    # 📊 DESPLIEGUE VISUAL DE MÉTRICAS CALIBRADAS EN INTERNET
    st.subheader(f"Bitácora acumulada de: {alumno_sel}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="✅ Horas Asistidas Totales", value=f"{horas_asistidas_totales} de {horas_maximas_acumuladas} hrs")
    with col2:
        st.metric(label="❌ Faltas Totales Acumuladas", value=f"{horas_faltas_totales} hrs")
    with col3:
        st.metric(label="📊 Porcentaje Real de Faltas", value=f"{porcentaje_faltas_real:.1f}%")

    # 🚨 SEMÁFORO DE ALERTAS CALIBRADO DGETI
    if porcentaje_faltas_real >= 21:
        st.error(f"🔴 **ALERTA CRÍTICA:** Has alcanzado o superado el límite del {porcentaje_faltas_real:.1f}% de inasistencias acumuladas. Riesgo inminente de BAJA en el sistema DGETI.")
    elif porcentaje_faltas_real >= 15:
        st.warning(f"🟡 **ADVERTENCIA:** Tienes un {porcentaje_faltas_real:.1f}% de inasistencias acumuladas en horas. Estás muy cerca del límite permitido (21%).")
    else:
        st.success(f"🟢 **ESTATUS REGULAR:** Tu porcentaje de faltas es del {porcentaje_faltas_real:.1f}%. Te mantienes en situación aprobatoria.")

    # Mostrar el desglose completo de las columnas de fechas del Excel
    st.markdown("---")
    st.write("📅 **Historial completo de horas asistidas por día de clase:**")
    
    columnas_fechas = [c for c in df_asist.columns if "mayo" in c or "junio" in c or "de" in c]
    st.table(registros_alumno[columnas_fechas])
