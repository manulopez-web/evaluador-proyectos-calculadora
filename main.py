from montecarlo import *
import matplotlib.pyplot as plt
from ia_analysis import *

import os
import streamlit as st
import pandas as pd
import numpy as np

from indicadores import *
from sensibilidad import *
from exportar import exportar_excel

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Evaluador Inteligente de Proyectos",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# ESTILOS PREMIUM
# =========================================================

st.markdown("""
<style>
.main { background-color: #F4F7FA; }
h1, h2, h3 { color: #0A2540; }
.stButton>button {
    background: linear-gradient(90deg,#0066FF,#00A3FF);
    color: white;
    border-radius: 14px;
    height: 52px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}
[data-testid="stMetricValue"] { color: #0066FF; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO Y SIDEBAR
# =========================================================

st.title("🚀 Plataforma Inteligente de Evaluación de Proyectos")

st.sidebar.header("⚙️ Configuración")
num = st.sidebar.number_input("Número de proyectos", min_value=1, value=2)

# =========================================================
# FORMULARIO DE CAPTURA
# =========================================================

proyectos = []

for p in range(num):
    st.divider()
    st.subheader(f"📁 Proyecto {p+1}")
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input(f"Nombre {p+1}", value=f"Proyecto {p+1}", key=f"n{p}")
        tipo = st.selectbox(f"Tipo {p+1}", ["Empresarial", "Social"], key=f"tipo{p}")
        inversion = st.number_input(f"Inversión inicial {p+1}", min_value=0.0, value=1000000.0, key=f"inv{p}")

    with col2:
        tasa = st.number_input(f"Tasa (%) {p+1}", min_value=0.0, value=10.0, key=f"t{p}") / 100
        años = st.number_input(f"Años {p+1}", min_value=1, value=5, key=f"a{p}")
        impacto = 0
        if tipo == "Social":
            impacto = st.slider(f"Impacto social {p+1}", 1, 5, 3, key=f"imp{p}")

    st.markdown("### 💰 Flujos de caja")
    flujos = [-abs(inversion)]
    columnas = st.columns(min(años, 4))
    for i in range(1, años + 1):
        with columnas[(i - 1) % len(columnas)]:
            flujo_input = st.number_input(f"Año {i}", value=500000.0, key=f"f{p}{i}")
            flujos.append(flujo_input)

    proyectos.append({
        "nombre": nombre, "tipo": tipo, "tasa": tasa, 
        "años": años, "flujos": flujos, "impacto": impacto, "inversion": inversion
    })

# =========================================================
# PROCESAMIENTO (EL CORAZÓN DEL CÓDIGO)
# =========================================================

if st.button("🚀 Evaluar proyectos"):
    resultados = []

    for proyecto in proyectos:
        # 1. Obtener valores crudos
        vpn_raw = calcular_vpn(proyecto["tasa"], proyecto["flujos"])
        tir_raw = calcular_tir(proyecto["flujos"])
        rbc_raw = calcular_rbc(proyecto["tasa"], proyecto["flujos"])

        # 2. LIMPIEZA CRÍTICA (Evita el TypeError de la línea 205)
        # Esto asegura que si la función devuelve None o un error, sea 0.0
        vpn = float(vpn_raw) if (vpn_raw is not None and not np.isnan(vpn_raw)) else 0.0
        tir = float(tir_raw) if (tir_raw is not None and not np.isnan(tir_raw)) else 0.0
        rbc = float(rbc_raw) if (rbc_raw is not None and not np.isnan(rbc_raw)) else 0.0

        # 3. Resto de indicadores usando valores ya limpios
        payback = calcular_payback(proyecto["flujos"])
        roi = calcular_roi(proyecto["inversion"], sum(proyecto["flujos"][1:]))
        indice = indice_rentabilidad(vpn, proyecto["inversion"])
        score = score_financiero(vpn, tir, rbc, proyecto["impacto"])
        
        # 4. Clasificaciones (Ahora seguras porque vpn, tir y rbc son float)
        clasificacion = clasificacion_proyecto(vpn, tir, rbc)
        riesgo = clasificar_riesgo(vpn, tir, rbc)

        resultados.append({
            "Proyecto": proyecto["nombre"],
            "Tipo": proyecto["tipo"],
            "VPN": vpn,
            "TIR (%)": round(tir * 100, 2),
            "Payback": payback,
            "RBC": rbc,
            "ROI (%)": round(roi, 2),
            "Score": score,
            "Clasificación": clasificacion,
            "Riesgo": riesgo
        })

    df = pd.DataFrame(resultados)
    st.session_state["df"] = df

    # --- MOSTRAR RESULTADOS ---
    st.divider()
    st.subheader("📊 Resultados Consolidados")
    st.dataframe(df, use_container_width=True)

    # Gráficas y comparación
    if len(df) > 1:
        st.subheader("🏆 Comparación")
        c1, c2 = st.columns(2)
        with c1: st.bar_chart(df.set_index("Proyecto")["VPN"])
        with c2: st.bar_chart(df.set_index("Proyecto")["Score"])

    # --- SENSIBILIDAD ---
    st.divider()
    st.subheader("📉 Sensibilidad")
    t_sens, v_sens = sensibilidad_vpn(proyectos[0]["flujos"])
    sens_df = pd.DataFrame({"Tasa (%)": t_sens, "VPN": v_sens})
    st.session_state["sens_df"] = sens_df
    st.line_chart(sens_df.set_index("Tasa (%)"))

    # --- IA ---
    st.divider()
    st.subheader("🤖 Análisis IA")
    with st.spinner("Analizando..."):
        st.markdown(generar_analisis_ia(df))

    # --- MONTE CARLO ---
    st.divider()
    st.subheader("🎲 Monte Carlo")
    res_mc = simulacion_montecarlo(proyectos[0]["flujos"], proyectos[0]["tasa"])
    st.metric("Probabilidad Éxito", f"{res_mc['probabilidad_exito']}%")

# =========================================================
# EXPORTACIÓN
# =========================================================
if "df" in st.session_state:
    st.divider()
    archivo = exportar_excel(st.session_state["df"], st.session_state.get("sens_df", pd.DataFrame()))
    if archivo:
        with open(archivo, "rb") as f:
            st.download_button("📥 Descargar Excel", f, file_name="reporte.xlsx")

st.info("Plataforma lista para toma de decisiones.")