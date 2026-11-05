"""MEF lineal 1D suministrado. q y P positivos en +x; unidades N y mm."""
from dataclasses import dataclass
import numpy as np

@dataclass
class Resultado:
    x: np.ndarray
    u: np.ndarray
    reacciones: np.ndarray
    K: np.ndarray
    f: np.ndarray
    libres: np.ndarray
    fijos: np.ndarray

def resolver_barra(n, L, E, A, P, q, extremo_derecho_fijo=False):
    if not isinstance(n, int) or n < 1:
        raise ValueError("n debe ser entero positivo")
    if min(L, E, A) <= 0 or not np.isfinite([L,E,A,P,q]).all():
        raise ValueError("Datos no finitos o propiedades no positivas")
    x = np.linspace(0., L, n+1)
    K = np.zeros((n+1, n+1)); f = np.zeros(n+1)
    for e in range(n):
        h = x[e+1]-x[e]
        idx = [e, e+1]
        K[np.ix_(idx, idx)] += E*A/h*np.array([[1.,-1.],[-1.,1.]])
        f[idx] += q*h/2
    f[-1] += P
    fijos = np.array([0,n] if extremo_derecho_fijo else [0])
    libres = np.setdiff1d(np.arange(n+1), fijos)
    u = np.zeros(n+1)
    if libres.size:
        u[libres] = np.linalg.solve(K[np.ix_(libres,libres)],f[libres])
    # K y f originales: el residuo restringido contiene las reacciones.
    r = K@u-f
    return Resultado(x,u,r,K,f,libres,fijos)
