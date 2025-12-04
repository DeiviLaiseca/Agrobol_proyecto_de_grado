
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# CONFIGURACIÓN DE LA APP
st.set_page_config(
    page_title="Predicción OEE – Agrobol",
    page_icon="🌿",
    layout="wide"
)

# Paleta Agrobol
colors = ["#1F3D2E", "#3E7D5F", "#5EBD8F", "#77EBAB", "#BEFFDD"]

# Fondo verde claro
page_bg = f'''
<style>
[data-testid="stAppViewContainer"] {{
    background-color: {colors[4]};
}}
[data-testid="stSidebar"] {{
    background-color: {colors[3]};
}}
.header-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
</style>
'''
st.markdown(page_bg, unsafe_allow_html=True)

# HEADER CON LOGO
col1, col2 = st.columns([7, 1])
with col1:
    st.markdown(
        f"<h1 style='color:{colors[0]};'>Modelo Predictivo OEE – Agrobol</h1>",
        unsafe_allow_html=True
    )
with col2:
    st.image("logo_agrobol.png", width=200)

st.markdown("---")

# CARGAR MODELO
model = joblib.load("modelo_predictivo_gradient_boosting.pkl")

# ORDEN DE COLUMNAS FINAL
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

# OPCIÓN DEL USUARIO
modo = st.radio(
    "Seleccione el modo de ingreso de datos:",
    ("Cargar archivo Excel/CSV", "Ingresar datos manualmente"),
    index=0
)

# 1 MODO ARCHIVO
if modo == "Cargar archivo Excel/CSV":
    archivo = st.file_uploader("Sube el archivo:", type=["csv", "xlsx"])

    if archivo:
        try:
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)

            st.success("Archivo cargado correctamente.")
            st.dataframe(df.head())

            # Reordenar columnas
            df = df[column_order]

            # Predicción
            pred = model.predict(df)
            df["OEE_Predicho"] = pred

            st.subheader("Resultados")
            st.dataframe(df)

            st.download_button(
                "Descargar resultados",
                df.to_csv(index=False).encode("utf-8"),
                "predicciones_oee.csv",
                "text/csv"
            )

        except Exception as e:
            st.error(f"Error procesando el archivo: {e}")

# 2 MODO MANUAL
else:
    st.subheader("Ingrese los valores manualmente")

    entradas = {}
    for col in column_order:
        if "(cm)" in col or "(Kg)" in col or "Min" in col or "(" in col or "$" in col:
            entradas[col] = st.number_input(col, value=0.0)
        else:
            entradas[col] = st.selectbox(col, [0, 1], index=0)

    if st.button("Predecir OEE"):
        fila = pd.DataFrame([entradas])[column_order]
        pred = model.predict(fila)[0]

        st.success(f"OEE Predicho: **{pred:.4f}**")
