# Capítulo 2: Raíces de Ecuaciones

Este capítulo se enfoca en métodos numéricos para encontrar las "raíces" o "ceros" de una función, es decir, los valores de `x` para los cuales `f(x) = 0`. Estos problemas son comunes en ingeniería cuando las ecuaciones no pueden resolverse analíticamente.

## Contenido Teórico

Los métodos de búsqueda de raíces son algoritmos iterativos que, partiendo de una o más estimaciones iniciales, refinan progresivamente la aproximación a la raíz. Se dividen en métodos de intervalo (que requieren que la raíz esté acotada entre dos puntos) y métodos abiertos (que no requieren acotamiento, pero pueden no converger).

*   **Raíz de una Función:** Valor de `x` donde la función cruza el eje horizontal.
*   **Métodos de Intervalo:** Garantizan convergencia si la función es continua y el intervalo inicial es válido.
*   **Métodos Abiertos:** Generalmente más rápidos, pero la convergencia no está garantizada y pueden divergir si la estimación inicial es pobre.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_metodo_biseccion.py`

*   **Descripción:** Implementación del Método de Bisección, un método de intervalo robusto que divide repetidamente el intervalo a la mitad. Incluye una versión didáctica y una versión más reutilizable.
*   **Conceptos Clave:** Teorema del Valor Intermedio, convergencia garantizada, lentitud relativa, intervalos.

### `ejercicio_2_metodo_newton_raphson.py`

*   **Descripción:** Implementación del Método de Newton-Raphson, un método abierto que utiliza la derivada de la función para una convergencia rápida. Se discuten sus ventajas y desventajas.
*   **Conceptos Clave:** Derivada, tangente, convergencia cuadrática, sensibilidad a la estimación inicial, divergencia.

### `ejercicio_3_metodo_secante.py`

*   **Descripción:** Implementación del Método de la Secante, una alternativa a Newton-Raphson que no requiere el cálculo analítico de la derivada, aproximándola con una línea secante entre dos puntos.
*   **Conceptos Clave:** Aproximación de la derivada, dos puntos iniciales, convergencia superlineal.

### `ejercicio_4_metodo_falsa_posicion.py`

*   **Descripción:** Implementación del Método de la Falsa Posición (Regula Falsi), que combina la robustez de Bisección con la idea de la Secante para mejorar la velocidad de convergencia, manteniendo el acotamiento de la raíz.
*   **Conceptos Clave:** Combinación de métodos, convergencia garantizada, mejora sobre Bisección.
