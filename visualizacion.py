"""
MÓDULO DE VISUALIZACIÓN

Genera gráficas financieras avanzadas
para análisis de proyectos.
"""

import matplotlib.pyplot as plt

# =====================================================
# GRÁFICA VPN
# =====================================================

def grafica_vpn(proyectos, vpns):

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        proyectos,
        vpns
    )

    # LÍNEA CRÍTICA
    ax.axhline(
        0,
        color='red',
        linestyle='--',
        linewidth=2
    )

    ax.set_title(
        "Comparación del Valor Presente Neto"
    )

    ax.set_xlabel(
        "Proyectos"
    )

    ax.set_ylabel(
        "VPN"
    )

    ax.grid(True)

    return fig

# =====================================================
# GRÁFICA LINEAL
# =====================================================

def grafica_lineal(

    x,
    y,
    titulo,
    xlabel,
    ylabel

):

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        x,
        y,
        marker='o'
    )

    ax.axhline(
        0,
        color='red',
        linestyle='--'
    )

    ax.set_title(titulo)

    ax.set_xlabel(xlabel)

    ax.set_ylabel(ylabel)

    ax.grid(True)

    return fig