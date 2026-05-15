"""
MÓDULO: VISUALIZACIÓN AVANZADA

Este módulo genera representaciones gráficas avanzadas
para facilitar la interpretación financiera y estratégica
de los proyectos evaluados.

Incluye:
- Comparación entre proyectos
- Sensibilidad del VPN
- Punto crítico de viabilidad
- Líneas de referencia financiera
"""

import matplotlib.pyplot as plt

# -----------------------------------------
# GRÁFICA COMPARACIÓN VPN
# -----------------------------------------

def grafica_vpn(proyectos, vpns):

    plt.figure(figsize=(10,6))

    barras = plt.bar(
        proyectos,
        vpns
    )

    # Línea de equilibrio financiero
    plt.axhline(
        y=0,
        color='red',
        linestyle='--',
        linewidth=2,
        label='VPN = 0 (Punto de equilibrio)'
    )

    # Etiquetas sobre barras
    for barra in barras:

        altura = barra.get_height()

        plt.text(
            barra.get_x() + barra.get_width()/2,
            altura,
            f'{round(altura,2)}',
            ha='center',
            va='bottom'
        )

    plt.title(
        "Comparación del Valor Presente Neto (VPN)",
        fontsize=16,
        fontweight='bold'
    )

    plt.xlabel(
        "Proyectos evaluados",
        fontsize=12
    )

    plt.ylabel(
        "Valor Presente Neto (VPN)",
        fontsize=12
    )

    plt.grid(
        axis='y',
        linestyle='--',
        alpha=0.5
    )

    plt.legend()

    plt.tight_layout()

    plt.show()

# -----------------------------------------
# GRÁFICA SENSIBILIDAD VPN
# -----------------------------------------

def grafica_lineal(x, y, titulo, xlabel, ylabel):

    plt.figure(figsize=(10,6))

    plt.plot(
        x,
        y,
        marker='o',
        linewidth=3
    )

    # Línea horizontal VPN = 0
    plt.axhline(
        y=0,
        color='red',
        linestyle='--',
        linewidth=2,
        label='VPN = 0'
    )

    # Buscar punto crítico
    punto_critico = None

    for i in range(len(y)-1):

        if y[i] > 0 and y[i+1] < 0:

            punto_critico = x[i+1]

    # Línea vertical punto crítico
    if punto_critico is not None:

        plt.axvline(
            x=punto_critico,
            color='darkred',
            linestyle=':',
            linewidth=3,
            label=f'Tasa límite ≈ {round(punto_critico,2)}%'
        )

        plt.scatter(
            punto_critico,
            0,
            s=120
        )

    plt.title(
        titulo,
        fontsize=16,
        fontweight='bold'
    )

    plt.xlabel(
        xlabel,
        fontsize=12
    )

    plt.ylabel(
        ylabel,
        fontsize=12
    )

    plt.grid(
        linestyle='--',
        alpha=0.5
    )

    plt.legend()

    plt.tight_layout()

    plt.show()