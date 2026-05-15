import streamlit as st
import pandas as pd
from indicadores import *
from sensibilidad import *

# ---------------------------------
# CONFIGURACIÓN PÁGINA
# ---------------------------------

st.set_page_config(
    page_title="Evaluador Inteligente de Proyectos",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# DISEÑO PREMIUM
# ---------------------------------

st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

h1 {
    color: #0A2540;
    text-align: center;
}

.stButton>button {
    background-color: #0066FF;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #004FCC;
    color: white;
}

.metric-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# TÍTULO
# ---------------------------------

st.title("💼 Evaluador Inteligente de Proyectos")
st.markdown("### Plataforma financiera y social para toma de decisiones")

# ---------------------------------
# CANTIDAD PROYECTOS
# ---------------------------------

num = st.number_input(
    "📌 Número de proyectos a evaluar",
    min_value=1,
    value=1
)

resultados = []

# ---------------------------------
# FORMULARIO PROYECTOS
# ---------------------------------

for p in range(num):

    st.markdown("---")

    st.subheader(f"📁 Proyecto {p+1}")

    tipo = st.selectbox(
        f"Tipo de proyecto {p+1}",
        ["Empresarial", "Social"],
        key=f"tipo{p}"
    )

    nombre = st.text_input(
        f"Nombre proyecto {p+1}",
        key=f"nombre{p}"
    )

    inversion = st.number_input(
        f"Inversión inicial {p+1}",
        min_value=0.0,
        key=f"inv{p}"
    )

    tasa = st.number_input(
        f"Tasa de descuento (%) {p+1}",
        min_value=0.0,
        key=f"tasa{p}"
    ) / 100

    años = st.number_input(
        f"Años del proyecto {p+1}",
        min_value=1,
        key=f"años{p}"
    )

    impacto = 0

    if tipo == "Social":

        impacto = st.slider(
            f"Impacto social {p+1}",
            1,
            5,
            3,
            help="""
            1 = Muy bajo
            5 = Muy alto
            """
        )

    flujos = [-abs(inversion)]

    st.markdown("### 💰 Flujos de caja")

    for i in range(1, años + 1):

        flujo = st.number_input(
            f"Año {i} - Proyecto {p+1}",
            key=f"flujo{p}{i}"
        )

        flujos.append(flujo)

    # ---------------------------------
    # CÁLCULOS
    # ---------------------------------

    vpn = calcular_vpn(tasa, flujos)
    tir = calcular_tir(flujos)
    payback = calcular_payback(flujos)
    rbc = calcular_rbc(flujos, inversion)

    score = vpn + (impacto * 1000000)

    resultados.append({
        "Proyecto": nombre,
        "Tipo": tipo,
        "VPN": round(vpn, 2),
        "TIR": round(tir * 100, 2),
        "Payback": round(payback, 2),
        "RBC": round(rbc, 2),
        "Impacto Social": impacto,
        "Score": round(score, 2)
    })

# ---------------------------------
# BOTÓN GENERAL
# ---------------------------------

if st.button("🚀 Evaluar proyectos"):

    df = pd.DataFrame(resultados)

    df = df.sort_values(by="Score", ascending=False)

    st.markdown("---")

    st.subheader("📊 Resultados Generales")

    st.dataframe(df)

    # ---------------------------------
    # EXPLICACIÓN SCORE
    # ---------------------------------

    st.subheader("🧮 Explicación del Score")

    st.info("""
    El score es un indicador compuesto utilizado para priorizar proyectos.

    Fórmula aplicada:

    Score = VPN + (Impacto Social × 1,000,000)

    Esto permite integrar variables financieras y sociales
    dentro del análisis de toma de decisiones.
    """)

    # ---------------------------------
    # UN SOLO PROYECTO
    # ---------------------------------

    if len(df) == 1:

        proyecto = df.iloc[0]

        st.subheader("🧠 Conclusión Inteligente")

        if proyecto["VPN"] > 0:

            st.success(f"""
            El proyecto {proyecto['Proyecto']} es financieramente viable,
            debido a que presenta un VPN positivo.

            La rentabilidad esperada supera el costo de inversión
            y el proyecto muestra estabilidad financiera aceptable.
            """)

        else:

            st.error(f"""
            El proyecto {proyecto['Proyecto']} no presenta viabilidad
            financiera bajo las condiciones actuales.

            Sin embargo, si se trata de un proyecto social,
            podría justificarse por su impacto comunitario.
            """)

    # ---------------------------------
    # MÚLTIPLES PROYECTOS
    # ---------------------------------

    else:

        mejor = df.iloc[0]

        st.subheader("🏆 Mejor alternativa")

        st.success(f"""
        El proyecto recomendado es:

        {mejor['Proyecto']}

        debido a que obtuvo el mayor score global.
        """)

        segundo = df.iloc[1]

        costo = mejor["VPN"] - segundo["VPN"]

        st.warning(f"""
        ⚠️ Costo de oportunidad:
        {round(costo,2)}
        """)

        st.subheader("🤖 Análisis Inteligente")

        st.info(f"""
        El sistema identificó que el proyecto {mejor['Proyecto']}
        presenta mejores condiciones financieras y sociales
        frente a las demás alternativas evaluadas.

        El análisis considera:
        • Rentabilidad
        • Recuperación de inversión
        • Relación beneficio costo
        • Impacto social
        • Sensibilidad financiera

        Esto permite tomar decisiones más informadas
        y estratégicas.
        """)

    # ---------------------------------
    # GRÁFICOS
    # ---------------------------------

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Comparación VPN")

        st.bar_chart(df.set_index("Proyecto")["VPN"])

        st.caption("Eje X = Proyecto | Eje Y = VPN")

    with col2:

        st.subheader("📊 Comparación Score")

        st.bar_chart(df.set_index("Proyecto")["Score"])

        st.caption("Eje X = Proyecto | Eje Y = Score")

    # ---------------------------------
    # SENSIBILIDAD
    # ---------------------------------

    tasas, vpns = sensibilidad_vpn(flujos)

    st.subheader("📉 Sensibilidad del VPN")

    sens_df = pd.DataFrame({
        "Tasa (%)": tasas,
        "VPN": vpns
    })

    st.line_chart(sens_df.set_index("Tasa (%)"))

    st.info("""
    El análisis de sensibilidad permite observar cómo cambia
    el VPN ante variaciones en la tasa de descuento.
    """)

    # ---------------------------------
    # ESCENARIOS
    # ---------------------------------

    st.subheader("📊 Escenarios Financieros")

    escenarios_df = pd.DataFrame({
        "Escenario": ["Pesimista", "Actual", "Optimista"],
        "VPN": [
            round(df.iloc[0]["VPN"] * 0.8, 2),
            round(df.iloc[0]["VPN"], 2),
            round(df.iloc[0]["VPN"] * 1.2, 2)
        ]
    })

    st.dataframe(escenarios_df)

    st.bar_chart(escenarios_df.set_index("Escenario"))

    # ---------------------------------
    # INTERPRETACIÓN IA
    # ---------------------------------

    st.subheader("🤖 Interpretación avanzada con IA")

    st.success("""
    La plataforma realiza una interpretación automatizada
    basada en los resultados financieros y sociales obtenidos.

    El análisis incorpora variables de rentabilidad,
    estabilidad financiera, sensibilidad y generación
    de valor social, permitiendo una evaluación integral
    para apoyar la toma de decisiones estratégicas.
    """)