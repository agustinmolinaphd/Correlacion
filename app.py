import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Simulador de Evidencia Organizacional", layout="wide")

# Diccionario de datos y escenarios
casos = {
    "Clima de servicio en el equipo vs Desempeño financiero del equipo": {
        "r": 0.22, 
        "x_nom": "Clima de servicio en el equipo", 
        "y_nom": "Desempeño financiero del equipo", 
        "color": "#2ecc71", "base_y": 100, "scale_y": 15,
        "ref": "Hong, Y., Liao, H., Hu, J., & Jiang, K. (2013). Missing link in the service profit chain: a meta-analytic review. Journal of Applied Psychology, 98(2), 237."
    },
    "Clima de seguridad en la unidad vs Accidentes en la unidad": {
        "r": -0.17, 
        "x_nom": "Clima de seguridad en la unidad", 
        "y_nom": "Accidentes en la unidad", 
        "color": "#e74c3c", "base_y": 30, "scale_y": -5,
        "ref": "Jiang, L., Lavaysse, L. M., & Probst, T. M. (2019). Safety climate and safety outcomes: A meta-analytic comparison. Work & Stress, 33(1), 41-57."
    },
    "Edad del trabajador/a vs Creatividad del trabajador/a": {
        "r": 0.00, 
        "x_nom": "Edad del trabajador/a", 
        "y_nom": "Creatividad del trabajador/a", 
        "color": "#95a5a6", "base_y": 50, "scale_y": 0,
        "ref": "Ng, T. W., & Feldman, D. C. (2008). The relationship of age to ten dimensions of job performance. Journal of Applied Psychology, 93(2), 392."
    }
}

# --- Título e Introducción ---
st.title("📊 Simulador de Decisiones Basadas en Evidencia")
st.markdown("""
Esta herramienta permite visualizar cómo impactan diferentes variables organizacionales basándose en **meta-análisis** previos.
""")

# --- Sidebar para Controles ---
st.sidebar.header("Configuración del Escenario")

caso_seleccionado = st.sidebar.selectbox(
    "Seleccionar Escenario:",
    options=list(casos.keys())
)

config = casos[caso_seleccionado]

valor_x = st.sidebar.slider(
    f"Nivel de {config['x_nom']}:",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.01
)

# --- Lógica de Simulación ---
def generar_grafico(caso_nombre, valor_x):
    config = casos[caso_nombre]
    r = config["r"]
    n = 350 
    
    # Generar datos aleatorios consistentes
    np.random.seed(42) # Semilla para que los puntos no "salten" al mover el slider
    x_continuo = np.random.normal(3.2, 0.7, n)
    x_continuo = np.clip(x_continuo, 1.0, 5.0)
    
    # Generar Y con r meta-analítico
    ruido_std = np.sqrt(1 - r**2) * 12
    y = config["base_y"] + (config["scale_y"] * (x_continuo - 3)) + np.random.normal(0, ruido_std, n)
    y = np.clip(y, 0, None)

    # Regresión lineal
    m, b = np.polyfit(x_continuo, y, 1)
    y_proyectado = m * valor_x + b

    # Crear la figura
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#fdfdfd')
    
    # Nube de puntos
    ax.scatter(x_continuo, y, alpha=0.3, color=config["color"], s=40, label="Datos de la muestra")
    
    # Línea de tendencia
    x_line = np.linspace(1, 5, 100)
    ax.plot(x_line, m*x_line + b, color='#34495e', lw=2, label=f"Tendencia (r = {r})")

    # Proyección y Sombreado
    ax.axvline(valor_x, color='#2980b9', linestyle='--', alpha=0.5)
    ax.axhline(y_proyectado, color='#2980b9', linestyle='--', alpha=0.5)
    ax.fill_between([1, valor_x], [y_proyectado, y_proyectado], color='#3498db', alpha=0.1)
    
    ax.plot(valor_x, y_proyectado, marker='h', color='#2980b9', markersize=12, 
            markeredgecolor='white', markeredgewidth=2, label="Proyección estimada")

    # Estética de ejes
    ax.set_xlim(0.8, 5.2)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["1\nTotalmente en\ndesacuerdo", "2\nEn\ndesacuerdo", "3\nNeutral", 
                        "4\nDe\nacuerdo", "5\nTotalmente de\nacuerdo"], fontsize=8)
    
    ax.set_title(f"Impacto estimado: {config['x_nom']} ➔ {config['y_nom']}", fontsize=12, fontweight='bold')
    ax.set_xlabel(config['x_nom'])
    ax.set_ylabel(config['y_nom'])
    ax.legend(loc='upper left', frameon=True, fontsize='small')
    ax.grid(True, linestyle=':', alpha=0.3)
    
    return fig, y_proyectado

# --- Renderizado en Streamlit ---
col1, col2 = st.columns([2, 1])

with col1:
    fig, y_estimado = generar_grafico(caso_seleccionado, valor_x)
    st.pyplot(fig)

with col2:
    st.subheader("Proyección Estratégica")
    st.metric(label=config['y_nom'], value=f"{y_estimado:.2f}")
    
    st.info(f"""
    **Análisis:** Si el promedio de **{config['x_nom']}** se sitúa en **{valor_x:.2f}**, 
    el resultado esperado para **{config['y_nom']}** es de **{y_estimado:.2f}** unidades.
    """)
    
    st.markdown("### Referencia Científica")
    st.caption(config['ref'])

# Pie de página
st.markdown("---")
st.markdown("*Nota: Los puntos representan una simulación estadística basada en los coeficientes de correlación (r) reportados en la literatura académica.*")
