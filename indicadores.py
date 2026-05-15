"""
MÓDULO: INDICADORES FINANCIEROS AVANZADOS

Este módulo contiene funciones para calcular
indicadores financieros utilizados en la evaluación
de proyectos empresariales y sociales.

INDICADORES:
1. VPN, 2. TIR, 3. Payback, 4. RBC, 5. ROI, 6. Índice de rentabilidad, 
7. Punto de equilibrio, 8. Margen de seguridad, 9. Clasificación financiera, 
10. Interpretación automática, 11. Clasificación de riesgo.
"""

import numpy_financial as npf
import numpy as np

# ===================================================
# 1. VPN (Valor Presente Neto)
# ===================================================
def calcular_vpn(tasa, flujos):
    try:
        vpn = npf.npv(tasa, flujos)
        return round(float(vpn), 2)
    except:
        return 0.0

# ===================================================
# 2. TIR (Tasa Interna de Retorno)
# ===================================================
def calcular_tir(flujos):
    try:
        tir = npf.irr(flujos)
        if tir is None or np.isnan(tir):
            return 0.0
        return round(float(tir), 4)
    except:
        return 0.0

# ===================================================
# 3. PAYBACK (Periodo de Recuperación)
# ===================================================
def calcular_payback(flujos):
    try:
        acumulado = 0
        for i, flujo in enumerate(flujos):
            acumulado += flujo
            if acumulado >= 0:
                return i  # Retorna el año en que el flujo se vuelve positivo
        return "No recuperado"
    except:
        return "Error en cálculo"

# ===================================================
# 4. RBC (Relación Beneficio/Costo)
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
            return 0.0
        return round(beneficios / costos, 2)
    except:
        return 0.0

# ===================================================
# 5. ROI (Retorno sobre Inversión)
# ===================================================
def calcular_roi(inversion, beneficios_totales):
    try:
        if inversion == 0:
            return 0.0
        roi = ((beneficios_totales - inversion) / inversion) * 100
        return round(roi, 2)
    except:
        return 0.0

# ===================================================
# 6. ÍNDICE DE RENTABILIDAD
# ===================================================
def indice_rentabilidad(vpn, inversion):
    try:
        if inversion == 0:
            return 0.0
        # IR = (VPN + Inversión) / Inversión
        indice = (vpn + inversion) / inversion
        return round(indice, 2)
    except:
        return 0.0

# ===================================================
# 7. PUNTO DE EQUILIBRIO
# ===================================================
def punto_equilibrio(costos_fijos, precio, costo_variable):
    try:
        if precio <= costo_variable:
            return 0.0
        pe = costos_fijos / (precio - costo_variable)
        return round(pe, 2)
    except:
        return 0.0

# ===================================================
# 8. MARGEN DE SEGURIDAD
# ===================================================
def margen_seguridad(ventas_actuales, ventas_equilibrio):
    try:
        if ventas_actuales == 0:
            return 0.0
        margen = ((ventas_actuales - ventas_equilibrio) / ventas_actuales) * 100
        return round(margen, 2)
    except:
        return 0.0

# ===================================================
# 9. SCORE FINANCIERO (Ponderación Gerenciarte)
# ===================================================
def score_financiero(vpn, tir, rbc, impacto):
    """
    Score compuesto ponderando VPN, TIR, RBC e Impacto Social.
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
        return 0.0

# ===================================================
# 10. CLASIFICACIÓN DEL PROYECTO
# ===================================================
def clasificacion_proyecto(vpn, tir, rbc):
    if vpn > 0 and tir > 0.20 and rbc > 1:
        return "Proyecto altamente viable"
    elif vpn > 0 and tir > 0.10:
        return "Proyecto viable"
    elif vpn > 0:
        return "Proyecto con viabilidad moderada"
    else:
        return "Proyecto no viable"

# ===================================================
# 11. CLASIFICACIÓN DE RIESGO
# ===================================================
def clasificar_riesgo(vpn, tir, rbc):
    riesgo_acumulado = 0.0
    
    if vpn <= 0:
        riesgo_acumulado += 0.5
    
    if tir < 0.10:
        riesgo_acumulado += 0.3
    elif tir < 0.20:
        riesgo_acumulado += 0.15
        
    if rbc < 1:
        riesgo_acumulado += 0.3

    if riesgo_acumulado >= 0.7:
        return "Alto"
    elif riesgo_acumulado >= 0.4:
        return "Moderado"
    else:
        return "Bajo"

# ===================================================
# INTERPRETACIÓN AUTOMÁTICA
# ===================================================
def interpretacion_financiera(vpn, tir, rbc):
    if vpn > 0 and tir > 0.20 and rbc > 1:
        return """
El proyecto presenta excelentes condiciones financieras.
La generación de valor es positiva, la rentabilidad es alta y los beneficios 
superan significativamente los costos.
"""
    elif vpn > 0:
        return """
El proyecto presenta viabilidad financiera aceptable.
Aunque genera valor económico, algunas variables financieras deben 
monitorearse cuidadosamente.
"""
    else:
        return """
El proyecto no presenta condiciones financieras favorables.
Se recomienda revisar costos, inversión inicial y estrategia financiera.
"""

# ===================================================
# RESUMEN EJECUTIVO
# ===================================================
def resumen_ejecutivo(nombre, vpn, tir, rbc, payback):
    return f"""
RESUMEN EJECUTIVO
Proyecto: {nombre}
VPN: ${vpn:,.2f}
TIR: {round(tir * 100, 2)}%
RBC: {rbc}
Payback: {payback}

CONCLUSIÓN:
El análisis permite evaluar la generación de valor, rentabilidad y 
sostenibilidad económica del proyecto.
"""