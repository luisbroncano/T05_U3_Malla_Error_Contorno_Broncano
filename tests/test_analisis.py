import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
from analisis import desplazamiento_referencia, error_puntos_medios
from barra_mef import resolver_barra

PARAM = dict(L=2000.0, E=200000.0, A=1000.0, P=20000.0, q=10.0)


def test_referencia_en_los_extremos():
    assert desplazamiento_referencia(0.0, **PARAM) == 0.0
    assert np.isclose(desplazamiento_referencia(PARAM["L"], **PARAM), 0.3)


def test_nodos_coinciden_y_error_es_cuadratico():
    for n in (2, 4, 8):
        r = resolver_barra(n, **PARAM)
        u_ref = desplazamiento_referencia(r.x, **PARAM)
        assert np.allclose(r.u, u_ref, rtol=1e-12, atol=1e-13)
        esperado = PARAM["q"] * (PARAM["L"] / n) ** 2 / (8 * PARAM["E"] * PARAM["A"])
        assert np.isclose(error_puntos_medios(r, **PARAM), esperado, rtol=1e-10)


def test_reacciones_del_contorno_alterado():
    r = resolver_barra(8, **PARAM, extremo_derecho_fijo=True)
    assert r.u[-1] == 0.0
    assert np.isclose(r.reacciones[0], -10000.0)
    assert np.isclose(r.reacciones[-1], -30000.0)
