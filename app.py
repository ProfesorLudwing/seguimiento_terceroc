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

# 6. Mostrar el resultado de la consulta personalizada en la web
st.subheader(f"Estado actual de: {alumno_seleccionado}")
st.table(datos_filtrados)
# 7. Botón inteligente para generar e imprimir la guía de avance en PDF
st.markdown("---")
st.write("¿Necesitas tu boleta física o una guía de estudio?")

# Al presionar este botón, se activa el comando de impresión del dispositivo del alumno
if st.button("🖨️ Generar e Imprimir mi Guía de Avance (PDF)"):
    # Añadimos un pequeño truco visual para que al abrir la ventana de impresión se enfoque en sus datos
    st.write("💡 *Consejo: En la ventana que se abrirá, selecciona 'Guardar como PDF' o elige tu impresora.*")
    
    # Este comando de JavaScript le ordena a Chrome/Edge de tu alumno abrir el menú de impresión nativo
    st.components.v1.html(
        "<script>window.print();</script>",
        height=0
    )

