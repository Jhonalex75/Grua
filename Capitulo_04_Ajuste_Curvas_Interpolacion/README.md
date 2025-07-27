# Capítulo 4: Ajuste de Curvas e Interpolación

Este capítulo explora técnicas para modelar relaciones entre datos. El **ajuste de curvas** busca una función que represente la tendencia general de un conjunto de datos (a menudo experimentales), mientras que la **interpolación** estima valores entre puntos de datos conocidos, asegurando que la curva pase exactamente por esos puntos.

## Contenido Teórico

*   **Ajuste de Curvas:** Se utiliza cuando los datos tienen ruido o dispersión, y se busca una relación subyacente que no necesariamente pase por todos los puntos. La regresión lineal es un ejemplo común.
*   **Interpolación:** Se usa cuando se asume que los datos son precisos y se necesita una estimación exacta en puntos intermedios. Es útil para rellenar huecos en tablas o para suavizar trayectorias.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_regresion_lineal.py`

*   **Descripción:** Implementación de la Regresión Lineal por el método de Mínimos Cuadrados, que encuentra la línea recta que mejor se ajusta a un conjunto de datos, minimizando la suma de los cuadrados de los errores.
*   **Conceptos Clave:** Mínimos cuadrados, línea de mejor ajuste, pendiente, intercepto, modelado de tendencias.

### `ejercicio_2_interpolacion_lineal.py`

*   **Descripción:** Implementación de la Interpolación Lineal, la forma más sencilla de estimar un valor entre dos puntos de datos conocidos, asumiendo una relación lineal entre ellos.
*   **Conceptos Clave:** Estimación entre puntos, segmentos de línea recta, tablas de datos.

### `ejercicio_3_interpolacion_lagrange.py`

*   **Descripción:** Implementación de la Interpolación Polinomial de Lagrange, que construye un único polinomio que pasa exactamente por todos los puntos de datos dados. Útil para obtener una curva suave que interpole todos los puntos.
*   **Conceptos Clave:** Polinomio interpolador, polinomios base de Lagrange, paso exacto por puntos.

### `ejercicio_4_splines_cubicos.py`

*   **Descripción:** Introducción a los Splines Cúbicos, que ajustan polinomios de tercer grado entre cada par de puntos de datos, asegurando una unión suave y continua. Son ideales para evitar oscilaciones indeseadas de polinomios de alto grado.
*   **Conceptos Clave:** Suavidad, continuidad de derivadas, evitación del fenómeno de Runge, `scipy.interpolate.CubicSpline`.
