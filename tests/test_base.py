import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from barra_mef import resolver_barra

def test_control_sin_carga_distribuida():
    r=resolver_barra(2,L=100.,E=1000.,A=10.,P=20.,q=0.)
    assert np.isclose(r.u[-1],0.2)
    assert np.isclose(r.reacciones[0],-20.)

def test_equilibrio_con_contorno_alterado():
    r=resolver_barra(4,L=100.,E=1000.,A=10.,P=20.,q=1.,extremo_derecho_fijo=True)
    assert abs(r.reacciones[r.fijos].sum()+r.f.sum())<1e-8
    assert r.u[-1]==0
