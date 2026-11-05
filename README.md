# T05 | Malla, error de campo y condiciones de borde

**Autor:** Luis Angel Broncano Marcelo  
**Carrera:** Ingeniería Civil en Obras Civiles — Universidad de Santiago de Chile (USACH)

Proyecto reproducible del Test 1 de la Unidad 3. Se estudia una barra axial lineal elástica mediante MEF unidimensional, se contrasta contra una referencia analítica independiente y se examina el efecto de agregar la restricción (u(L)=0).

## Reproducción

Con Python 3.10 o superior, desde la raíz:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python src/ejecutar.py
```

Para compilar el informe desde `informe/`:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

El informe usa tamaño A4, 11 puntos y márgenes de 2,4 cm. La bibliografía está en BibTeX. El PDF final para Moodle se incluye en el ZIP de entrega, junto con las fuentes y las figuras.

## Problema y resultados de referencia

Datos: (L=2000 mathrm{mm}), (E=200000 mathrm{N/mm^2}), (A=1000 mathrm{mm^2}), (P=20000 mathrm{N}), (q=10 mathrm{N/mm}). El contorno base es (u(0)=0) y (EAu'(L)=P).

```
u_ref(x) = [P*x + q*(L*x - x**2/2)]/(E*A)
u_ref(L) = 0.300000 mm
```

| n | h (mm) | u(L) (mm) | Error máximo en puntos medios (mm) |
|---:|---:|---:|---:|
| 2 | 1000 | 0,300000 | 0,006250 |
| 4 | 500 | 0,300000 | 0,0015625 |
| 8 | 250 | 0,300000 | 0,000390625 |

Con (u(L)=0) adicional y ocho elementos, el problema de borde cambia: (u(L)=0), (R_0=-10000 mathrm{N}) y (R_L=-30000 mathrm{N}). El cierre del equilibrio no convierte el contorno alterado en el problema original.

## Estructura

- `src/`: solver MEF suministrado, referencia y análisis de resultados.
- `datos/`: parámetros del problema.
- `salidas/`: CSV de resultados nodales y por malla, figuras y versiones.
- `tests/`: cinco pruebas automatizadas.
- `informe/`: fuente LaTeX, BibTeX y figuras.
- `registros/`: ejecución, pruebas y versiones del entorno.
- `BITACORA.md`, `USO_IA.md`, `REFERENCIAS.md`, `entrega.json`: trazabilidad.

## Alcance y uso de IA

Se utilizó asistencia de IA para la derivación, implementación de funciones de análisis y preparación del informe, registrada en `USO_IA.md`. Se conservaron las funciones del solver suministrado en `src/barra_mef.py`. Las pruebas verifican consistencia numérica; no constituyen validación experimental ni una ejecución de MAPDL. El autor debe revisar y poder explicar todo lo entregado.

## Repositorio

https://github.com/luisbroncano/T05_U3_Malla_Error_Contorno_Broncano

La URL y el hash completo del commit principal están en `entrega.json`.
