import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ================================
# CONFIGURACIÓN GENERAL
# ================================
st.set_page_config(
    page_title="Predicción OEE – Agrobol",
    page_icon="🌿",
    layout="wide"
)

# Paleta Agrobol
GREEN_DARK = "#1F3D2E"
GREEN_MED = "#3E7D5F"
GREEN_LIGHT = "#77EBAB"
GREEN_SOFT = "#BEFFDD"
WHITE = "#FFFFFF"

# ================================
# ESTILOS CSS PERSONALIZADOS
# ================================
css = f"""
<style>

body {{
    background-color: {WHITE};
}}

h1, h2, h3, h4, h5, h6, label, .stTextInput label {{
    color: {GREEN_DARK} !important;
}}

[data-testid="stMetricValue"] {{
    color: {GREEN_DARK} !important;
}}

.card {{
    background: {GREEN_SOFT};
    padding: 18px;
    border-radius: 12px;
    box-shadow: 1px 1px 8px #cccccc;
}}

.header-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ================================
# ENCABEZADO
# ================================
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown(
        f"<h1 style='font-weight:700;'>Modelo Predictivo de OEE – Agrobol</h1>",
        unsafe_allow_html=True
    )
with col2:
    st.image("logo_agrobol.png", width=90)

st.write("---")

# ================================
# CARGAR MODELO
# ================================
model = joblib.load("modelo_predictivo_gradient_boosting.pkl")

# Orden de columnas usado por el modelo
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

# ================================
# SIDEBAR – DASHBOARD DE MÉTRICAS
# ================================
st.sidebar.header("Dashboard de métricas")

st.sidebar.metric("Versión del modelo", "Gradient Boosting")
st.sidebar.metric("R² del modelo", "0.986")
st.sidebar.metric("MAE", "0.0255")
st.sidebar.metric("RMSE", "0.0483")

st.sidebar.write("---")
st.sidebar.write("**Agrobol S.A. – Proyecto de Grado**")

# ================================
# MODO DE OPERACIÓN
# ================================
modo = st.radio(
    "Seleccione el modo de ingreso:",
    ("Subir archivo Excel/CSV", "Ingresar valores manualmente")
)

# ===============================================
# 1) MODO ARCHIVO
# ===============================================
if modo == "Subir archivo Excel/CSV":

    archivo = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])

    if archivo:
        try:
            df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
            st.success("Archivo cargado correctamente.")
            st.dataframe(df.head())

            df = df[column_order]
            df["OEE_Predicho"] = model.predict(df)

            st.subheader("Resultados del archivo")
            st.dataframe(df)

            st.download_button(
                "Descargar predicciones",
                df.to_csv(index=False).encode("utf-8"),
                "predicciones_oee.csv",
                "text/csv"
            )

        except Exception as e:
            st.error(f"Error en el archivo: {e}")

# ===============================================
# 2) MODO MANUAL
# ===============================================
else:
    st.subheader("Ingreso manual de valores")

    entradas = {}
    columnas_numericas = [c for c in column_order if any(x in c for x in ["(", "$", "Min", "Kg", "cm"])]
    columnas_dummies = [c for c in column_order if c not in columnas_numericas]

    # Tarjetas distribuidas en 3 columnas
    colA, colB, colC = st.columns(3)

    for i, col in enumerate(column_order):

        cont = colA if i % 3 == 0 else colB if i % 3 == 1 else colC

        with cont:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            if col in columnas_numericas:
                entradas[col] = st.number_input(col, value=0.0)
            else:
                entradas[col] = st.selectbox(col, [0, 1], index=0)

            st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Predecir OEE"):
        fila = pd.DataFrame([entradas])[column_order]
        pred = model.predict(fila)[0]
        st.success(f"OEE Predicho: **{pred:.4f}**")
