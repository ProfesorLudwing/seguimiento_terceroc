import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Conexión central a la base de datos SQL de DBeaver
engine = create_engine("sqlite:///clase")

# 2. Menú de navegación lateral para dividir la aplicación
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
    st.write("Conforme al reglamento de la DGETI, alcanzar el 21% de inasistencias en horas causa baja automática.")
    
    # Leer la nueva tabla de asistencias de SQL
    df_asist = pd.read_sql("SELECT * FROM asistencias", engine)
    
    # 🧠 TRUCO DE INGENIERÍA DE DATOS: Python toma el '8' de la primera celda de 'asis_max'
    # e imagina que se repite en todas las filas vacías para corregir las faltas en internet
    horas_maximas_semana = int(df_asist["asis_max"].dropna().iloc[0])
    
    alumno_sel = st.selectbox("Selecciona tu nombre para verificar tu estatus:", df_asist["nombre"].unique(), key="asistencias_sel")
    
    # Filtrar el renglón del alumno seleccionado
    datos_alumno = df_asist[df_asist["nombre"] == alumno_sel].iloc[0]
    
    # Extraer el total de asistencias en horas registradas por el alumno
    horas_asistidas = int(datos_alumno["asistencia"])
    
    # 🧮 CORRECCIÓN MATEMÁTICA: Python hace la resta real (8 - Asistencias) en el servidor
    horas_faltas = horas_maximas_semana - horas_asistidas
    
    # Calcular el porcentaje de faltas acumulado real
    porcentaje_faltas = (horas_faltas / horas_maximas_semana) * 100 if horas_maximas_semana > 0 else 0
    
    # 📊 DESPLIEGUE VISUAL DE MÉTRICAS EN INTERNET
    st.subheader(f"Bitácora de asistencia de: {alumno_sel}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="✅ Horas Asistidas", value=f"{horas_asistidas} de {horas_maximas_semana} hrs")
    with col2:
        st.metric(label="❌ Faltas Reales", value=f"{horas_faltas} hrs")
    with col3:
        st.metric(label="📊 Porcentaje de Faltas", value=f"{porcentaje_faltas:.1f}%")

    # 🚨 SEMÁFORO DE ALERTAS INTELIGENTE DGETI (Basado en la resta corregida)
    if porcentaje_faltas >= 21:
        st.error(f"🔴 **ALERTA CRÍTICA:** Has alcanzado o superado el límite del 21% de inasistencias en horas. Riesgo inminente de BAJA en el sistema DGETI.")
    elif porcentaje_faltas >= 15:
        st.warning(f"🟡 **ADVERTENCIA:** Tienes un {porcentaje_faltas:.1f}% de inasistencias en horas. Estás muy cerca del límite permitido (21%).")
    else:
        st.success(f"🟢 **ESTATUS REGULAR:** Tu porcentaje de faltas es del {porcentaje_faltas:.1f}%. Te mantienes en situación aprobatoria.")

    # Mostrar el desglose por fechas del Excel (solo las columnas que contienen las fechas)
    st.markdown("---")
    st.write("📅 **Desglose de horas asistidas por día de clase:**")
    
    columnas_fechas = [c for c in df_asist.columns if "mayo" in c or "junio" in c]
    df_fechas_alumno = df_asist[df_asist["nombre"] == alumno_sel][columnas_fechas]
    st.table(df_fechas_alumno)
