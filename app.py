import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ============================
# CONFIGURACIÓN GENERAL
# ============================
st.set_page_config(
    page_title="Predicción OEE – Agrobol",
    page_icon="🌿",
    layout="wide"
)

# Paleta Agrobol
COLOR_PRINCIPAL = "#1F3D2E"
COLOR_SECUNDARIO = "#3E7D5F"
COLOR_ACENTO = "#5EBD8F"
COLOR_FONDO_SUAVE = "#F6FFF9"   # Blanco con matiz verde
COLOR_CARD = "#FFFFFF"

# ============================
# CSS PERSONALIZADO
# ============================
custom_css = f"""
<style>

body {{
    background-color: {COLOR_FONDO_SUAVE};
}}

[data-testid="stAppViewContainer"] {{
    background-color: {COLOR_FONDO_SUAVE};
}}

[data-testid="stSidebar"] {{
    background-color: {COLOR_PRINCIPAL};
}}

h1, h2, h3 {{
    color: {COLOR_PRINCIPAL};
    font-weight: 700;
    font-family: 'Arial', sans-serif;
}}

.card {{
    background: {COLOR_CARD};
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e3e3e3;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 25px;
}}

.header-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0px 20px 0px;
}}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ============================
# ENCABEZADO CON LOGO
# ============================
st.markdown(
    """
    <div class="header-container">
        <h1>Modelo Predictivo OEE – Agrobol</h1>
        <img src="logo_agrobol.png" width="110">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================
# CARGAR MODELO
# ============================
model = joblib.load("modelo_predictivo_gradient_boosting.pkl")

# ORDEN DE COLUMNAS
column_order = [
 'Diseño perforado_Lineal 45','Diseño perforado_Sin diseño',
 'Diseño perforado_Zigzag 20','Diseño perforado_Zigzag 35',
 'Diseño perforado_Zigzag 50','Diseño perforado_Zigzag 60',
 'Diseño perforado_Zigzag 75','Linea producto_C','Linea producto_G',
 'Linea producto_P/B','Maquina_Cortadora 2','Maquina_Cortadora 3',
 'Maquina_Extrusora 5','Maquina_Perforadora 1','Maquina_cortadora 1',
 'Maquina_cortadora 2','Maquina_cortadora 3','Maquina_extrusora 2',
 'Maquina_extrusora 3','Maquina_extrusora 4','Maquina_perforadora',
 'Maquina_perforadora 1','Maquina_perforadora 2','Turno_Noche',
 'Turno_Tarde','Ancho (cm)','Largo (cm)','Calibre (mp)',
 'Peso Paquete','Cantidad Conforme (Kg)',
 'Número de Capas por Rollo/Número de rollos',
 'Retal proceso (Kg)',
 'Retal Natural - Aleluya/Orejas/ Torta (Kg)',
 'PARO ALISTAMIENTO (Min)','PARO PROGRAMADO (Min)',
 'PARO CALIDAD (Min)','PARO AVERIAS (Min)','PARO ORGANIZACIÓN (Min)',
 'Velocidad teorica','Velocidad Real','No conforme (Kg)',
 'VALOR MOD NO UTILIZADO POR INEFICIENCIA (COP $)',
 'Referencia_LE','Operario_LE'
]

# ============================
# OPCIÓN DEL USUARIO
# ============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
modo = st.radio(
    "Seleccione el modo de ingreso de datos:",
    ("Cargar archivo Excel/CSV", "Ingresar datos manualmente")
)
st.markdown("</div>", unsafe_allow_html=True)


# ============================
# MODO ARCHIVO
# ============================
if modo == "Cargar archivo Excel/CSV":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    archivo = st.file_uploader("Sube el archivo:", type=["csv", "xlsx"])
    st.markdown("</div>", unsafe_allow_html=True)

    if archivo:
        try:
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.success("Archivo cargado correctamente.")
            st.dataframe(df.head())
            st.markdown("</div>", unsafe_allow_html=True)

            # Reordenar columnas
            df = df[column_order]

            pred = model.predict(df)
            df["OEE_Predicho"] = pred

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Resultados de Predicción")
            st.dataframe(df)
            st.download_button(
                "Descargar resultados",
                df.to_csv(index=False).encode("utf-8"),
                "predicciones_oee.csv",
                "text/csv"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error procesando el archivo: {e}")

# ============================
# MODO MANUAL
# ============================
else:
    st.subheader("Ingreso Manual de Datos")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    entradas = {}
    for col in column_order:

        # Variables numéricas
        if any(x in col for x in ["cm", "Kg", "Min", "$", "Capas", "Velocidad"]):
            entradas[col] = st.number_input(col, value=0.0)

        # Variables binarias
        else:
            entradas[col] = st.selectbox(col, [0, 1], index=0)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Predecir OEE"):
        fila = pd.DataFrame([entradas])[column_order]
        pred = model.predict(fila)[0]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.success(f"OEE Predicho: **{pred:.4f}**")
        st.markdown("</div>", unsafe_allow_html=True)

