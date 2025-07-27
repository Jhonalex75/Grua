# Capítulo 5: Diferenciación e Integración Numérica

Este capítulo se centra en cómo aproximar derivadas e integrales de funciones utilizando métodos numéricos. Esto es crucial cuando las funciones son complejas, no se conocen analíticamente (por ejemplo, provienen de datos experimentales), o cuando la integración/diferenciación analítica es imposible o muy difícil.

## Contenido Teórico

*   **Diferenciación Numérica:** Estima la tasa de cambio de una función a partir de un conjunto de puntos de datos. Es útil para calcular velocidades, aceleraciones o pendientes cuando solo se tienen mediciones discretas.
*   **Integración Numérica:** Aproxima el área bajo una curva (la integral definida) a partir de una función o un conjunto de datos. Es fundamental para calcular cantidades acumuladas como trabajo, impulso, volumen o centroides.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_diferenciacion_numerica.py`

*   **Descripción:** Implementa las fórmulas de diferencia hacia adelante, hacia atrás y central para aproximar la derivada de una función. Se compara la precisión de cada método.
*   **Conceptos Clave:** Aproximación de la derivada, tamaño de paso (h), error de truncamiento.

### `ejercicio_2_integracion_trapecio.py`

*   **Descripción:** Implementa la Regla del Trapecio para la integración numérica, que aproxima el área bajo la curva dividiéndola en trapecios. Es un método simple y visualmente intuitivo.
*   **Conceptos Clave:** Área bajo la curva, subintervalos, aproximación lineal, suma de áreas.

### `ejercicio_3_integracion_simpson.py`

*   **Descripción:** Implementa la Regla de Simpson 1/3, un método de integración numérica más preciso que el trapecio, ya que aproxima la función con parábolas. Requiere un número par de subintervalos.
*   **Conceptos Clave:** Aproximación parabólica, mayor precisión, número par de subintervalos.

### `ejercicio_4_integracion_scipy.py`

*   **Descripción:** Demuestra el uso de las funciones de integración numérica optimizadas de la biblioteca SciPy (`scipy.integrate.quad`, `scipy.integrate.simpson`, `scipy.integrate.trapezoid`), que son las herramientas preferidas en la práctica de ingeniería.
*   **Conceptos Clave:** Bibliotecas científicas, `scipy.integrate`, `quad` (para funciones), `simpson` y `trapezoid` (para datos discretos), eficiencia y robustez.
