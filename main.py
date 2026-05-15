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
.main {
    background-color: #F4F7FA;
}
h1, h2, h3 {
    color: #0A2540;
}
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
.stButton>button:hover {
    background: linear-gradient(90deg,#004FCC,#008AE6);
    color: white;
}
[data-testid="stMetricValue"] {
    color: #0066FF;
    font-weight: bold;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("🚀 Plataforma Inteligente de Evaluación de Proyectos")

st.markdown("""
Sistema avanzado de evaluación financiera,
social y estratégica con simulación probabilística,
análisis inteligente y comparación multicriterio.
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Configuración")

num = st.sidebar.number_input(
    "Número de proyectos",
    min_value=1,
    value=2
)

st.sidebar.info("""
La plataforma permite:
• Evaluación financiera  
• Evaluación social  
• Comparación multicriterio  
• Simulación Monte Carlo  
• Sensibilidad del VPN  
• Inteligencia artificial  
• Exportación ejecutiva  
""")

# =========================================================
# FORMULARIO (RECOLECCIÓN DE DATOS)
# =========================================================

proyectos = []

for p in range(num):
    st.divider()
    st.subheader(f"📁 Proyecto {p+1}")
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input(
            f"Nombre del proyecto {p+1}",
            value=f"Proyecto {p+1}",
            key=f"n{p}"
        )
        tipo = st.selectbox(
            f"Tipo de proyecto {p+1}",
            ["Empresarial", "Social"],
            key=f"tipo{p}"
        )
        inversion = st.number_input(
            f"Inversión inicial {p+1}",
            min_value=0.0,
            value=1000000.0,
            key=f"inv{p}"
        )

    with col2:
        tasa_input = st.number_input(
            f"Tasa descuento (%) {p+1}",
            min_value=0.0,
            value=10.0,
            key=f"t{p}"
        )
        tasa = tasa_input / 100
        
        años = st.number_input(
            f"Años del proyecto {p+1}",
            min_value=1,
            value=5,
            key=f"a{p}"
        )
        impacto = 0
        if tipo == "Social":
            impacto = st.slider(
                f"Impacto social {p+1}",
                1, 5, 3,
                key=f"imp{p}",
                help="1 = Bajo, 5 = Muy alto"
            )

    st.markdown("### 💰 Flujos de caja")
    flujos = [-abs(inversion)]
    columnas = st.columns(min(años, 4))
    for i in range(1, años + 1):
        with columnas[(i - 1) % len(columnas)]:
            flujo_val = st.number_input(
                f"Flujo año {i} (P{p+1})",
                value=500000.0,
                key=f"f{p}{i}"
            )
        flujos.append(flujo_val)

    proyectos.append({
        "nombre": nombre,
        "tipo": tipo,
        "tasa": tasa,
        "años": años,
        "flujos": flujos,
        "impacto": impacto,
        "inversion": inversion
    })

# =========================================================
# LÓGICA DE PROCESAMIENTO (DENTRO DEL BOTÓN)
# =========================================================

if st.button("🚀 Evaluar proyectos"):
    resultados = []

    for proyecto in proyectos:
        # Extraer datos con seguridad
        p_nombre = proyecto["nombre"]
        p_tipo = proyecto["tipo"]
        p_tasa = proyecto["tasa"]
        p_flujos = proyecto["flujos"]
        p_impacto = proyecto["impacto"]
        p_inversion = proyecto["inversion"]

        # 1. CÁLCULOS BASE
        vpn_calc = calcular_vpn(p_tasa, p_flujos)
        tir_calc = calcular_tir(p_flujos)
        rbc_calc = calcular_rbc(p_tasa, p_flujos)

        # 🔴 BLINDAJE ANTI-TYPEERROR: 
        # Convertimos todo a float y manejamos nulos antes de pasar a otras funciones
        vpn = float(vpn_calc) if vpn_calc is not None else 0.0
        tir = float(tir_calc) if tir_calc is not None else 0.0
        rbc = float(rbc_calc) if rbc_calc is not None else 0.0

        # 2. INDICADORES SECUNDARIOS
        payback = calcular_payback(p_flujos)
        roi = calcular_roi(p_inversion, sum(p_flujos[1:]))
        indice = indice_rentabilidad(vpn, p_inversion)
        score = score_financiero(vpn, tir, rbc, p_impacto)
        
        # 3. CLASIFICACIONES (Aquí es donde fallaba antes)
        clasificacion = clasificacion_proyecto(vpn, tir, rbc)
        riesgo = clasificar_riesgo(vpn, tir, rbc)
        
        flujo_acumulado = np.cumsum(p_flujos)

        resultados.append({
            "Proyecto": p_nombre,
            "Tipo": p_tipo,
            "VPN": round(vpn, 2),
            "TIR (%)": round(tir * 100, 2),
            "Payback": payback,
            "RBC": round(rbc, 2),
            "ROI (%)": round(roi, 2),
            "Índice Rentabilidad": round(indice, 2),
            "Impacto Social": p_impacto,
            "Score": round(score, 2),
            "Clasificación": clasificacion,
            "Riesgo": riesgo,
            "Flujo Acumulado": round(flujo_acumulado[-1], 2)
        })

    # Guardar en Session State para que persista al descargar
    df = pd.DataFrame(resultados)
    st.session_state["df"] = df

    # --- VISUALIZACIÓN DE RESULTADOS ---
    st.divider()
    st.subheader("📊 Resultados Consolidados")
    st.dataframe(df, use_container_width=True)

    # Evaluación por cantidad de proyectos
    if len(df) == 1:
        fila = df.iloc[0]
        st.divider()
        st.subheader(f"📌 Evaluación Individual: {fila['Proyecto']}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("VPN", f"${fila['VPN']:,.2f}")
        c2.metric("TIR (%)", f"{fila['TIR (%)']}%")
        c3.metric("RBC", fila["RBC"])
        c4.metric("Score", f"{fila['Score']:,.2f}")

        if fila["VPN"] > 0:
            st.success(f"🟢 El proyecto presenta viabilidad financiera.")
        else:
            st.error(f"🔴 El proyecto no presenta viabilidad financiera.")

    else:
        # Comparación si hay más de uno
        df_sorted = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
        mejor = df_sorted.iloc[0]
        segundo = df_sorted.iloc[1]
        costo_op = mejor["VPN"] - segundo["VPN"]

        st.divider()
        st.subheader("🏆 Comparación Inteligente")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Mejor Proyecto", mejor["Proyecto"])
        c2.metric("VPN Líder", f"${mejor['VPN']:,.2f}")
        c3.metric("Score Líder", f"{mejor['Score']:,.2f}")
        c4.metric("Costo Oportunidad", f"${costo_op:,.2f}")

        st.success(f"🏆 El proyecto recomendado por el sistema es: **{mejor['Proyecto']}**")

        st.divider()
        st.subheader("📈 Comparación Financiera Visual")
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            st.markdown("### VPN por Proyecto")
            st.bar_chart(df.set_index("Proyecto")["VPN"])
        with col_graf2:
            st.markdown("### Score de Rendimiento")
            st.bar_chart(df.set_index("Proyecto")["Score"])

    # --- ANÁLISIS DE SENSIBILIDAD ---
    st.divider()
    st.subheader("📉 Sensibilidad Financiera (Proyecto Principal)")
    p_base = proyectos[0]
    tasas_sens, vpns_sens = sensibilidad_vpn(p_base["flujos"])
    sens_df = pd.DataFrame({"Tasa (%)": tasas_sens, "VPN": vpns_sens})
    st.session_state["sens_df"] = sens_df

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(tasas_sens, vpns_sens, marker='o', color='#0066FF', linewidth=2)
    ax.axhline(0, color='red', linestyle='--', linewidth=1.5)
    
    p_critico = punto_critico_vpn(tasas_sens, vpns_sens)
    if p_critico:
        ax.axvline(p_critico, color='orange', linestyle=':', label=f'Cruce: {p_critico}%')
    
    ax.set_title("Sensibilidad: VPN vs Tasa de Descuento")
    ax.set_xlabel("Tasa (%)")
    ax.set_ylabel("VPN ($)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)

    # --- INTELIGENCIA ARTIFICIAL ---
    st.divider()
    st.subheader("🤖 Análisis Estratégico con IA")
    with st.spinner("Analizando datos..."):
        informe_ia = generar_analisis_ia(df)
    st.info("Informe ejecutivo generado por IA")
    st.markdown(informe_ia)

    # --- SIMULACIÓN MONTE CARLO ---
    st.divider()
    st.subheader("🎲 Simulación de Riesgo Monte Carlo")
    res_mc = simulacion_montecarlo(p_base["flujos"], p_base["tasa"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric("VPN Promedio Esperado", f"${res_mc['vpn_promedio']:,.2f}")
    m2.metric("Probabilidad de Éxito", f"{res_mc['probabilidad_exito']}%")
    m3.metric("Riesgo (Desviación)", f"${res_mc['desviacion']:,.2f}")

    fig_mc, ax_mc = plt.subplots(figsize=(10, 4))
    ax_mc.hist(res_mc["vpns"], bins=50, color='#00A3FF', edgecolor='white', alpha=0.7)
    ax_mc.axvline(0, color='red', linestyle='--')
    ax_mc.set_title("Distribución Probabilística del VPN")
    st.pyplot(fig_mc)

# =========================================================
# EXPORTACIÓN Y CIERRE
# =========================================================

if "df" in st.session_state:
    st.divider()
    st.subheader("📥 Exportación Ejecutiva")
    
    # Intentar generar el Excel
    try:
        path_excel = exportar_excel(
            st.session_state["df"], 
            st.session_state.get("sens_df", pd.DataFrame())
        )
        
        if path_excel and os.path.exists(path_excel):
            with open(path_excel, "rb") as file:
                st.download_button(
                    label="📥 Descargar Reporte en Excel",
                    data=file,
                    file_name="Analisis_Financiero_Gerenciarte.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.warning("El módulo de exportación está esperando datos finales.")

st.divider()
st.subheader("🧠 Conclusión del Sistema")
st.markdown("""
Esta plataforma utiliza modelos econométricos y redes neuronales para transformar 
datos financieros en decisiones estratégicas. El análisis de **Gerenciarte** asegura 
que la Belleza y la Moda se gestionen con la precisión de una gran corporación.
""")