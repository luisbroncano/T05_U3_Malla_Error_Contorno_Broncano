"""Referencia analitica independiente y error de interpolacion entre nodos."""
import numpy as np


def desplazamiento_referencia(x, L, E, A, P, q):
    """Solucion exacta en mm para u(0)=0 y EA*u'(L)=P.

    Integra -(EA u')'=q, con E y A constantes:
        u(x) = [P*x + q*(L*x - x**2/2)]/(E*A).
    Acepta escalares o arreglos NumPy.
    """
    x = np.asarray(x, dtype=float)
    if L <= 0 or E <= 0 or A <= 0:
        raise ValueError("L, E y A deben ser positivos")
    if not np.isfinite(x).all() or not np.isfinite([L, E, A, P, q]).all():
        raise ValueError("Los argumentos deben ser finitos")
    if np.any((x < 0) | (x > L)):
        raise ValueError("Los puntos x deben pertenecer al intervalo [0, L]")
    return (P * x + q * (L * x - 0.5 * x**2)) / (E * A)


def error_puntos_medios(resultado, L, E, A, P, q):
    """Maximo error absoluto en los puntos medios, en mm.

    Compara la referencia con la interpolacion lineal de u_h dentro de
    cada elemento. Para una malla uniforme, los puntos medios se obtienen
    promediando las coordenadas y los desplazamientos nodales adyacentes.
    """
    x_nodos = np.asarray(resultado.x, dtype=float)
    u_nodos = np.asarray(resultado.u, dtype=float)
    if x_nodos.ndim != 1 or u_nodos.ndim != 1 or x_nodos.size != u_nodos.size:
        raise ValueError("resultado.x y resultado.u deben ser vectores compatibles")
    if x_nodos.size < 2:
        raise ValueError("Se requiere al menos un elemento")

    x_medios = 0.5 * (x_nodos[:-1] + x_nodos[1:])
    u_h_medios = 0.5 * (u_nodos[:-1] + u_nodos[1:])
    u_ref_medios = desplazamiento_referencia(x_medios, L, E, A, P, q)
    return float(np.max(np.abs(u_h_medios - u_ref_medios)))
