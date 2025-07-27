# -*- coding: utf-8 -*-
"""
Capítulo 2: Raíces de Ecuaciones
Ejercicio 3: Método de la Secante

El Método de la Secante es una excelente alternativa al Método de Newton-Raphson
cuando no podemos (o no queremos) calcular la derivada analítica de la función.

Recuerda que Newton-Raphson usa la tangente (la derivada) para encontrar la
siguiente aproximación a la raíz. El Método de la Secante hace algo similar,
pero en lugar de una tangente (que requiere la derivada), usa una "secante",
es decir, una línea recta que conecta dos puntos de la función.

Imagina que estás en la montaña (la función) y quieres llegar al nivel del mar.
No tienes un mapa de pendientes (derivada), pero tienes dos puntos donde estás
y puedes trazar una línea recta entre ellos. Donde esa línea cruza el nivel del
mar, esa es tu siguiente estimación para la raíz.

Este método requiere dos estimaciones iniciales, al igual que Bisección, pero
no necesita que los signos de la función sean opuestos en esos puntos.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 3: Método de la Secante ---")

# --- Parte 1: Definición de la Función ---
# Usaremos la misma función de los ejercicios anteriores para comparar resultados.

def funcion_secante(x):
    """
    Define la función f(x) = x^3 - 2x - 5.
    """
    return x**3 - 2*x - 5

# --- Parte 2: Visualización de la Función y una Secante (Opcional pero Recomendado) ---
# Graficar nos ayuda a entender cómo la línea secante nos guía hacia la raíz.

print("\n--- Parte 2: Visualización de la Función y una Secante ---")

x_valores = np.linspace(-3, 3, 400)
y_valores = funcion_secante(x_valores)

plt.figure(figsize=(10, 7))
plt.plot(x_valores, y_valores, label='f(x) = x^3 - 2x - 5', color='blue')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--', label='Eje X (f(x)=0)')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--', label='Eje Y')

# Vamos a dibujar una secante entre dos puntos iniciales para ilustrar el método.
x_0_secante = 1.0
x_1_secante = 3.0

y_0_secante = funcion_secante(x_0_secante)
y_1_secante = funcion_secante(x_1_secante)

# Ecuación de la recta que pasa por (x0, y0) y (x1, y1):
# y - y0 = ((y1 - y0) / (x1 - x0)) * (x - x0)
# y = ((y1 - y0) / (x1 - x0)) * (x - x0) + y0

pendiente_secante = (y_1_secante - y_0_secante) / (x_1_secante - x_0_secante)
secante_y = pendiente_secante * (x_valores - x_0_secante) + y_0_secante

plt.plot(x_valores, secante_y, color='green', linestyle=':', label='Secante entre x=1 y x=3')
plt.scatter([x_0_secante, x_1_secante], [y_0_secante, y_1_secante], color='red', zorder=5, label='Puntos iniciales')

plt.title('Gráfico de la Función y una Línea Secante')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.ylim(-20, 20) # Ajustamos los límites del eje Y para mejor visualización
plt.show()

print("Observa cómo la línea verde (secante) apunta hacia el eje X, cerca de la raíz.")

# --- Parte 3: Implementación del Método de la Secante ---
# La fórmula de iteración de la Secante es:
# x_nueva = x_1 - f(x_1) * (x_1 - x_0) / (f(x_1) - f(x_0))
# Donde x_0 y x_1 son las dos aproximaciones anteriores.

def metodo_secante(func, x0, x1, tolerancia, max_iteraciones):
    """
    Implementa el Método de la Secante para encontrar la raíz de una función.

    Parámetros:
        func (function): La función f(x).
        x0 (float): La primera estimación inicial de la raíz.
        x1 (float): La segunda estimación inicial de la raíz.
        tolerancia (float): Criterio de parada: cuando el cambio en x sea menor
                            que este valor, o f(x) sea muy cercano a cero.
        max_iteraciones (int): Número máximo de iteraciones.

    Retorna:
        float: La raíz aproximada de la función.
        None: Si no se encuentra una raíz o si f(x1) - f(x0) es cero (división por cero).
    """

    print("\n--- Parte 3: Ejecución del Método de la Secante ---")
    print(f"Estimaciones iniciales: x0={x0}, x1={x1}")
    print(f"Tolerancia deseada: {tolerancia}")

    x_anterior_2 = x0 # x_{i-1}
    x_anterior_1 = x1 # x_i

    for i in range(max_iteraciones):
        f_x_anterior_2 = func(x_anterior_2)
        f_x_anterior_1 = func(x_anterior_1)

        # Verificamos si el denominador es cero, lo que causaría una división por cero.
        if abs(f_x_anterior_1 - f_x_anterior_2) < 1e-9: # Muy cercano a cero
            print("\nError: Denominador muy cercano a cero (f(x1) - f(x0)). El método no puede continuar.")
            return None

        x_nueva = x_anterior_1 - f_x_anterior_1 * (x_anterior_1 - x_anterior_2) / (f_x_anterior_1 - f_x_anterior_2)

        print(f"Iteración {i+1}: x_i-1={x_anterior_2:.6f}, x_i={x_anterior_1:.6f}, x_nueva={x_nueva:.6f}, f(x_nueva)={func(x_nueva):.6e}")

        # Criterio de parada: si el cambio en x es muy pequeño
        if abs(x_nueva - x_anterior_1) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones (cambio en x muy pequeño).")
            return x_nueva

        # Criterio de parada alternativo: si f(x) es muy cercano a cero
        if abs(func(x_nueva)) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones (f(x) muy cercano a cero).")
            return x_nueva

        # Actualizamos los valores para la siguiente iteración
        x_anterior_2 = x_anterior_1
        x_anterior_1 = x_nueva

    print("\nAdvertencia: Se alcanzó el número máximo de iteraciones sin cumplir la tolerancia.")
    return x_nueva # Devolvemos la mejor aproximación encontrada

# --- Parte 4: Aplicación del Método ---

# Definimos dos estimaciones iniciales (observado del gráfico, cerca de 2)
x_inicial_0 = 1.0
x_inicial_1 = 3.0

# Definimos la tolerancia y el número máximo de iteraciones
tol = 0.0001
max_iter = 50

# Llamamos a nuestra función del método de la Secante
raiz_encontrada = metodo_secante(funcion_secante, x_inicial_0, x_inicial_1, tol, max_iter)

if raiz_encontrada is not None:
    print(f"\nLa raíz aproximada de la función es: {raiz_encontrada:.6f}")
    print(f"Verificación: f({raiz_encontrada:.6f}) = {funcion_secante(raiz_encontrada):.6e}")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El Método de la Secante es muy útil en situaciones donde la derivada de la")
print("función es muy complicada de obtener analíticamente o cuando la función es")
print("el resultado de un proceso experimental o una simulación compleja, y no")
print("tenemos una expresión matemática explícita para su derivada.")
print("Por ejemplo, al encontrar el punto de operación de una bomba o turbina a")
print("partir de curvas de rendimiento dadas en tablas o gráficos, donde la relación")
print("entre caudal y altura es una función que no tiene una derivada fácil de calcular.")

print("\n¡Has completado el tercer ejercicio del Capítulo 2!")
print("Ahora conoces el Método de la Secante, una herramienta flexible cuando la")
print("derivada no está disponible.")
