"""
MÓDULO: INDICADORES FINANCIEROS AVANZADOS
Versión: 2.0 (Blindada contra errores de tipo)
"""

import numpy_financial as npf
import numpy as np

# ===================================================
# FUNCIONES DE APOYO (BLINDAJE)
# ===================================================
def _limpiar_numero(valor):
    """Asegura que el valor sea un float válido."""
    try:
        if valor is None: return 0.0
        # Convertir de numpy.float64 u otros a float nativo
        num = float(valor)
        if np.isnan(num) or np.isinf(num): return 0.0
        return num
    except:
        return 0.0

# ===================================================
# VPN
# ===================================================
def calcular_vpn(tasa, flujos):
    try:
        vpn = npf.npv(tasa, flujos)
        return round(_limpiar_numero(vpn), 2)
    except:
        return 0.0

# ===================================================
# TIR
# ===================================================
def calcular_tir(flujos):
    try:
        tir = npf.irr(flujos)
        return _limpiar_numero(tir)
    except:
        return 0.0

# ===================================================
# PAYBACK
# ===================================================
def calcular_payback(flujos):
    try:
        acumulado = 0
        for i, flujo in enumerate(flujos):
            acumulado += flujo
            if acumulado >= 0:
                return i
        return "No recuperado"
    except:
        return "Error"

# ===================================================
# RBC
# ===================================================
def calcular_rbc(tasa, flujos):
    try:
        beneficios = 0
        costos = 0
        for i, f in enumerate(flujos):
            valor_actual = f / ((1 + tasa) ** i)
            if f > 0: beneficios += valor_actual
            else: costos += abs(valor_actual)
        
        if costos == 0: return 0.0
        return round(beneficios / costos, 2)
    except:
        return 0.0

# ===================================================
# ROI
# ===================================================
def calcular_roi(inversion, beneficios_totales):
    try:
        inv = _limpiar_numero(inversion)
        if inv == 0: return 0.0
        roi = ((beneficios_totales - inv) / inv) * 100
        return round(roi, 2)
    except:
        return 0.0

# ===================================================
# ÍNDICE RENTABILIDAD
# ===================================================
def indice_rentabilidad(vpn, inversion):
    try:
        inv = _limpiar_numero(inversion)
        if inv == 0: return 0.0
        indice = (vpn + inv) / inv
        return round(indice, 2)
    except:
        return 0.0

# ===================================================
# SCORE FINANCIERO
# ===================================================
def score_financiero(vpn, tir, rbc, impacto):
    try:
        # Ponderación basada en el modelo de negocio
        score = (
            _limpiar_numero(vpn) * 0.5
            + (_limpiar_numero(tir) * 100) * 10000
            + _limpiar_numero(rbc) * 50000
            + _limpiar_numero(impacto) * 1000000
        )
        return round(score, 2)
    except:
        return 0.0

# ===================================================
# CLASIFICACIÓN DE RIESGO (CORREGIDA)
# ===================================================
def clasificar_riesgo(vpn, tir, rbc):
    # Forzamos conversión a float para evitar el TypeError en la comparación
    v = _limpiar_numero(vpn)
    t = _limpiar_numero(tir)
    r = _limpiar_numero(rbc)
    
    riesgo_puntos = 0.0
    
    if v <= 0:
        riesgo_puntos += 0.5
    
    if t < 0.10:
        riesgo_puntos += 0.3
    elif t < 0.20:
        riesgo_puntos += 0.15
        
    if r < 1:
        riesgo_puntos += 0.3

    if riesgo_puntos >= 0.7:
        return "Alto"
    elif riesgo_puntos >= 0.4:
        return "Moderado"
    else:
        return "Bajo"

# ===================================================
# CLASIFICACIÓN PROYECTO
# ===================================================
def clasificacion_proyecto(vpn, tir, rbc):
    v = _limpiar_numero(vpn)
    t = _limpiar_numero(tir)
    r = _limpiar_numero(rbc)
    
    if v > 0 and t > 0.20 and r > 1:
        return "Proyecto altamente viable"
    elif v > 0 and t > 0.10:
        return "Proyecto viable"
    elif v > 0:
        return "Proyecto con viabilidad moderada"
    else:
        return "Proyecto no viable"

# ===================================================
# INTERPRETACIÓN Y RESUMEN
# ===================================================
def interpretacion_financiera(vpn, tir, rbc):
    v = _limpiar_numero(vpn)
    if v > 0:
        return "El proyecto genera valor económico positivo."
    return "El proyecto no genera valor suficiente bajo las tasas actuales."

def resumen_ejecutivo(nombre, vpn, tir, rbc, payback):
    return f"Resumen: {nombre} | VPN: {vpn} | TIR: {round(tir*100,2)}% | RBC: {rbc}"