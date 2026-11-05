"""Ejecuta las tres mallas y el caso con contorno alterado."""
import csv
import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from barra_mef import resolver_barra
from analisis import error_puntos_medios

ROOT = Path(__file__).resolve().parents[1]
TOL_BALANCE_REL = 1e-8


def fila_resultado(caso, n, r, error, P, q, L):
    """Arma metricas de equilibrio usando K y f sin modificar."""
    balance = float(np.sum(r.reacciones[r.fijos]) + np.sum(r.f))
    carga_total = abs(P + q * L)
    balance_rel = abs(balance) / carga_total if carga_total else abs(balance)
    residuo_libre = float(np.max(np.abs(r.reacciones[r.libres]))) if r.libres.size else 0.0
    if balance_rel > TOL_BALANCE_REL:
        raise AssertionError(
            f"El balance relativo {balance_rel:.3e} supera {TOL_BALANCE_REL:.1e}"
        )
    return {
        "caso": caso,
        "n": n,
        "u_L_mm": float(r.u[-1]),
        "R_izq_N": float(r.reacciones[0]),
        "R_der_N": float(r.reacciones[-1]),
        "balance_N": balance,
        "balance_relativo": balance_rel,
        "residuo_libre_max_N": residuo_libre,
        "error_medio_mm": "" if error is None else float(error),
    }


def guardar_desplazamientos(kw, mallas, out):
    """Guarda desplazamientos nodales del modelo base y del contorno alterado."""
    with (out / "desplazamientos_nodales.csv").open("w", newline="", encoding="utf-8") as f:
        campos = ["caso", "n", "nodo", "x_mm", "u_mef_mm", "u_ref_base_mm"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for n in mallas:
            r = resolver_barra(n, **kw)
            u_ref = (kw["P"] * r.x + kw["q"] * (kw["L"] * r.x - 0.5 * r.x**2)) / (kw["E"] * kw["A"])
            for i, (x_i, u_i, u_r) in enumerate(zip(r.x, r.u, u_ref)):
                writer.writerow({"caso": "BASE", "n": n, "nodo": i,
                                 "x_mm": float(x_i), "u_mef_mm": float(u_i),
                                 "u_ref_base_mm": float(u_r)})
        r_alt = resolver_barra(8, **kw, extremo_derecho_fijo=True)
        u_ref = (kw["P"] * r_alt.x + kw["q"] * (kw["L"] * r_alt.x - 0.5 * r_alt.x**2)) / (kw["E"] * kw["A"])
        for i, (x_i, u_i, u_r) in enumerate(zip(r_alt.x, r_alt.u, u_ref)):
            writer.writerow({"caso": "BC_ALTERADO", "n": 8, "nodo": i,
                             "x_mm": float(x_i), "u_mef_mm": float(u_i),
                             "u_ref_base_mm": float(u_r)})


def guardar_esquema(kw, out):
    """Dibuja el contorno original y la restriccion adicional estudiada."""
    fig, ax = plt.subplots(figsize=(8.0, 2.3))
    ax.plot([0.08, 0.92], [0.52, 0.52], color="black", linewidth=5, solid_capstyle="butt")
    # Apoyo izquierdo original.
    ax.plot([0.08, 0.08], [0.34, 0.70], color="black", linewidth=2)
    for yy in np.linspace(0.35, 0.68, 7):
        ax.plot([0.035, 0.08], [yy - 0.045, yy], color="black", linewidth=0.8)
    ax.text(0.08, 0.20, r"$u(0)=0$", ha="center", va="top", fontsize=10)
    # Carga axial distribuida hacia +x.
    for xx in np.linspace(0.19, 0.79, 6):
        ax.annotate("", xy=(xx + 0.045, 0.82), xytext=(xx, 0.82),
                    arrowprops=dict(arrowstyle="->", lw=1.1, color="black"))
    ax.text(0.49, 0.91, r"$q=10\;\mathrm{N/mm}$ hacia $+x$", ha="center", fontsize=10)
    # Carga puntual en el extremo libre original.
    ax.annotate("", xy=(0.99, 0.52), xytext=(0.92, 0.52),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="black"))
    ax.text(0.96, 0.64, r"$P=20\;\mathrm{kN}$", ha="center", fontsize=10)
    ax.text(0.92, 0.20, r"$EAu'(L)=P$", ha="center", va="top", fontsize=10)
    # Restriccion agregada, solo para el caso alternativo.
    ax.plot([0.92, 0.92], [0.34, 0.70], color="tab:red", linewidth=1.8, linestyle="--")
    ax.text(0.78, 0.06, r"Caso alternativo: se agrega $u(L)=0$", color="tab:red", ha="center", fontsize=9)
    ax.text(0.08, 0.52, "", ha="center")
    ax.set_xlim(0, 1.04); ax.set_ylim(0, 1.02); ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(out / "contorno.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main():
    p = json.loads((ROOT / "datos/barra.json").read_text(encoding="utf-8"))
    kw = dict(L=p["L_mm"], E=p["E_MPa"], A=p["A_mm2"], P=p["P_N"], q=p["q_N_mm"])
    rows = []
    errores = []

    for n in p["mallas"]:
        r = resolver_barra(n, **kw)
        err = error_puntos_medios(r, **kw)
        if not np.isfinite(err) or err <= 0:
            raise ValueError("El error de campo debe ser finito y positivo")
        rows.append(fila_resultado(f"M{n}", n, r, err, kw["P"], kw["q"], kw["L"]))
        errores.append(err)

    # Se agrega u(L)=0 sin cambiar P ni q: es un problema de borde distinto.
    r_alt = resolver_barra(8, **kw, extremo_derecho_fijo=True)
    rows.append(fila_resultado("BC_ALTERADO", 8, r_alt, None, kw["P"], kw["q"], kw["L"]))

    out = ROOT / "salidas"
    out.mkdir(exist_ok=True)
    guardar_desplazamientos(kw, p["mallas"], out)
    guardar_esquema(kw, out)
    campos = list(rows[0])
    with (out / "resultados.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(rows)

    n_values = p["mallas"]
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    ax.semilogy(n_values, errores, "o-", linewidth=1.8, markersize=6, label="Error calculado")
    ax.semilogy(n_values, [errores[0] * (n_values[0] / n) ** 2 for n in n_values],
              "--", linewidth=1.2, label=r"Referencia $\propto n^{-2}$")
    for n, err in zip(n_values, errores):
        ax.annotate(f"{err:.3g} mm", (n, err), xytext=(5, 7), textcoords="offset points", fontsize=8)
    ax.set(xlabel="Numero de elementos, n [-]", ylabel="Error maximo en puntos medios [mm]",
           title="Convergencia del error entre nodos")
    ax.grid(True, which="both", alpha=0.35)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out / "convergencia.png", dpi=220)
    plt.close(fig)

    versions = (
        f"Python={platform.python_version()}\n"
        f"NumPy={np.__version__}\n"
        f"Matplotlib={matplotlib.__version__}\n"
        f"Tolerancia_balance_relativo={TOL_BALANCE_REL:.1e}\n"
    )
    (out / "versiones.txt").write_text(versions, encoding="utf-8")
    print(f"Resultados guardados en {out}")
    print(f"Balance relativo maximo: {max(row['balance_relativo'] for row in rows):.3e}")
    print(f"Residuo libre maximo: {max(row['residuo_libre_max_N'] for row in rows):.3e} N")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
