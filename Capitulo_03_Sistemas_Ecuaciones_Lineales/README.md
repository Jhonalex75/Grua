# Capítulo 3: Sistemas de Ecuaciones Lineales

Este capítulo aborda la resolución de sistemas de ecuaciones lineales, un problema fundamental en todas las ramas de la ingeniería. Estos sistemas surgen al modelar fenómenos como el equilibrio de fuerzas en estructuras, el análisis de circuitos eléctricos, o la distribución de temperaturas en un sólido.

## Contenido Teórico

Un sistema de ecuaciones lineales se puede representar en forma matricial como `Ax = b`, donde `A` es la matriz de coeficientes, `x` es el vector de incógnitas y `b` es el vector de términos independientes. Existen dos categorías principales de métodos para resolver estos sistemas:

*   **Métodos Directos:** Producen la solución en un número finito de pasos. Son precisos (limitados solo por errores de redondeo) y adecuados para sistemas pequeños a medianos.
*   **Métodos Iterativos:** Comienzan con una estimación inicial y la refinan progresivamente hasta alcanzar una solución con la precisión deseada. Son preferidos para sistemas muy grandes o dispersos (con muchos ceros).

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_eliminacion_gaussiana.py`

*   **Descripción:** Implementación del método de Eliminación Gaussiana, un método directo clásico que transforma el sistema en una forma triangular superior para luego resolverlo mediante sustitución hacia atrás.
*   **Conceptos Clave:** Matriz aumentada, pivoteo, eliminación hacia adelante, sustitución hacia atrás.

### `ejercicio_2_descomposicion_lu.py`

*   **Descripción:** Implementación de la Descomposición LU, que factoriza la matriz `A` en una matriz triangular inferior (`L`) y una superior (`U`). Es eficiente para resolver múltiples sistemas con la misma matriz `A` pero diferentes vectores `b`.
*   **Conceptos Clave:** Factorización de matrices, sustitución hacia adelante, sustitución hacia atrás, eficiencia computacional.

### `ejercicio_3_metodo_jacobi.py`

*   **Descripción:** Implementación del Método de Jacobi, un método iterativo que actualiza cada incógnita utilizando los valores de la iteración anterior. Es simple y útil para sistemas grandes y diagonalmente dominantes.
*   **Conceptos Clave:** Métodos iterativos, convergencia, diagonal dominante, actualización simultánea.

### `ejercicio_4_metodo_gauss_seidel.py`

*   **Descripción:** Implementación del Método de Gauss-Seidel, una mejora del método de Jacobi que utiliza los valores de las incógnitas recién calculados dentro de la misma iteración, lo que generalmente acelera la convergencia.
*   **Conceptos Clave:** Métodos iterativos, convergencia más rápida, actualización secuencial.
