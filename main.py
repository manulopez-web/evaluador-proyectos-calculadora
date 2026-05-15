from montecarlo import *
import matplotlib.pyplot as plt
from ia_analysis import *

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
# FORMULARIO
# =========================================================

proyectos = []

for p in range(num):

    st.divider()

    st.subheader(f"📁 Proyecto {p+1}")

    col1, col2 = st.columns(2)

    with col1:

        nombre = st.text_input(
            f"Nombre del proyecto {p+1}",
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

        tasa = st.number_input(
            f"Tasa descuento (%) {p+1}",
            min_value=0.0,
            value=10.0,
            key=f"t{p}"
        ) / 100

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
                1,
                5,
                3,
                help="""
1 = Impacto bajo  
5 = Impacto muy alto
"""
            )

    # =====================================================
    # FLUJOS
    # =====================================================

    st.markdown("### 💰 Flujos de caja")

    flujos = [-abs(inversion)]

    columnas = st.columns(min(años, 4))

    for i in range(1, años + 1):

        with columnas[(i - 1) % len(columnas)]:

            flujo = st.number_input(
                f"Flujo año {i}",
                value=500000.0,
                key=f"f{p}{i}"
            )

        flujos.append(flujo)

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
# BOTÓN PRINCIPAL
# =========================================================

