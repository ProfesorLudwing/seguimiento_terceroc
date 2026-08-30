import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# 1. Conexión central a la base de datos SQL de DBeaver
engine = create_engine("sqlite:///clase")

# 2. Menú de navegación lateral
st.sidebar.title("🎒 Panel Escolar 3°D")
opcion_pagina = st.sidebar.radio(
    "Selecciona la sección que deseas consultar:",
    ["📋 Seguimiento de Tareas", "📆 Alertas de Asistencia DGETI"]
)

# 🧠 FUNCIÓN MAESTRA: Fabrica las boletas oficiales en PDF con formato de impresión limpio
def generar_pdf_oficial(nombre_alumno, datos_tabla, tipo_reporte, metricas_texto=""):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.black, spaceAfter=10)
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=11, textColor=colors.black, spaceAfter=15)
    
    story.append(Paragraph(f"<b>REPORTE OFICIAL: {tipo_reporte.upper()}</b>", title_style))
    story.append(Paragraph(f"<b>Estudiante:</b> {nombre_alumno}", text_style))
    if metricas_texto:
        story.append(Paragraph(f"<b>Resumen de Rendimiento:</b> {metricas_texto}", text_style))
    story.append(Spacer(1, 10))
    
    contenido_tabla = [[str(col).capitalize() for col in datos_tabla.columns]]
    for fila in datos_tabla.values:
        contenido_tabla.append([str(int(float(celda))) if str(celda).replace('.','',1).isdigit() and float(celda).is_integer() else str(celda) for celda in fila])
    
    t = Table(contenido_tabla)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EADFCA")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.gray),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
    ]))
    
    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

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
    
    st.markdown("---")
    st.subheader("📥 Descarga tu Boleta de Tareas")
    bytes_boleta = generar_pdf_oficial(alumno_sel, tabla_final, "Seguimiento de Tareas")
    
    st.download_button(
        label="📥 Descargar Boleta de Tareas Oficial (PDF)",
        data=bytes_boleta,
        file_name=f"Boleta_Tareas_{alumno_sel.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ==========================================
# PÁGINA 2: CONTROL DE ASISTENCIAS DGETI
# ==========================================
elif opcion_pagina == "📆 Alertas de Asistencia DGETI":
    st.title("📆 Control de Horas de Clase y Asistencias")
    st.write("Conforme al reglamento de la DGETI, el 21% de inasistencias en horas acumuladas causa baja automática.")
    
    df_asist = pd.read_sql("SELECT * FROM asistencias", engine)
    alumno_sel = st.selectbox("Selecciona tu nombre para verificar tu estatus:", df_asist["nombre"].unique(), key="asistencias_sel")
    
    registros_alumno = df_asist[df_asist["nombre"] == alumno_sel]
    df_asist["asis_max"] = df_asist["asis_max"].ffill()
    maximos_limpios = df_asist[df_asist["nombre"] == alumno_sel]["asis_max"]

    horas_maximas_acumuladas = int(maximos_limpios.sum())
    horas_asistidas_totales = int(registros_alumno["asistencia"].sum())
    horas_faltas_totales = horas_maximas_acumuladas - horas_asistidas_totales
    porcentaje_faltas_real = (horas_faltas_totales / horas_maximas_acumuladas) * 100 if horas_maximas_acumuladas > 0 else 0
    
    st.subheader(f"Bitácora de asistencia de: {alumno_sel}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="✅ Horas Asistidas Totales", value=f"{horas_asistidas_totales} de {horas_maximas_acumuladas} hrs")
    with col2:
        st.metric(label="❌ Faltas Totales Acumuladas", value=f"{horas_faltas_totales} hrs")
    with col3:
        st.metric(label="📊 Porcentaje Real de Faltas", value=f"{porcentaje_faltas_real:.1f}%")

    if porcentaje_faltas_real >= 21:
        st.error(f"🔴 **ALERTA CRÍTICA:** Has alcanzado o superado el límite del {porcentaje_faltas_real:.1f}% de inasistencias acumuladas. Riesgo inminente de BAJA.")
    elif porcentaje_faltas_real >= 15:
        st.warning(f"🟡 **ADVERTENCIA:** Tienes un {porcentaje_faltas_real:.1f}% de inasistencias acumuladas en horas. Estás muy cerca del límite.")
    else:
        st.success(f"🟢 **ESTATUS REGULAR:** Tu porcentaje de faltas es del {porcentaje_faltas_real:.1f}%. Te mantienes en situación aprobatoria.")

    st.markdown("---")
    st.write("📅 **Historial completo de horas asistidas por día de clase:**")
    columnas_fechas = [c for c in df_asist.columns if "mayo" in c or "junio" in c or "de" in c]
    
    df_pantalla_fechas = registros_alumno[columnas_fechas].fillna(0).astype(float).astype(int)
    st.table(df_pantalla_fechas)
    
    st.markdown("---")
    st.subheader("📥 Descarga tu Reporte de Asistencia")
    resumen_asistencia = f"{horas_asistidas_totales} asistencias de {horas_maximas_acumuladas} hrs. Faltas: {horas_faltas_totales} ({porcentaje_faltas_real:.1f}%)"
    bytes_asistencia = generar_pdf_oficial(alumno_sel, registros_alumno[columnas_fechas], "Control de Asistencia DGETI", resumen_asistencia)
    
    st.download_button(
        label="📥 Descargar Reporte de Asistencia Oficial (PDF)",
        data=bytes_asistencia,
        file_name=f"Reporte_Asistencia_{alumno_sel.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ==========================================
# 📂 COMPONENTES INSTITUCIONALES (Descarga Directa Segura)
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Documentos Oficiales")
st.sidebar.write("Descarga los lineamientos del curso:")

try:
    with open("./acuerdo_convivencia.pdf", "rb") as file_acuerdo:
        st.sidebar.download_button(
            label="📜 Descargar Acuerdo de Convivencia (PDF)",
            data=file_acuerdo,
            file_name="Acuerdo_de_Convivencia_3D.pdf",
            mime="application/pdf",
            use_container_width=True
        )
except FileNotFoundError:
    st.sidebar.info("ℹ️ Archivo 'acuerdo_convivencia.pdf' no encontrado.")

try:
    with open("./temario_clase.pdf", "rb") as file_temario:
        st.sidebar.download_button(
            label="📚 Descargar Temario de la Clase (PDF)",
            data=file_temario,
            file_name="Temario_Clase_3D.pdf",
            mime="application/pdf",
            use_container_width=True
        )
except FileNotFoundError:
    st.sidebar.info("ℹ️ Archivo 'temario_clase.pdf' no encontrado.")

# ==========================================
# 🖨️ MÓDULO UNIVERSAL DE BOTÓN DE IMPRESIÓN
# ==========================================
st.sidebar.markdown("---")
st.sidebar.subheader("🖨️ Impresión Rápida")
st.sidebar.write("Para mandar a la impresora física esta pantalla completa de forma inmediata, utiliza el atajo:")
st.sidebar.info("💻 **Presiona las teclas:**\n**Ctrl + P** (Windows)\n**Cmd + P** (Mac)")
st.sidebar.caption("💡 *Nota: Recuerda desmarcar 'Gráficos de fondo' en la ventana de impresión para que la hoja salga blanca.*")
