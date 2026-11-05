# Bitácora de trabajo

| Fecha | Predicción / decisión previa | Cambio realizado | Prueba y evidencia | Commit |
|---|---|---|---|---|
| 05-11-2026 | Antes de la corrida reproducible final se dejó asentado que la solución cuadrática debe coincidir en nodos con el MEF lineal; el error en puntos medios debe disminuir como h^2 (un cuarto al duplicar n). Con u(L)=0, el extremo pasa a desplazamiento cero y aparecen dos reacciones. | Se completaron únicamente `src/analisis.py` y el postproceso de `src/ejecutar.py`; se mantuvo `src/barra_mef.py` sin cambios. Se añadieron pruebas del análisis, CSV de resultados y desplazamientos, figuras y registros. | `registros/pytest.log`, `registros/ejecucion.log`, `salidas/resultados.csv`, `salidas/desplazamientos_nodales.csv`, `salidas/convergencia.png` y `salidas/contorno.png`. | Repositorio remoto: https://github.com/luisbroncano/T05_U3_Malla_Error_Contorno_Broncano. El hash del commit principal se registra en entrega.json. |

## Predicción previa (desarrollo analítico)

Para el problema base se anticipó `u(L)=0.300000 mm` en las tres mallas y un error máximo en puntos medios `q h^2/(8 E A)`: 0.006250, 0.0015625 y 0.000390625 mm para n=2, 4 y 8. Para el contorno con ambos extremos fijos se anticiparon `R_izq=-10000 N` y `R_der=-30000 N`.

**Nota de autoría:** la predicción fue formulada analíticamente antes de la corrida reproducible registrada en los logs; la asistencia de IA ayudó a redactarla. El estudiante debe revisarla y poder justificarla en la microdefensa.
