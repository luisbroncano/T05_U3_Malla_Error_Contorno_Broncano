# Declaración de uso de IA

Se utilizó ChatGPT (modelo GPT-6), el 05-11-2026, como asistencia permitida para el trabajo de laboratorio y la preparación del informe.

- **Propósito:** derivar la solución analítica del problema de borde, implementar las funciones pendientes de referencia y error en puntos medios, ampliar el registro de resultados y redactar una primera versión del análisis y del informe LaTeX.
- **Bloques utilizados:** expresión de `u_ref(x)`; interpolación lineal del campo MEF en los puntos medios; comprobación del residuo `K @ u - f`; contraste con `u(L)=0`; generación de tabla, gráfico y texto de conclusión.
- **Verificación independiente ejecutada:** `python -m pytest -q` (5 pruebas aprobadas) y `python src/ejecutar.py`. Se comprobó que los desplazamientos nodales coinciden con la referencia, que el error medido sigue `q h^2/(8EA)`, y que el balance relativo máximo es `9.095e-16`, menor que `1e-8`.
- **Correcciones / límites:** se mantuvo sin cambios el solver suministrado `src/barra_mef.py`; se distinguió el residuo en grados libres de las reacciones en grados restringidos. Los resultados son una verificación numérica del modelo lineal elástico dado, no una validación experimental ni una simulación MAPDL.
- **Responsabilidad:** el estudiante debe leer, verificar y ser capaz de explicar cada ecuación, función, resultado y decisión incluida antes de entregar.
