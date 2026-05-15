"""
MÓDULO: ANÁLISIS DE SENSIBILIDAD AVANZADO

Este módulo permite evaluar cómo cambian los resultados
del proyecto ante variaciones en variables financieras.

Incluye:

1. Sensibilidad del VPN
2. Sensibilidad de la TIR
3. Escenarios financieros
4. Punto crítico de viabilidad
5. Sensibilidad de ingresos
6. Sensibilidad de costos
7. Clasificación de riesgo
8. Interpretación financiera automática
"""

import numpy_financial as npf

# -----------------------------------------------------
# SENSIBILIDAD VPN
# -----------------------------------------------------

def sensibilidad_vpn(flujos):

    tasas = list(range(1, 31))

    vpns = []

    for t in tasas:

        vpn = npf.npv(t / 100, flujos)

        vpns.append(round(vpn, 2))

    return tasas, vpns

# -----------------------------------------------------
# PUNTO CRÍTICO
# -----------------------------------------------------

def punto_critico_vpn(tasas, vpns):

    for i in range(len(vpns)-1):

        if vpns[i] > 0 and vpns[i+1] < 0:

            return tasas[i+1]

    return None

# -----------------------------------------------------
# SENSIBILIDAD TIR
# -----------------------------------------------------

def sensibilidad_tir(flujos):

    inversiones = list(range(5, 21))

    tires = []

    for inv in inversiones:

        inv_real = -inv * 1000000

        nuevos_flujos = [inv_real] + flujos[1:]

        tir_temp = npf.irr(nuevos_flujos)

        if tir_temp is not None:

            tires.append(round(tir_temp * 100, 2))

        else:

            tires.append(0)

    return inversiones, tires

# -----------------------------------------------------
# ESCENARIOS FINANCIEROS
# -----------------------------------------------------

def generar_escenarios(vpn_actual):

    escenarios = {

        "Pesimista": round(vpn_actual * 0.8, 2),

        "Actual": round(vpn_actual, 2),

        "Optimista": round(vpn_actual * 1.2, 2)
    }

    return escenarios

# -----------------------------------------------------
# SENSIBILIDAD INGRESOS
# -----------------------------------------------------

def sensibilidad_ingresos(flujos):

    porcentajes = [-30, -20, -10, 0, 10, 20, 30]

    resultados = []

    for p in porcentajes:

        nuevos_flujos = [flujos[0]]

        for f in flujos[1:]:

            nuevo = f * (1 + p/100)

            nuevos_flujos.append(nuevo)

        vpn = npf.npv(0.1, nuevos_flujos)

        resultados.append(round(vpn,2))

    return porcentajes, resultados

# -----------------------------------------------------
# SENSIBILIDAD COSTOS
# -----------------------------------------------------

def sensibilidad_costos(flujos):

    porcentajes = [-30, -20, -10, 0, 10, 20, 30]

    resultados = []

    for p in porcentajes:

        nueva_inversion = flujos[0] * (1 + p/100)

        nuevos_flujos = [nueva_inversion] + flujos[1:]

        vpn = npf.npv(0.1, nuevos_flujos)

        resultados.append(round(vpn,2))

    return porcentajes, resultados

# -----------------------------------------------------
# CLASIFICACIÓN RIESGO
# -----------------------------------------------------

def clasificar_riesgo(vpn, tir):

    if vpn > 0 and tir > 20:

        return "Riesgo bajo"

    elif vpn > 0 and tir > 10:

        return "Riesgo moderado"

    else:

        return "Riesgo alto"

# -----------------------------------------------------
# ESTABILIDAD FINANCIERA
# -----------------------------------------------------

def estabilidad_financiera(vpns):

    positivos = 0

    for v in vpns:

        if v > 0:

            positivos += 1

    estabilidad = (positivos / len(vpns)) * 100

    return round(estabilidad,2)

# -----------------------------------------------------
# INTERPRETACIÓN AUTOMÁTICA
# -----------------------------------------------------

def interpretacion_sensibilidad(vpn, estabilidad):

    if vpn > 0 and estabilidad >= 70:

        return """
El proyecto presenta estabilidad financiera aceptable
frente a cambios en variables económicas.

La sensibilidad indica una buena capacidad
de adaptación financiera.
"""

    elif vpn > 0:

        return """
El proyecto mantiene viabilidad financiera,
aunque presenta sensibilidad moderada
ante cambios económicos.
"""

    else:

        return """
El proyecto presenta alta vulnerabilidad financiera.

Los cambios en variables económicas afectan
significativamente la viabilidad del proyecto.
"""

# -----------------------------------------------------
# RESUMEN EJECUTIVO
# -----------------------------------------------------

def resumen_riesgo(vpn, tir, estabilidad):

    riesgo = clasificar_riesgo(vpn, tir)

    texto = f"""
Resumen ejecutivo del riesgo:

• VPN actual: {round(vpn,2)}
• TIR esperada: {round(tir,2)}%
• Estabilidad financiera: {round(estabilidad,2)}%
• Clasificación del riesgo: {riesgo}

Este análisis permite evaluar la capacidad
del proyecto para soportar variaciones
económicas y financieras.
"""

    return texto