if st.button("🚀 Evaluar proyectos"):

    resultados = []

    # =====================================================
    # CÁLCULOS
    # =====================================================

    for proyecto in proyectos:

        nombre = proyecto["nombre"]
        tipo = proyecto["tipo"]
        tasa = proyecto["tasa"]
        flujos = proyecto["flujos"]
        impacto = proyecto["impacto"]
        inversion = proyecto["inversion"]

        vpn = calcular_vpn(tasa, flujos)

        tir = calcular_tir(flujos)

        rbc = calcular_rbc(tasa, flujos)

        payback = calcular_payback(flujos)

        roi = calcular_roi(
            inversion,
            sum(flujos[1:])
        )

        indice = indice_rentabilidad(
            vpn,
            inversion
        )

        score = score_financiero(
            vpn,
            tir,
            rbc,
            impacto
        )

        clasificacion = clasificacion_proyecto(
            vpn,
            tir,
            rbc
        )

        riesgo = clasificar_riesgo(
            vpn,
            tir
        )

        flujo_acumulado = np.cumsum(flujos)

        resultados.append({

            "Proyecto": nombre,
            "Tipo": tipo,
            "VPN": round(vpn, 2),
            "TIR (%)": round(tir * 100, 2),
            "Payback": payback,
            "RBC": round(rbc, 2),
            "ROI (%)": round(roi, 2),
            "Índice Rentabilidad": round(indice, 2),
            "Impacto Social": impacto,
            "Score": round(score, 2),
            "Clasificación": clasificacion,
            "Riesgo": riesgo,
            "Flujo Acumulado": round(flujo_acumulado[-1], 2)

        })

    # =====================================================
    # DATAFRAME
    # =====================================================

    df = pd.DataFrame(resultados)

    st.divider()

    st.subheader("📊 Resultados Consolidados")

    st.dataframe(
        df,
        width="stretch"
    )

    # =====================================================
    # UN SOLO PROYECTO
    # =====================================================

    if len(df) == 1:

        fila = df.iloc[0]

        st.divider()

        st.subheader("📌 Evaluación Individual")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("VPN", f"${fila['VPN']:,.2f}")
        c2.metric("TIR (%)", f"{fila['TIR (%)']}%")
        c3.metric("RBC", fila["RBC"])
        c4.metric("Score", f"{fila['Score']:,.2f}")

        if fila["VPN"] > 0:

            st.success(f"""
🟢 El proyecto {fila['Proyecto']}
presenta viabilidad financiera.

El análisis evidencia generación
positiva de valor económico.
""")

        else:

            st.error(f"""
🔴 El proyecto {fila['Proyecto']}
no presenta viabilidad financiera.
""")

    # =====================================================
    # COMPARACIÓN
    # =====================================================

    else:

        df = df.sort_values(
            by="Score",
            ascending=False
        ).reset_index(drop=True)

        mejor = df.iloc[0]
        segundo = df.iloc[1]

        costo = mejor["VPN"] - segundo["VPN"]

        st.divider()

        st.subheader("🏆 Comparación Inteligente")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Mejor Proyecto",
            mejor["Proyecto"]
        )

        c2.metric(
            "VPN Líder",
            f"${mejor['VPN']:,.2f}"
        )

        c3.metric(
            "Score Líder",
            f"{mejor['Score']:,.2f}"
        )

        c4.metric(
            "Costo Oportunidad",
            f"${costo:,.2f}"
        )

        st.success(f"""
El proyecto recomendado es:

🏆 {mejor['Proyecto']}

La decisión se fundamenta en:

• Rentabilidad  
• Riesgo  
• Impacto social  
• Score financiero  
• Generación de valor  
""")

        # =================================================
        # GRÁFICAS
        # =================================================

        st.divider()

        st.subheader("📈 Comparación Financiera")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### VPN")

            st.bar_chart(
                df.set_index("Proyecto")["VPN"]
            )

        with col2:

            st.markdown("### Score")

            st.bar_chart(
                df.set_index("Proyecto")["Score"]
            )

    # =====================================================
    # SENSIBILIDAD
    # =====================================================

    st.divider()

    st.subheader("📉 Sensibilidad Financiera")

    proyecto_base = proyectos[0]

    tasas, vpns = sensibilidad_vpn(
        proyecto_base["flujos"]
    )

    sens_df = pd.DataFrame({

        "Tasa (%)": tasas,
        "VPN": vpns

    })

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        tasas,
        vpns,
        marker='o',
        linewidth=2
    )

    ax.axhline(
        0,
        color='red',
        linestyle='--',
        linewidth=2
    )

    punto = punto_critico_vpn(
        tasas,
        vpns
    )

    if punto:

        ax.axvline(
            punto,
            color='red',
            linestyle='--',
            linewidth=2
        )

    ax.set_title(
        "Sensibilidad VPN vs Tasa"
    )

    ax.set_xlabel(
        "Tasa de descuento (%)"
    )

    ax.set_ylabel(
        "VPN"
    )

    ax.grid(True)

    st.pyplot(fig)

    if punto:

        st.warning(f"""
⚠️ Punto crítico detectado:

A partir de una tasa cercana al
{punto}% el VPN comienza
a ser negativo.
""")

    # =====================================================
    # IA FINANCIERA
    # =====================================================

    st.divider()

    st.subheader("🤖 Análisis Inteligente con IA")

    with st.spinner("Generando análisis ejecutivo..."):

        analisis_ia = generar_analisis_ia(df)

    st.success("✅ Análisis generado correctamente")

    st.markdown(analisis_ia)

    # =====================================================
    # MONTE CARLO
    # =====================================================

    st.divider()

    st.subheader("🎲 Simulación Monte Carlo")

    resultado_mc = simulacion_montecarlo(

        proyecto_base["flujos"],
        proyecto_base["tasa"],

        simulaciones=5000,

        variacion=0.15

    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "VPN Promedio",
        f"${resultado_mc['vpn_promedio']:,.2f}"
    )

    c2.metric(
        "Probabilidad Éxito",
        f"{resultado_mc['probabilidad_exito']}%"
    )

    c3.metric(
        "Desviación",
        f"${resultado_mc['desviacion']:,.2f}"
    )

    fig2, ax2 = plt.subplots(figsize=(10,5))

    ax2.hist(
        resultado_mc["vpns"],
        bins=40
    )

    ax2.axvline(
        0,
        color='red',
        linestyle='--',
        linewidth=2
    )

    ax2.set_title(
        "Distribución Monte Carlo del VPN"
    )

    ax2.set_xlabel(
        "VPN"
    )

    ax2.set_ylabel(
        "Frecuencia"
    )

    ax2.grid(True)

    st.pyplot(fig2)

    # =====================================================
    # EXPORTACIÓN
    # =====================================================

    st.divider()

    st.subheader("📥 Exportación Ejecutiva")

    exportar_excel(
        df,
        sens_df
    )

    archivo = "C:/Users/johan/Desktop/analisis_proyectos.xlsx"

    with open(archivo, "rb") as f:

        st.download_button(
            "📥 Descargar Reporte Ejecutivo",
            f,
            file_name="analisis_proyectos.xlsx"
        )

    # =====================================================
    # CONCLUSIÓN
    # =====================================================

    st.divider()

    st.subheader("🧠 Conclusión General")

    st.markdown("""
La plataforma integra análisis financiero,
evaluación social, simulación probabilística
e inteligencia artificial para apoyar
la toma de decisiones estratégicas.

El sistema permite comparar proyectos,
analizar escenarios, medir sensibilidad
y estimar probabilidades de éxito
financiero de manera más profesional.
""")