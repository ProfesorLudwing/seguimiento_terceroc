import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# 1. Configuración de la interfaz web
st.title("Sistema de Seguimiento Académico")
st.write("Bienvenido al portal de consulta de tareas.")

# 2. Conexión y lectura de la base de datos SQL
engine = create_engine("sqlite:///clase")
df = pd.read_sql("SELECT * FROM seguimiento", engine)

# 3. Buscador interactivo para alumnos y padres
alumno_seleccionado = st.selectbox(
    "Selecciona tu nombre para verificar tus calificaciones:",
    df["nombre"].unique()
)

# 4. Filtrar y ordenar el historial del estudiante
datos_filtrados = df[df["nombre"] == alumno_seleccionado]
columnas_vista = ["tarea", "estado", "calificacion", "fecha_limite"]
tabla_final = datos_filtrados[columnas_vista]

st.subheader(f"📋 Historial de entregas de: {alumno_seleccionado}")
st.table(tabla_final)

# 5. MOTOR DE GENERACIÓN AUTOMÁTICA DE PDF (Fondo blanco y letras negras)
def generar_pdf_boleta(nombre_alumno, datos_tabla):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.black, spaceAfter=10)
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=11, textColor=colors.black, spaceAfter=20)
    
    # Encabezado del documento físico
    story.append(Paragraph("<b>BOLETA OFICIAL DE SEGUIMIENTO ACADÉMICO</b>", title_style))
    story.append(Paragraph(f"<b>Estudiante:</b> {nombre_alumno}", text_style))
    story.append(Spacer(1, 10))
    
    # Estructurar la tabla para ReportLab
    contenido_tabla = [["Actividad", "Estado", "Calificación", "Fecha Límite"]]
    for fila in datos_tabla.values:
        contenido_tabla.append([str(celda) for celda in fila])
    
    # Diseño estético de la tabla para impresión en papel (Letras negras, líneas limpias)
    t = Table(contenido_tabla, colWidths=[120, 100, 80, 100])
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
    return buffer

# 6. Botón de un solo clic exclusivo para Alumnos y Padres de Familia
st.markdown("---")
st.subheader("📥 Descarga tu Guía en PDF")

pdf_data = generar_pdf_boleta(alumno_seleccionado, tabla_final)

st.download_button(
    label="📥 Descargar mi Boleta Oficial (PDF)",
    data=pdf_data,
    file_name=f"Boleta_{alumno_seleccionado.replace(' ', '_')}.pdf",
    mime="application/pdf",
    use_container_width=True
)
