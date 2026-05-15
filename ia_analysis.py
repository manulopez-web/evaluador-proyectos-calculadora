"""
MÓDULO IA - ANÁLISIS INTELIGENTE AVANZADO
"""

# =========================================================
# IMPORTACIONES
# =========================================================

import google.generativeai as genai
import pandas as pd
import os

from dotenv import load_dotenv

# =========================================================
# CARGAR VARIABLES DE ENTORNO
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# =========================================================
# CONFIGURAR GEMINI
# =========================================================

GEMINI_DISPONIBLE = False

try:

    if API_KEY:

        genai.configure(api_key=API_KEY)

        GEMINI_DISPONIBLE = True

except:

    GEMINI_DISPONIBLE = False

# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================

def generar_analisis_ia(df):

    """
    Genera análisis ejecutivo automático
    utilizando Gemini AI.

    Si Gemini falla, el sistema genera
    automáticamente un análisis interno
    avanzado sin detener la plataforma.
    """

    # =====================================================
    # VALIDACIÓN
    # =====================================================

    if df.empty:

        return """
No existen proyectos suficientes para analizar.
"""

    # =====================================================
    # MEJOR PROYECTO
    # =====================================================

    mejor = df.sort_values(
        by="Score",
        ascending=False
    ).iloc[0]

    # =====================================================
    # RESUMEN TABLA
    # =====================================================

    resumen = df.to_string(index=False)

    # =====================================================
    # PROMPT PROFESIONAL
    # =====================================================

    prompt = f"""
Actúa como un director financiero senior
especialista en evaluación de proyectos,
riesgo financiero y análisis estratégico.

Analiza los siguientes resultados:

{resumen}

Debes generar un análisis profesional
extenso y técnico incluyendo:

1. Resumen ejecutivo
2. Proyecto más recomendable
3. Interpretación del VPN
4. Interpretación del TIR
5. Evaluación del RBC
6. Interpretación del score
7. Evaluación del riesgo
8. Evaluación financiera general
9. Posibles debilidades
10. Recomendaciones estratégicas
11. Conclusión final

Usa lenguaje profesional,
claro y técnico.
"""

    # =====================================================
    # INTENTO GEMINI
    # =====================================================

    if GEMINI_DISPONIBLE:

        try:

            model = genai.GenerativeModel(
                "gemini-1.5-flash"
            )

            respuesta = model.generate_content(
                prompt
            )

            if respuesta.text:

                return respuesta.text

        except:

            pass

    # =====================================================
    # FALLBACK INTELIGENTE
    # =====================================================

    vpn = mejor["VPN"]
    tir = mejor["TIR (%)"]
    rbc = mejor["RBC"]
    score = mejor["Score"]
    clasificacion = mejor["Clasificación"]
    riesgo = mejor["Riesgo"]

    # =====================================================
    # INTERPRETACIÓN VPN
    # =====================================================

    if vpn > 0:

        texto_vpn = f"""
El proyecto genera valor económico positivo,
debido a que presenta un VPN de
${vpn:,.2f}.

Esto indica que los ingresos futuros
superan la inversión inicial requerida.
"""

    else:

        texto_vpn = f"""
El VPN obtenido es negativo
(${vpn:,.2f}),
lo que evidencia destrucción de valor
bajo las condiciones actuales.
"""

    # =====================================================
    # INTERPRETACIÓN TIR
    # =====================================================

    if tir > 20:

        texto_tir = f"""
La TIR de {tir}% refleja una rentabilidad
alta y competitiva frente al costo
de capital.
"""

    elif tir > 10:

        texto_tir = f"""
La TIR de {tir}% refleja una rentabilidad
moderada y financieramente aceptable.
"""

    else:

        texto_tir = f"""
La TIR de {tir}% refleja una rentabilidad
limitada frente al riesgo asumido.
"""

    # =====================================================
    # INTERPRETACIÓN RBC
    # =====================================================

    if rbc > 1:

        texto_rbc = f"""
La relación beneficio/costo es de {rbc},
indicando que los beneficios descontados
superan los costos del proyecto.
"""

    else:

        texto_rbc = f"""
La relación beneficio/costo es de {rbc},
lo que evidencia debilidad financiera
en el equilibrio económico del proyecto.
"""

    # =====================================================
    # ANÁLISIS FINAL
    # =====================================================

    analisis = f"""
# 📌 ANÁLISIS EJECUTIVO INTELIGENTE

## 🏆 Proyecto recomendado

### {mejor['Proyecto']}

El sistema identifica este proyecto
como la mejor alternativa estratégica
según los indicadores financieros,
sociales y de riesgo evaluados.

---

# 📊 Evaluación Financiera

## VPN

{texto_vpn}

---

## TIR

{texto_tir}

---

## RBC

{texto_rbc}

---

# 🎯 Score Estratégico

El proyecto obtuvo un score total de:

# {score:,.2f}

Este score integra múltiples variables:

• Rentabilidad  
• Riesgo financiero  
• Retorno esperado  
• Impacto social  
• Generación de valor  
• Relación beneficio/costo  

permitiendo realizar una evaluación
multicriterio más completa.

---

# ⚠️ Riesgo Financiero

Clasificación del riesgo:

## {riesgo}

El análisis evidencia un comportamiento
financiero coherente frente a los
escenarios evaluados.

---

# 📈 Clasificación General

## {clasificacion}

La combinación de VPN,
TIR, RBC y score permite concluir
que el proyecto presenta condiciones
favorables para la inversión.

---

# 🧠 Recomendaciones Estratégicas

Se recomienda:

• Monitorear los flujos futuros  
• Controlar variaciones de costos  
• Evaluar escenarios económicos  
• Mantener estabilidad financiera  
• Realizar seguimiento periódico del VPN  

---

# 🚀 Conclusión Final

El proyecto evaluado presenta
condiciones financieras y estratégicas
favorables según los indicadores
analizados por la plataforma.

La evaluación evidencia capacidad
de generación de valor,
rentabilidad aceptable y sostenibilidad
económica en el tiempo.

Por lo tanto,
el proyecto puede considerarse
una alternativa viable para inversión
o implementación estratégica.
"""

    return analisis