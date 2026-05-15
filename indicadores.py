"""
MÓDULO: INDICADORES FINANCIEROS AVANZADOS

Este módulo contiene funciones para calcular
indicadores financieros utilizados en la evaluación
de proyectos empresariales y sociales.

INDICADORES:

1. VPN (Valor Presente Neto)
2. TIR (Tasa Interna de Retorno)
3. Payback
4. RBC (Relación Beneficio/Costo)
5. ROI (Retorno sobre inversión)
6. Índice de rentabilidad
7. Punto de equilibrio
8. Margen de seguridad
9. Clasificación financiera
10. Interpretación automática
11. Clasificación de riesgo

------------------------------------------------------

INTERPRETACIÓN:

VPN > 0
→ El proyecto genera valor.

TIR > tasa de descuento
→ El proyecto es rentable.

RBC > 1
→ Los beneficios superan los costos.

ROI > 0
→ Existe retorno positivo.

------------------------------------------------------
"""

import numpy_financial as npf


# ===================================================
# VPN
# ===================================================

def calcular_vpn(tasa, flujos):

    try:

        vpn = npf.npv(tasa, flujos)

        return round(vpn, 2)

    except:

        return 0


# ===================================================
# TIR
# ===================================================

def calcular_tir(flujos):

    try:

        tir = npf.irr(flujos)

        if tir is None:
            return 0

        return round(tir, 4)

    except:

        return 0


# ===================================================
# PAYBACK
# ===================================================

def calcular_payback(flujos):

    acumulado = 0

    for i, flujo in enumerate(flujos):

        acumulado += flujo

        if acumulado >= 0:

            return i

    return "No recuperado"


# ===================================================
# RBC
# ===================================================

def calcular_rbc(tasa, flujos):

    try:

        beneficios = 0
        costos = 0

        for i, f in enumerate(flujos):

            valor_actual = f / ((1 + tasa) ** i)

            if f > 0:

                beneficios += valor_actual

            else:

                costos += abs(valor_actual)

        if costos == 0:

            return 0

        return round(beneficios / costos, 2)

    except:

        return 0


# ===================================================
# ROI
# ===================================================

def calcular_roi(inversion, beneficios):

    try:

        if inversion == 0:

            return 0

        roi = (
            (beneficios - inversion)
            / inversion
        ) * 100

        return round(roi, 2)

    except:

        return 0


# ===================================================
# ÍNDICE RENTABILIDAD
# ===================================================

def indice_rentabilidad(vpn, inversion):

    try:

        if inversion == 0:

            return 0

        indice = (
            vpn + inversion
        ) / inversion

        return round(indice, 2)

    except:

        return 0


# ===================================================
# PUNTO EQUILIBRIO
# ===================================================

def punto_equilibrio(costos_fijos, precio, costo_variable):

    try:

        if precio <= costo_variable:

            return 0

        pe = costos_fijos / (
            precio - costo_variable
        )

        return round(pe, 2)

    except:

        return 0


# ===================================================
# MARGEN SEGURIDAD
# ===================================================

def margen_seguridad(
    ventas_actuales,
    ventas_equilibrio
):

    try:

        if ventas_actuales == 0:

            return 0

        margen = (
            (
                ventas_actuales
                - ventas_equilibrio
            )
            / ventas_actuales
        ) * 100

        return round(margen, 2)

    except:

        return 0


# ===================================================
# SCORE FINANCIERO
# ===================================================

def score_financiero(
    vpn,
    tir,
    rbc,
    impacto
):

    """
    Score compuesto.

    Se ponderan:

    - VPN
    - TIR
    - RBC
    - Impacto social

    """

    try:

        score = (

            vpn * 0.5

            + (tir * 100) * 10000

            + rbc * 50000

            + impacto * 1000000

        )

        return round(score, 2)

    except:

        return 0


# ===================================================
# CLASIFICACIÓN PROYECTO
# ===================================================

def clasificacion_proyecto(
    vpn,
    tir,
    rbc
):

    if vpn > 0 and tir > 0.20 and rbc > 1:

        return "Proyecto altamente viable"

    elif vpn > 0 and tir > 0.10:

        return "Proyecto viable"

    elif vpn > 0:

        return "Proyecto con viabilidad moderada"

    else:

        return "Proyecto no viable"


# ===================================================
# CLASIFICACIÓN RIESGO
# ===================================================

def clasificar_riesgo(vpn, tir, inversion, tasa):

    riesgo = 0

    # 1. VPN negativo = riesgo fuerte
    if vpn < 0:
        riesgo += 0.5

    # 2. TIR comparada con tasa
    if tir < tasa:
        riesgo += 0.3

    # 3. inversión alta (escala relativa)
    if inversion > 2_000_000:
        riesgo += 0.2

    # clasificación
    if riesgo >= 0.7:
        return "Alto"
    elif riesgo >= 0.4:
        return "Moderado"
    else:
        return "Bajo"

# ===================================================
# INTERPRETACIÓN AUTOMÁTICA
# ===================================================

def interpretacion_financiera(
    vpn,
    tir,
    rbc
):

    if vpn > 0 and tir > 0.20 and rbc > 1:

        return """
El proyecto presenta excelentes condiciones financieras.

La generación de valor es positiva,
la rentabilidad es alta y los beneficios
superan significativamente los costos.

El comportamiento financiero evidencia
solidez y sostenibilidad económica.
"""

    elif vpn > 0:

        return """
El proyecto presenta viabilidad financiera aceptable.

Aunque genera valor económico,
algunas variables financieras deben
monitorearse cuidadosamente.
"""

    else:

        return """
El proyecto no presenta condiciones
financieras favorables.

Se recomienda revisar:

• Costos
• Inversión inicial
• Flujos de caja
• Estrategia financiera
"""


# ===================================================
# RESUMEN EJECUTIVO
# ===================================================

def resumen_ejecutivo(
    nombre,
    vpn,
    tir,
    rbc,
    payback
):

    texto = f"""
RESUMEN EJECUTIVO

Proyecto:
{nombre}

VPN:
{vpn}

TIR:
{round(tir * 100, 2)}%

RBC:
{rbc}

Payback:
{payback}

CONCLUSIÓN:

El análisis financiero permite evaluar
la generación de valor, rentabilidad,
riesgo y sostenibilidad económica
del proyecto.
"""

    return texto