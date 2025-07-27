# Capítulo 6: Ecuaciones Diferenciales Ordinarias (EDO)

Este capítulo se dedica a la resolución numérica de Ecuaciones Diferenciales Ordinarias (EDO), que son fundamentales para modelar sistemas dinámicos en ingeniería. Las EDOs describen cómo una cantidad cambia con respecto a otra, y su solución nos permite predecir el comportamiento de sistemas a lo largo del tiempo o el espacio.

## Contenido Teórico

*   **Problemas de Valor Inicial (PVI):** Una EDO junto con una condición inicial que especifica el estado del sistema en un punto de partida. Los métodos numéricos resuelven estas EDOs "paso a paso" desde la condición inicial.
*   **Sistemas de EDOs:** Muchos problemas de ingeniería requieren múltiples EDOs interconectadas para describir su comportamiento. Los métodos numéricos pueden extenderse para resolver estos sistemas.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_metodo_euler.py`

*   **Descripción:** Implementación del Método de Euler, el método numérico más simple para resolver EDOs. Es didáctico para entender el concepto de integración paso a paso, aunque su precisión es limitada.
*   **Conceptos Clave:** Aproximación lineal, tamaño de paso, error acumulado, integración paso a paso.

### `ejercicio_2_metodo_runge_kutta_4.py`

*   **Descripción:** Implementación del Método de Runge-Kutta de 4to Orden (RK4), un método mucho más preciso y robusto que Euler. Incluye una implementación genérica de RK4 para sistemas de EDOs, que es altamente reutilizable.
*   **Conceptos Clave:** Mayor precisión, promedio ponderado de pendientes, estabilidad, método de uso común.

### `ejercicio_3_sistemas_edos.py`

*   **Descripción:** Demuestra cómo extender el método RK4 para resolver sistemas de EDOs acopladas. Se utiliza un ejemplo de oscilador armónico para ilustrar la simulación de múltiples variables dependientes.
*   **Conceptos Clave:** EDOs acopladas, vector de estado, espacio de fase, simulación de sistemas dinámicos.

### `ejercicio_4_scipy_solve_ivp.py`

*   **Descripción:** Muestra cómo utilizar la función `solve_ivp` de la biblioteca SciPy, la herramienta estándar y más eficiente para resolver problemas de valor inicial de EDOs en Python. Permite resolver sistemas complejos con alta precisión y control.
*   **Conceptos Clave:** `scipy.integrate.solve_ivp`, métodos adaptativos, robustez, eficiencia, solución de problemas de ingeniería a gran escala.

### `ejercicio_5_sistema_masa_resorte_amortiguador.py`

*   **Descripción:** Aplica el solucionador RK4 genérico para simular el comportamiento de un sistema masa-resorte-amortiguador, un problema clásico de ingeniería mecánica. Demuestra la conversión de una EDO de segundo orden a un sistema de primer orden.
*   **Conceptos Clave:** Modelado de sistemas físicos, conversión de EDOs de orden superior, simulación de vibraciones, aplicación práctica de RK4.
