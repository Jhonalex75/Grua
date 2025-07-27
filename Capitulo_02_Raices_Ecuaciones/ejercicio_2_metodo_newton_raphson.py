# -*- coding: utf-8 -*-
"""
Capítulo 2: Raíces de Ecuaciones
Ejercicio 2: Método de Newton-Raphson

El Método de Newton-Raphson es otra técnica muy potente para encontrar las
raíces de una ecuación f(x) = 0. A diferencia del Método de Bisección, que
"corta" el intervalo a la mitad, Newton-Raphson utiliza la información de
la pendiente (derivada) de la función para "apuntar" directamente hacia la raíz.

Imagina que estás en una montaña (la función f(x)) y quieres llegar al nivel
del mar (donde f(x)=0). Si sabes la pendiente de la montaña donde estás,
puedes estimar dónde está el nivel del mar si sigues esa pendiente. Newton-Raphson
hace exactamente eso: usa la pendiente para hacer una mejor estimación en cada paso.

Este método es generalmente más rápido (converge más rápido) que el de Bisección,
pero tiene un requisito adicional: necesitamos conocer la derivada de la función.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 2: Método de Newton-Raphson ---")

# --- Parte 1: Definición de la Función y su Derivada ---
# Para Newton-Raphson, necesitamos tanto la función f(x) como su derivada f'(x).
# Si no podemos obtener la derivada analíticamente, a veces se usa una aproximación
# numérica de la derivada (diferenciación numérica), pero eso lo veremos más adelante.

def funcion_newton(x):
    """
    Define la función f(x) = x^3 - 2x - 5.
    Es la misma función del ejercicio de Bisección para comparar.
    """
    return x**3 - 2*x - 5

def derivada_funcion_newton(x):
    """
    Define la derivada de la función f(x) = x^3 - 2x - 5.
    f'(x) = 3x^2 - 2
    """
    return 3*x**2 - 2

# --- Parte 2: Visualización de la Función y la Tangente (Opcional pero Recomendado) ---
# Graficar nos ayuda a entender cómo la tangente nos guía hacia la raíz.

print("\n--- Parte 2: Visualización de la Función y la Tangente ---")

x_valores = np.linspace(-3, 3, 400)
y_valores = funcion_newton(x_valores)

plt.figure(figsize=(10, 7))
plt.plot(x_valores, y_valores, label='f(x) = x^3 - 2x - 5', color='blue')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--', label='Eje X (f(x)=0)')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--', label='Eje Y')

# Vamos a dibujar una tangente en un punto inicial para ilustrar el método.
x_inicial_tangente = 3.0
y_inicial_tangente = funcion_newton(x_inicial_tangente)
pendiente_tangente = derivada_funcion_newton(x_inicial_tangente)

# Ecuación de la recta tangente: y - y1 = m(x - x1) => y = m(x - x1) + y1
tangente_y = pendiente_tangente * (x_valores - x_inicial_tangente) + y_inicial_tangente

# Solo mostramos la parte relevante de la tangente para que no ocupe toda la gráfica
plt.plot(x_valores, tangente_y, color='green', linestyle=':', label='Tangente en x=3')
plt.scatter(x_inicial_tangente, y_inicial_tangente, color='red', zorder=5, label='Punto inicial')

plt.title('Gráfico de la Función y una Tangente')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.ylim(-20, 20) # Ajustamos los límites del eje Y para mejor visualización
plt.show()

print("Observa cómo la línea verde (tangente) apunta hacia el eje X, cerca de la raíz.")

# --- Parte 3: Implementación del Método de Newton-Raphson ---
# La fórmula de iteración de Newton-Raphson es:
# x_nueva = x_anterior - f(x_anterior) / f'(x_anterior)

def metodo_newton_raphson(func, dfunc, x0, tolerancia, max_iteraciones):
    """
    Implementa el Método de Newton-Raphson para encontrar la raíz de una función.

    Parámetros:
        func (function): La función f(x).
        dfunc (function): La derivada de la función f'(x).
        x0 (float): La estimación inicial de la raíz.
        tolerancia (float): Criterio de parada: cuando el cambio en x sea menor
                            que este valor, o f(x) sea muy cercano a cero.
        max_iteraciones (int): Número máximo de iteraciones.

    Retorna:
        float: La raíz aproximada de la función.
        None: Si no se encuentra una raíz o si la derivada es cero (división por cero).
    """

    print("\n--- Parte 3: Ejecución del Método de Newton-Raphson ---")
    print(f"Estimación inicial (x0): {x0}")
    print(f"Tolerancia deseada: {tolerancia}")

    x_anterior = x0

    for i in range(max_iteraciones):
        f_x = func(x_anterior)
        df_x = dfunc(x_anterior)

        # Verificamos si la derivada es cero, lo que causaría una división por cero.
        if abs(df_x) < 1e-9: # Usamos un número muy pequeño en lugar de 0 exacto por seguridad con flotantes.
            print("\nError: Derivada muy cercana a cero. El método no puede continuar.")
            return None

        x_nueva = x_anterior - f_x / df_x

        print(f"Iteración {i+1}: x_anterior={x_anterior:.6f}, f(x_anterior)={f_x:.6e}, f'(x_anterior)={df_x:.6f}, x_nueva={x_nueva:.6f}")

        # Criterio de parada: si el cambio en x es muy pequeño
        if abs(x_nueva - x_anterior) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones (cambio en x muy pequeño).")
            return x_nueva

        # Criterio de parada alternativo: si f(x) es muy cercano a cero
        if abs(f_x) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones (f(x) muy cercano a cero).")
            return x_nueva

        x_anterior = x_nueva # Actualizamos x para la siguiente iteración

    print("\nAdvertencia: Se alcanzó el número máximo de iteraciones sin cumplir la tolerancia.")
    return x_nueva # Devolvemos la mejor aproximación encontrada

# --- Parte 4: Aplicación del Método ---

# Definimos una estimación inicial (observado del gráfico, cerca de 2)
x_inicial = 2.0

# Definimos la tolerancia y el número máximo de iteraciones
tol = 0.0001
max_iter = 50 # Newton-Raphson suele converger en menos iteraciones que Bisección

# Llamamos a nuestra función del método de Newton-Raphson
raiz_encontrada = metodo_newton_raphson(funcion_newton, derivada_funcion_newton, x_inicial, tol, max_iter)

if raiz_encontrada is not None:
    print(f"\nLa raíz aproximada de la función es: {raiz_encontrada:.6f}")
    print(f"Verificación: f({raiz_encontrada:.6f}) = {funcion_newton(raiz_encontrada):.6e}")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("Newton-Raphson es muy útil en problemas de diseño donde se busca optimizar")
print("una variable para que una condición se cumpla. Por ejemplo, encontrar el")
print("ángulo de lanzamiento de un proyectil para que caiga a una distancia específica,")
print("o determinar la temperatura de equilibrio en un intercambiador de calor")
print("cuando las ecuaciones de balance de energía son no lineales.")
print("También se usa en el análisis de circuitos eléctricos no lineales o en el")
print("cálculo de la distribución de esfuerzos en materiales con comportamiento no lineal.")

print("\n¡Has completado el segundo ejercicio del Capítulo 2!")
print("Ahora conoces el potente Método de Newton-Raphson y sus ventajas (rapidez)")
print("y desventajas (necesidad de la derivada, posible divergencia si x0 es malo).")
