import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# ============================
# PALETA AGROBOL
# ============================
VERDE_OSCURO = "#1F3D2E"
VERDE_MEDIO = "#3E7D5F"
VERDE_CLARO = "#77EBAB"
VERDE_PASTEL = "#BEFFDD"

# ============================
# CONFIGURACIÓN DE LA PÁGINA
# ============================
st.set_page_config(
    page_title="Predicción OEE – Agrobol",
    page_icon="🌿",
    layout="wide"
)

# ==========================
# ESTILOS PARA EL SIDEBAR
# ==========================
sidebar_style = """
<style>
[data-testid="stSidebar"] {
    background-color: #3E7D5F; /* Verde Agrobol */
}
[data-testid="stSidebar"] * {
    color: white !important;   /* Letra blanca dentro del sidebar */
}
</style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
        body {{
            background-color: white;
            color: {VERDE_OSCURO};
        }}
        h1, h2, h3, h4, label, .stRadio label {{
            color: {VERDE_OSCURO} !important;
        }}
        div.stButton > button:first-child {{
            background-color: {VERDE_MEDIO};
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }}
        .card {{
            background-color: #F9FAF9;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #d9d9d9;
            margin-bottom: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================
# CARGAR MODELO
# ============================
model = joblib.load("modelo_predictivo_gradient_boosting.pkl")

# ============================
# LOGO
# ============================
st.image("logo_agrobol.png", width=400)

# ============================
# TÍTULO
# ============================
st.markdown(f"<h1 style='font-size:36px;' >Modelo Predictivo de OEE – Agrobol</h1>", unsafe_allow_html=True)
st.markdown("---")


# ORDEN DE VARIABLES EXACTO DEL MODELO
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
# SIDEBAR DASHBOARD
# ============================
st.sidebar.markdown(f"<h2>Dashboard</h2>", unsafe_allow_html=True)
st.sidebar.info("Ingrese los valores en la interfaz principal para obtener el OEE predictivo.")

st.sidebar.write("---")
st.sidebar.write("**Agrobol S.A. – Proyecto de Grado**")

# ============================
#  BLOQUES DE VARIABLES
# ============================
st.markdown("## Ingreso de Variables")

col1, col2, col3 = st.columns(3)

# ======================================================
# BLOQUE 1 — TURNOS (selección múltiple)
# ======================================================
with col1:
    st.markdown("### Turnos")
    turnos = st.multiselect(
        "Seleccione uno o más turnos:",
        ["Turno_Dia", "Turno_Tarde", "Turno_Noche"],
        default=["Turno_Dia"]
    )

    turno_values = {
        "Turno_Dia": 1 if "Turno_Dia" in turnos and len(turnos) == 1 else 0,
        "Turno_Tarde": 1 if "Turno_Tarde" in turnos else 0,
        "Turno_Noche": 1 if "Turno_Noche" in turnos else 0
    }

    # Si el usuario no selecciona nada, activar Turno_Dia
    if sum(turno_values.values()) == 0:
        turno_values["Turno_Dia"] = 1


# ======================================================
# BLOQUE 2 — LÍNEA DE PRODUCTO (SOLO 1 OPCIÓN)
# ======================================================
with col2:
    st.markdown("### Línea de Producto")
    linea_sel = st.radio(
        "Seleccione una línea de producto:",
        ["Ninguna", "C", "G", "P/B"]
    )
    linea_values = {
        "Linea producto_C": 1 if linea_sel == "C" else 0,
        "Linea producto_G": 1 if linea_sel == "G" else 0,
        "Linea producto_P/B": 1 if linea_sel == "P/B" else 0,
    }

# ======================================================
# BLOQUE 3 — DISEÑO PERFORADO (SOLO 1)
# ======================================================
with col3:
    st.markdown("### Diseño Perforado")
    dis = st.radio(
        "Seleccione un diseño:",
        ["Ninguno", "Lineal 45", "Sin diseño", "Z20", "Z35", "Z50", "Z60", "Z75"]
    )
    dis_values = {
        'Diseño perforado_Lineal 45': 1 if dis=="Lineal 45" else 0,
        'Diseño perforado_Sin diseño': 1 if dis=="Sin diseño" else 0,
        'Diseño perforado_Zigzag 20': 1 if dis=="Z20" else 0,
        'Diseño perforado_Zigzag 35': 1 if dis=="Z35" else 0,
        'Diseño perforado_Zigzag 50': 1 if dis=="Z50" else 0,
        'Diseño perforado_Zigzag 60': 1 if dis=="Z60" else 0,
        'Diseño perforado_Zigzag 75': 1 if dis=="Z75" else 0,
    }

# ======================================================
# BLOQUE 4 — MÁQUINAS (SOLO UNA)
# ======================================================
st.markdown("### Selección de Máquina (solo una)")
maquina = st.radio(
    "Seleccione la máquina utilizada:",
    ["Ninguna", "Cortadora 1", "Cortadora 2", "Cortadora 3", 
     "Extrusora 2", "Extrusora 3", "Extrusora 4", "Extrusora 5",
     "Perforadora", "Perforadora 1", "Perforadora 2",
     "Cortadora 2 (alt)", "Cortadora 3 (alt)"]
)

maquina_map = {
    'Maquina_cortadora 1': maquina=="Cortadora 1",
    'Maquina_cortadora 2': maquina=="Cortadora 2",
    'Maquina_cortadora 3': maquina=="Cortadora 3",
    'Maquina_extrusora 2': maquina=="Extrusora 2",
    'Maquina_extrusora 3': maquina=="Extrusora 3",
    'Maquina_extrusora 4': maquina=="Extrusora 4",
    'Maquina_Extrusora 5': maquina=="Extrusora 5",
    'Maquina_perforadora': maquina=="Perforadora",
    'Maquina_perforadora 1': maquina=="Perforadora 1",
    'Maquina_perforadora 2': maquina=="Perforadora 2",
    'Maquina_Cortadora 2': maquina=="Cortadora 2 (alt)",
    'Maquina_Cortadora 3': maquina=="Cortadora 3 (alt)",
}

# ======================================================
# BLOQUE 5 — VARIABLES NUMÉRICAS
# ======================================================
st.markdown("### Variables Numéricas")

num_cols1, num_cols2, num_cols3 = st.columns(3)

num_inputs = {}

numericas = [
 'Ancho (cm)','Largo (cm)','Calibre (mp)',
 'Peso Paquete','Cantidad Conforme (Kg)',
 'Número de Capas por Rollo/Número de rollos',
 'Retal proceso (Kg)',
 'Retal Natural - Aleluya/Orejas/ Torta (Kg)',
 'PARO ALISTAMIENTO (Min)','PARO PROGRAMADO (Min)',
 'PARO CALIDAD (Min)','PARO AVERIAS (Min)','PARO ORGANIZACIÓN (Min)',
 'Velocidad teorica','Velocidad Real','No conforme (Kg)',
]

grupo = [num_cols1, num_cols2, num_cols3]
idx = 0
for col in numericas:
    with grupo[idx % 3]:
        num_inputs[col] = st.number_input(col, value=0.0)
    idx += 1

# ======================================================
# BLOQUE 6 — VALOR COP
# ======================================================
valor_cop = st.number_input("VALOR MOD NO UTILIZADO POR INEFICIENCIA (COP $)", value=0.0)

# ======================================================
# BLOQUE 7 — VARIABLES BINARIAS
# ======================================================
ref = st.radio("Referencia_LE", [0, 1])
oper = st.radio("Operario_LE", [0, 1])

# ======================================================
# BOTÓN DE PREDICCIÓN (con medidor y clasificación)
# ======================================================
if st.button("Calcular OEE"):
    row = {}

    # Cargar todas las variables
    row.update(dis_values)
    row.update(linea_values)
    row.update(maquina_map)
    row.update(turno_values)
    row.update(num_inputs)

    row['VALOR MOD NO UTILIZADO POR INEFICIENCIA (COP $)'] = valor_cop
    row['Referencia_LE'] = ref
    row['Operario_LE'] = oper

    # Asegurar que todas las columnas existan (incluso si faltan)
    for col in column_order:
        row.setdefault(col, 0)

    df = pd.DataFrame([row])[column_order]

    pred = float(model.predict(df)[0])
    porcentaje = pred * 100

    # =======================
    # CLASIFICACIÓN DEL OEE
    # =======================
    if porcentaje < 60:
        categoria = "Regular"
        color_cat = "#ff6b6b"      # rojo suave
    elif porcentaje < 85:
        categoria = "Aceptable"
        color_cat = "#FFD54F"      # amarillo/mostaza claro
    else:
        categoria = "Bueno"
        color_cat = "#5EBD8F"      # verde Agrobol bueno

    # =======================
    # GAUGE (medidor)
    # =======================
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=porcentaje,
        number={'suffix': "%", 'font': {'color': VERDE_OSCURO}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color_cat},
            'steps': [
                {'range': [0, 60], 'color': "#ffe6e6"},   # regular
                {'range': [60, 85], 'color': VERDE_CLARO}, # aceptable
                {'range': [85, 100], 'color': VERDE_PASTEL}, # bueno
            ]
        }
    ))
    fig.update_layout(height=320)

    # =======================
    # MOSTRAR RESULTADOS
    # =======================
    st.markdown("### Resultado de Predicción")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"""
        <div style='padding: 15px; border-radius: 10px; text-align:center;
                    font-size:22px; font-weight:700; color:{VERDE_OSCURO};
                    background-color:{color_cat}; opacity:0.85;'>
            OEE Predicho: {porcentaje:.2f}% — {categoria}
        </div>
        """,
        unsafe_allow_html=True
    )




