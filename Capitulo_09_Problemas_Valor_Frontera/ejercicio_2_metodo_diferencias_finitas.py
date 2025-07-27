# -*- coding: utf-8 -*-
"""
Capítulo 9: Problemas de Valor en la Frontera (PVF)
Ejercicio 2: Método de Diferencias Finitas

El Método de Diferencias Finitas es otra técnica poderosa para resolver
Problemas de Valor en la Frontera (PVF). A diferencia del Método de Disparo,
que convierte el PVF en un PVI y lo resuelve iterativamente, el Método de
Diferencias Finitas transforma directamente la EDO en un sistema de ecuaciones
algebraicas (generalmente lineales) que se puede resolver de una sola vez.

La idea principal es discretizar el dominio (dividirlo en pequeños segmentos)
y reemplazar las derivadas de la EDO por aproximaciones de diferencias finitas.
Esto convierte la EDO continua en un conjunto de ecuaciones algebraicas para
los valores de la función en los puntos discretos (nodos).

Imagina que tienes una viga y quieres saber cómo se deforma a lo largo de su
longitud. En lugar de resolver una ecuación diferencial compleja, puedes
dividir la viga en pequeños segmentos y escribir una ecuación simple para la
deformación en cada punto, relacionándola con los puntos vecinos. Al final,
tendrás un sistema de ecuaciones que puedes resolver para encontrar la
deformación en todos los puntos.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 2: Método de Diferencias Finitas ---")

# --- Parte 1: Definición del PVF de Ejemplo ---
# Resolveremos el mismo PVF lineal de segundo orden:
# y'' = -y
# Con condiciones de frontera: y(0) = 0, y(pi/2) = 1
# La solución analítica es: y(x) = sin(x)

print("\n--- Parte 1: PVF de Ejemplo ---")

# Condiciones de frontera
x_inicio = 0.0
y_inicio = 0.0 # y(0) = 0
x_fin = np.pi / 2
y_fin = 1.0 # y(pi/2) = 1

print(f"PVF: y'' = -y")
print(f"Condiciones de frontera: y({x_inicio}) = {y_inicio}, y({x_fin:.2f}) = {y_fin}")

# --- Parte 2: Implementación del Método de Diferencias Finitas ---
# Aproximaciones de diferencias finitas para derivadas:
# y'(x)  ≈ (y(x+h) - y(x-h)) / (2h)   (Diferencia central de primer orden)
# y''(x) ≈ (y(x+h) - 2y(x) + y(x-h)) / h^2 (Diferencia central de segundo orden)

# Sustituimos y'' en la EDO: (y(x+h) - 2y(x) + y(x-h)) / h^2 = -y(x)
# Reorganizando para y(x):
# y(x-h) - 2y(x) + y(x+h) = -h^2 * y(x)
# y(x-h) + (h^2 - 2)y(x) + y(x+h) = 0

def metodo_diferencias_finitas(n_nodos, x_inicio, x_fin, y_inicio, y_fin):
    """
    Resuelve el PVF y'' = -y con el Método de Diferencias Finitas.

    Parámetros:
        n_nodos (int): Número total de nodos (incluyendo los de frontera).
        x_inicio (float): Valor de x en la frontera inicial.
        x_fin (float): Valor de x en la frontera final.
        y_inicio (float): Valor de y en la frontera inicial.
        y_fin (float): Valor de y en la frontera final.

    Retorna:
        tuple: (x_valores, y_valores) arrays con la solución aproximada.
    """

    # Calculamos el tamaño del paso (h)
    h = (x_fin - x_inicio) / (n_nodos - 1)

    # Creamos los valores de x en los nodos
    x_valores = np.linspace(x_inicio, x_fin, n_nodos)

    # El número de incógnitas es n_nodos - 2 (excluyendo los nodos de frontera)
    num_incognitas = n_nodos - 2

    # Creamos la matriz de coeficientes A y el vector b para el sistema lineal Ay = b
    # La matriz A será tridiagonal.
    A = np.zeros((num_incognitas, num_incognitas))
b_vector = np.zeros(num_incognitas)

    print(f"\n--- Parte 2: Construyendo el Sistema Lineal (n_nodos={n_nodos}, h={h:.4f}) ---")

    # Llenamos la matriz A y el vector b
    for i in range(num_incognitas):
        # Elemento diagonal principal
        A[i, i] = (h**2 - 2)

        # Elementos fuera de la diagonal
        if i > 0: # Elemento a la izquierda
            A[i, i-1] = 1
        if i < num_incognitas - 1: # Elemento a la derecha
            A[i, i+1] = 1
        
        # Llenamos el vector b
        # Los términos de frontera se mueven al lado derecho de la ecuación
        if i == 0: # Primera ecuación interna (afectada por y_inicio)
            b_vector[i] = -y_inicio
        if i == num_incognitas - 1: # Última ecuación interna (afectada por y_fin)
            b_vector[i] = -y_fin

    print("Matriz de Coeficientes A:")
    print(A)
    print("\nVector b:")
    print(b_vector)

    # Resolvemos el sistema lineal Ay = b para encontrar los valores de y en los nodos internos
    y_internos = np.linalg.solve(A, b_vector)

    # Construimos la solución completa incluyendo los valores de frontera
    y_valores = np.concatenate(([y_inicio], y_internos, [y_fin]))

    return x_valores, y_valores

# --- Parte 3: Aplicación y Visualización ---

print("\n--- Parte 3: Aplicación y Visualización ---")

num_nodos = 10 # Número de nodos. Experimenta con más nodos para mayor precisión.

x_sol_num, y_sol_num = metodo_diferencias_finitas(num_nodos, x_inicio, x_fin, y_inicio, y_fin)

# Solución analítica para comparar: y(x) = sin(x)
x_analitica = np.linspace(x_inicio, x_fin, 100) # Muchos puntos para una curva suave
y_analitica = np.sin(x_analitica)

plt.figure(figsize=(10, 6))
plt.plot(x_analitica, y_analitica, color='blue', linestyle='-', label='Solución Analítica: sin(x)')
plt.plot(x_sol_num, y_sol_num, color='red', linestyle='--', marker='o', markersize=6, label=f'Solución Numérica (Diferencias Finitas, N={num_nodos})')
plt.scatter([x_inicio, x_fin], [y_inicio, y_fin], color='green', s=100, zorder=5, label='Condiciones de Frontera')

plt.title('Solución de PVF con el Método de Diferencias Finitas')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

print("\n¡Has resuelto un Problema de Valor en la Frontera usando el Método de Diferencias Finitas!")
print("Este método es muy potente para transformar EDOs en sistemas algebraicos resolubles.")
