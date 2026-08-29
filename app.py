import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Título principal de la página web
st.title("Sistema de Seguimiento Académico")
st.write("Bienvenido al portal de consulta de tareas.")

# 2. Conexión con la base de datos SQLite que creamos en DBeaver
engine = create_engine("sqlite:///clase")

# 3. Leer la tabla de SQL y guardarla en un DataFrame de Pandas
df = pd.read_sql("SELECT * FROM seguimiento", engine)

# 4. Mostrar la tabla completa en la web como prueba inicial
# 4. Crear la lista desplegable interactiva con los nombres únicos de tus alumnos
alumno_seleccionado = st.selectbox(
    "Selecciona tu nombre para ver tus tareas pendientes:",
    df["nombre"].unique()
)

# 5. Filtrar la tabla de datos para que solo contenga los renglones de ese alumno
datos_filtrados = df[df["nombre"] == alumno_seleccionado]

# 6. Seleccionar y ordenar las columnas para la vista del alumno
columnas_vista = ["tarea", "estado", "calificacion", "fecha_limite"]
tabla_final = datos_filtrados[columnas_vista]

# 7. Mostrar la tabla personalizada en la web
st.subheader(f"Estado actual de: {alumno_seleccionado}")
st.table(tabla_final)

# 8. Botón nativo de impresión
st.markdown("---")
if st.button("🖨️ Generar mi Guía de Avance (PDF)"):
    st.write("💡 *Consejo: Selecciona 'Guardar como PDF' en la ventana del sistema.*")
    st.components.v1.html(
        "<script>window.print();</script>",
        height=0
    )
