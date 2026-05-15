"""
MÓDULO: SIMULACIÓN MONTE CARLO

Permite ejecutar miles de escenarios
probabilísticos para medir riesgo financiero.
"""

import numpy as np
import numpy_financial as npf

def simulacion_montecarlo(
    flujos,
    tasa,
    simulaciones=5000,
    variacion=0.15
):

    resultados = []

    for _ in range(simulaciones):

        flujos_simulados = [flujos[0]]

        for flujo in flujos[1:]:

            cambio = np.random.normal(
                1,
                variacion
            )

            nuevo_flujo = flujo * cambio

            flujos_simulados.append(
                nuevo_flujo
            )

        vpn = npf.npv(
            tasa,
            flujos_simulados
        )

        resultados.append(vpn)

    resultados = np.array(resultados)

    return {

        "vpns": resultados,

        "vpn_promedio": round(
            np.mean(resultados),
            2
        ),

        "vpn_min": round(
            np.min(resultados),
            2
        ),

        "vpn_max": round(
            np.max(resultados),
            2
        ),

        "desviacion": round(
            np.std(resultados),
            2
        ),

        "probabilidad_exito": round(
            (
                np.sum(resultados > 0)
                / simulaciones
            ) * 100,
            2
        )
    }