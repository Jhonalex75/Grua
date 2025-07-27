# -*- coding: utf-8 -*-
"""
Capítulo 4: Ajuste de Curvas e Interpolación
Ejercicio 1: Regresión Lineal (Mínimos Cuadrados)

En ingeniería, a menudo recolectamos datos experimentales o de simulaciones.
Por ejemplo, cómo varía la deformación de un material con la carga aplicada,
o cómo cambia la temperatura de un fluido con el tiempo de calentamiento.
Muchas veces, queremos encontrar una relación matemática simple (una ecuación)
que describa la tendencia de estos datos.

La Regresión Lineal es una técnica estadística que nos permite encontrar la
línea recta que "mejor se ajusta" a un conjunto de puntos de datos. El objetivo
es minimizar la suma de los cuadrados de las distancias verticales entre cada
punto de dato y la línea recta. Por eso se llama "Mínimos Cuadrados".

Imagina que tienes un gráfico con muchos puntos dispersos y quieres dibujar
una línea recta que pase lo más cerca posible de todos ellos. La regresión
lineal nos da la ecuación de esa línea.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 1: Regresión Lineal (Mínimos Cuadrados) ---")

# --- Parte 1: Datos de Ejemplo ---
# Vamos a usar un conjunto de datos simple para ilustrar la regresión lineal.
# Por ejemplo, la relación entre la carga aplicada a un resorte y su deformación.

print("\n--- Parte 1: Datos de Ejemplo ---")

carga = np.array([10, 20, 30, 40, 50, 60, 70, 80]) # Unidades: Newtons (N)
deformacion = np.array([0.5, 1.1, 1.4, 2.0, 2.6, 3.0, 3.5, 4.1]) # Unidades: cm

print("Carga (x):", carga)
print("Deformación (y):", deformacion)

# Visualizamos los datos para ver la tendencia.
plt.figure(figsize=(8, 6))
plt.scatter(carga, deformacion, color='blue', label='Datos Experimentales')
plt.title('Carga vs. Deformación de un Resorte')
plt.xlabel('Carga (N)')
plt.ylabel('Deformación (cm)')
plt.grid(True)
plt.legend()
plt.show()

print("Los puntos parecen seguir una tendencia lineal.")

# --- Parte 2: Implementación de la Regresión Lineal ---
# La ecuación de una línea recta es y = mx + b, donde:
# m = pendiente
# b = intercepto (punto donde la línea cruza el eje Y)

# Las fórmulas para m y b usando el método de mínimos cuadrados son:
# m = (n * sum(xy) - sum(x) * sum(y)) / (n * sum(x^2) - (sum(x))^2)
# b = (sum(y) - m * sum(x)) / n
# Donde n es el número de puntos de datos.

def regresion_lineal(x, y):
    """
    Calcula la pendiente (m) y el intercepto (b) de la línea de regresión lineal
    usando el método de mínimos cuadrados.

    Parámetros:
        x (numpy.array): Array de los valores de la variable independiente.
        y (numpy.array): Array de los valores de la variable dependiente.

    Retorna:
        tuple: (m, b) la pendiente y el intercepto de la línea de regresión.
    """

    n = len(x) # Número de puntos de datos

    # Calculamos las sumas necesarias
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y) # Suma de (x_i * y_i)
    sum_x_squared = np.sum(x**2) # Suma de (x_i^2)

    # Calculamos la pendiente (m)
    numerador_m = n * sum_xy - sum_x * sum_y
    denominador_m = n * sum_x_squared - (sum_x)**2

    if denominador_m == 0:
        print("Error: El denominador para la pendiente es cero. No se puede calcular la regresión lineal.")
        return None, None

    m = numerador_m / denominador_m

    # Calculamos el intercepto (b)
    b = (sum_y - m * sum_x) / n

    return m, b

# --- Parte 3: Aplicación y Visualización de la Línea de Regresión ---

print("\n--- Parte 3: Aplicación y Visualización ---")

pendiente, intercepto = regresion_lineal(carga, deformacion)

if pendiente is not None and intercepto is not None:
    print(f"Pendiente (m): {pendiente:.4f}")
    print(f"Intercepto (b): {intercepto:.4f}")
    print(f"Ecuación de la línea de regresión: y = {pendiente:.4f}x + {intercepto:.4f}")

    # Generamos puntos para la línea de regresión usando la ecuación encontrada.
    # Usamos los valores mínimos y máximos de carga para dibujar la línea.
    x_linea = np.array([np.min(carga), np.max(carga)])
    y_linea = pendiente * x_linea + intercepto

    # Volvemos a graficar los datos y añadimos la línea de regresión.
    plt.figure(figsize=(8, 6))
    plt.scatter(carga, deformacion, color='blue', label='Datos Experimentales')
    plt.plot(x_linea, y_linea, color='red', linestyle='-', label='Línea de Regresión')
    plt.title('Regresión Lineal: Carga vs. Deformación')
    plt.xlabel('Carga (N)')
    plt.ylabel('Deformación (cm)')
    plt.grid(True)
    plt.legend()
    plt.show()

    # --- Verificación con NumPy (opcional, para mostrar que Python ya lo hace) ---
    # NumPy tiene funciones para hacer esto de forma más directa.
    # np.polyfit(x, y, grado) devuelve los coeficientes de un polinomio.
    # Para una línea recta, el grado es 1.
    coeficientes_np = np.polyfit(carga, deformacion, 1)
    m_np = coeficientes_np[0]
    b_np = coeficientes_np[1]
    print(f"\nVerificación con NumPy: Pendiente (m) = {m_np:.4f}, Intercepto (b) = {b_np:.4f}")
    print("Los resultados son muy similares, lo que valida nuestra implementación.")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La regresión lineal es fundamental en la caracterización de materiales.")
print("Por ejemplo, para determinar el módulo de Young de un material a partir")
print("de un ensayo de tracción (relación esfuerzo-deformación en la zona elástica).")
print("También se usa para calibrar sensores, predecir el rendimiento de máquinas")
print("basado en variables de operación, o para modelar la pérdida de calor en")
print("sistemas térmicos en función de la diferencia de temperatura.")

print("\n¡Has completado el primer ejercicio del Capítulo 4!")
print("Ahora entiendes cómo la Regresión Lineal nos ayuda a encontrar relaciones")
print("entre variables a partir de datos experimentales.")
