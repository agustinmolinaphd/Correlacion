import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página web
st.set_page_config(page_title="Simulador de Correlación", layout="wide")

st.title("📊 Simulador de Impacto Organizacional")
st.markdown("Esta herramienta permite explorar cómo las variables de gestión impactan en los resultados basándose en metaanálisis reales.")

# Diccionario de datos (Basado en tus especificaciones)
casos = {
    "Clima de servicio en el equipo vs Desempeño financiero del equipo": {
        "r": 0.22, "x_nom": "Clima de servicio en el equipo", "y_nom": "Desempeño financiero del equipo", 
        "color": "#2ecc71", "base_y": 100, "scale_y": 15,
        "ref": "Hong, Y., Liao, H., Hu, J., & Jiang, K. (2013). Journal of Applied Psychology, 98(2), 237."
    },
    "Clima de seguridad en la unidad vs Accidentes en la unidad": {
        "r": -0.17, "x_nom": "Clima de seguridad en la unidad", "y_nom": "Accidentes en la unidad", 
        "color": "#e74c3c", "base_y": 30, "scale_y": -5,
        "ref": "Jiang, L., Lavaysse, L. M., & Probst, T. M. (2019). Work & Stress, 33(1), 41-57."
    },
    "Edad del trabajador/a vs Creatividad del trabajador/a": {
        "r": 0.00, "x_nom": "Edad del trabajador/a", "y_nom": "Creatividad del trabajador/a", 
        "color": "#95a5a6", "base_y": 50, "scale_y": 0,
        "ref": "Ng, T. W., & Feldman, D. C. (2008). Journal of Applied Psychology, 93(2), 392."
    }
}

# Barra lateral con controles
with st.sidebar:
    st.header("Controles")
    seleccion = st.selectbox("Seleccionar escenario:", list(casos.keys()))
    n_muestra = st.slider("Tamaño de la muestra (n):", 10, 1000, 200)
    valor_x = st.slider(f"Nivel de {casos[seleccion]['x_nom']}:", 1.0, 5.0, 3.0, 0.01)

# Lógica del Simulador
config = casos[seleccion]
r_meta = config["r"]

# Generación de datos
np.random.seed(42) # Para que sea estable al mover X
x = np.clip(np.random.normal(3.2, 0.7, n_muestra), 1.0, 5.0)
std_error = np.sqrt(1 - r_meta**2) * 12
y = config["base_y"] + (config["scale_y"] * (x - 3)) + np.random.normal(0, std_error, n_muestra)
y = np.clip(y, 0, None)

# Estadísticas
m, b = np.polyfit(x, y, 1)
r_obs = np.corrcoef(x, y)[0,1]
y_proy = m * valor_x + b

# Gráfico
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(x, y, alpha=0.4, color=config["color"], edgecolors='w')
ax.plot(np.linspace(1, 5, 10), m*np.linspace(1, 5, 10) + b, color="#34495e", lw=2)
ax.axvline(valor_x, color='#2980b9', ls='--')
ax.axhline(y_proy, color='#2980b9', ls='--')

# Etiquetas Likert
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(["1\nTotalmente\ndesacuerdo", "2\nEn\ndesacuerdo", "3\nNeutral", "4\nDe\nacuerdo", "5\nTotalmente\nacuerdo"], fontsize=7)
ax.set_title(f"Visualización: {seleccion}")
ax.set_xlabel(config["x_nom"])
ax.set_ylabel(config["y_nom"])

# Mostrar en Streamlit
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(fig)

with col2:
    st.subheader("Análisis de Datos")
    st.metric("Correlación (r) observada", f"{r_obs:.2f}")
    st.metric("Varianza explicada (R²)", f"{r_obs**2:.2%}")
    st.info(f"**Proyección:** Si el promedio de {config['x_nom'].upper()} es {valor_x:.2f}, el valor estimado de {config['y_nom'].upper()} es {y_proy:.2f}.")
    st.caption(f"**Referencia:** {config['ref']}")
