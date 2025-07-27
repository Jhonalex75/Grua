# Capítulo 9: Problemas de Valor en la Frontera (PVF)

Este capítulo se enfoca en la resolución numérica de Ecuaciones Diferenciales Ordinarias (EDO) que son **Problemas de Valor en la Frontera (PVF)**. A diferencia de los Problemas de Valor Inicial (PVI) donde todas las condiciones se conocen en un solo punto (el inicio), en los PVF las condiciones se especifican en dos o más puntos diferentes, generalmente en los límites o "fronteras" del dominio.

## Contenido Teórico

Los PVF son comunes en ingeniería para modelar fenómenos donde el comportamiento de un sistema está influenciado por condiciones en sus extremos. Ejemplos incluyen la distribución de temperatura en una aleta de enfriamiento, la deflexión de una viga bajo carga, o el perfil de velocidad en un flujo de tubería.

*   **Diferencia entre PVI y PVF:** En PVI, se avanza desde un punto inicial. En PVF, se busca una solución que satisfaga condiciones en múltiples puntos.
*   **Método de Disparo (Shooting Method):** Convierte un PVF en un PVI. Se "adivina" una condición inicial desconocida, se resuelve el PVI, y se ajusta la adivinanza iterativamente hasta que la solución satisface la condición en la otra frontera.
*   **Método de Diferencias Finitas:** Discretiza el dominio y reemplaza las derivadas por aproximaciones de diferencias finitas, transformando la EDO en un sistema de ecuaciones algebraicas (lineales o no lineales) que se puede resolver.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_metodo_disparo.py`

*   **Descripción:** Implementación del Método de Disparo para resolver un PVF lineal simple. Se muestra cómo se itera sobre una condición inicial desconocida hasta satisfacer la condición de frontera final.
*   **Conceptos Clave:** Conversión PVF a PVI, adivinanza inicial, iteración, `scipy.integrate.solve_ivp` (o RK4), búsqueda de raíces para ajustar la adivinanza.

### `ejercicio_2_metodo_diferencias_finitas.py`

*   **Descripción:** Implementación del Método de Diferencias Finitas para resolver el mismo PVF lineal simple. Se explica cómo discretizar la EDO y formar un sistema de ecuaciones lineales que se resuelve con `numpy.linalg.solve`.
*   **Conceptos Clave:** Discretización, aproximación de derivadas por diferencias finitas, sistema de ecuaciones lineales, matriz de coeficientes.

### `ejercicio_3_aplicacion_aleta_calor.py`

*   **Descripción:** Aplicación del Método de Diferencias Finitas para modelar la distribución de temperatura en una aleta de enfriamiento. Se muestra cómo las condiciones de frontera afectan el perfil de temperatura a lo largo de la aleta.
*   **Conceptos Clave:** Transferencia de calor, aletas, ecuación de conducción de calor, condiciones de frontera (temperatura fija, convección, adiabática).

### `ejercicio_4_aplicacion_deflexion_viga.py`

*   **Descripción:** Aplicación del Método de Diferencias Finitas para calcular la deflexión de una viga simplemente apoyada bajo una carga distribuida. Se modela la ecuación de la elástica de la viga como un PVF.
*   **Conceptos Clave:** Mecánica de materiales, deflexión de vigas, ecuación de la elástica, condiciones de apoyo (simplemente apoyada, empotrada, libre).
