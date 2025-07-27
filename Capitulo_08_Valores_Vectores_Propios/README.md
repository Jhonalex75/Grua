# Capítulo 8: Valores y Vectores Propios (Eigenvalores y Eigenvectores)

Este capítulo introduce los conceptos de valores y vectores propios, que son fundamentales en muchas áreas de la ingeniería mecánica, como el análisis de vibraciones, la estabilidad de sistemas, la mecánica cuántica y el análisis de esfuerzos. Comprender estos conceptos nos permite identificar las características intrínsecas de un sistema.

## Contenido Teórico

Los valores y vectores propios surgen en el contexto de transformaciones lineales representadas por matrices. Un **vector propio** de una matriz es un vector no nulo que, cuando la matriz lo multiplica, solo cambia su escala (se estira o encoge), pero no su dirección. El factor por el cual se escala se llama **valor propio**.

*   **Definición:** Para una matriz cuadrada `A`, un vector `v` es un vector propio si `Av = λv`, donde `λ` es el valor propio correspondiente.
*   **Significado Físico:** En sistemas dinámicos, los valores propios a menudo representan frecuencias naturales o tasas de decaimiento/crecimiento. Los vectores propios describen los modos de vibración o las direcciones principales de deformación.
*   **Cálculo:** Encontrar los valores propios implica resolver el polinomio característico `det(A - λI) = 0`, donde `I` es la matriz identidad. Una vez que se tienen los valores propios, se pueden encontrar los vectores propios resolviendo el sistema lineal `(A - λI)v = 0`.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_introduccion_eigen.py`

*   **Descripción:** Introduce los conceptos de valores y vectores propios con un ejemplo simple de una matriz 2x2. Se muestra cómo una matriz "estira" o "encoge" un vector propio sin cambiar su dirección.
*   **Conceptos Clave:** Transformación lineal, vector propio, valor propio, visualización de la transformación.

### `ejercicio_2_calculo_numpy.py`

*   **Descripción:** Demuestra cómo calcular valores y vectores propios de matrices utilizando la función `np.linalg.eig` de NumPy. Se aplica a matrices de mayor tamaño y se verifica la relación `Av = λv`.
*   **Conceptos Clave:** `numpy.linalg.eig`, verificación de la ecuación de valores propios, eficiencia computacional.

### `ejercicio_3_aplicacion_vibraciones.py`

*   **Descripción:** Aplica el concepto de valores y vectores propios al análisis de vibraciones de un sistema masa-resorte simple. Los valores propios representan las frecuencias naturales y los vectores propios los modos de vibración.
*   **Conceptos Clave:** Frecuencias naturales, modos de vibración, matriz de masa, matriz de rigidez, sistemas dinámicos.

### `ejercicio_4_aplicacion_esfuerzos.py`

*   **Descripción:** Utiliza valores y vectores propios para determinar los esfuerzos principales y las direcciones principales en un estado de esfuerzo plano. Esto es fundamental en el análisis de resistencia de materiales.
*   **Conceptos Clave:** Esfuerzos principales, direcciones principales, círculo de Mohr (conceptual), tensor de esfuerzos.
