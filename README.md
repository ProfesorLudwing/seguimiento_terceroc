# 📊 Sistema de Seguimiento Académico Interactivo

Este proyecto fue desarrollado como parte de mi portafolio profesional como **Analista de Datos**. Consiste en un ecosistema digital local y en la nube diseñado para optimizar el control docente, automatizar reportes directivos y ofrecer un portal de consulta interactivo para los estudiantes.

## 🛠️ Tecnologías Utilizadas
* **Base de Datos:** SQL (SQLite) diseñado y gestionado de forma nativa mediante **DBeaver**.
* **Lenguaje de Programación:** Python 3 (entorno virtual aislado para la gestión de dependencias).
* **Análisis de Datos:** Pandas y SQLAlchemy para la extracción, transformación y carga (ETL).
* **Interfaz e Implementación Web:** Streamlit Community Cloud (Despliegue en la Nube).
* **Control de Versiones:** Git y GitHub.
* **Inteligencia de Negocios (BI):** Power BI Desktop (Dashboard de cumplimiento escolar).

## 🚀 Componentes del Proyecto

### 1. Portal Web del Alumno (Streamlit)
* **Buscador Interactivo:** Filtra en tiempo real el estado y la calificación de cada alumno mediante consultas SQL automatizadas.
* **Diseño Ergonómico:** Interfaz en modo oscuro con tonos ámbar y crema para reducir la fatiga visual del docente y los estudiantes.
* **Actualización en Segundos:** Sincronización automática con la nube mediante comandos Git (`git push`) al realizar cambios locales.

### 2. Panel de Control del Profesor (Power BI)
* **Gráfico de Sectores Interactivos:** Mide visualmente el porcentaje exacto de cumplimiento general del grupo (Tareas Entregadas vs. Pendientes).
* **Matriz de Alumnos Rezagados:** Listado compacto y automatizado que filtra exclusivamente a los alumnos deudores y sus fechas límite para reportes directivos.
* **Exportación Directiva:** Diseño optimizado para impresión en papel o distribución inmediata en formato PDF.

---
*Proyecto diseñado con un enfoque 100% local y seguro, garantizando la continuidad operativa en el aula sin depender de conexiones a internet estables.*
