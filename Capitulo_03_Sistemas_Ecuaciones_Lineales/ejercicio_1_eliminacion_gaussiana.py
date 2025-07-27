# -*- coding: utf-8 -*-
"""
Capítulo 3: Sistemas de Ecuaciones Lineales
Ejercicio 1: Eliminación Gaussiana

En ingeniería, es muy común encontrarse con problemas que se pueden modelar
como un sistema de ecuaciones lineales. Por ejemplo, el análisis de mallas
en circuitos eléctricos, el cálculo de fuerzas en estructuras reticuladas,
o la determinación de concentraciones en reacciones químicas en equilibrio.

Un sistema de ecuaciones lineales se ve así:

a11*x1 + a12*x2 + ... + a1n*xn = b1
a21*x1 + a22*x2 + ... + a2n*xn = b2
...
an1*x1 + an2*x2 + ... + ann*xn = bn

Donde 'a' son los coeficientes conocidos, 'x' son las incógnitas que queremos
encontrar, y 'b' son los términos independientes conocidos.

La Eliminación Gaussiana es un método directo (no iterativo) para resolver
estos sistemas. Su objetivo es transformar el sistema original en uno equivalente
que sea más fácil de resolver, específicamente una forma triangular superior.
Luego, las incógnitas se encuentran mediante "sustitución hacia atrás".

Imagina que tienes un conjunto de balanzas interconectadas y quieres saber el
peso de cada objeto. La Eliminación Gaussiana es como ir simplificando las
balanzas paso a paso hasta que puedes determinar el peso de un objeto, y luego
usar ese peso para encontrar los demás.
"""

import numpy as np # NumPy es esencial para trabajar con matrices.

print("--- Ejercicio 1: Eliminación Gaussiana ---")

# --- Parte 1: Representación del Sistema de Ecuaciones ---
# Un sistema de ecuaciones lineales se puede representar convenientemente
# usando matrices. La matriz 'A' contiene los coeficientes, y el vector 'b'
# contiene los términos independientes.

# Ejemplo de sistema:
# 2x + y - z = 8
# -3x - y + 2z = -11
# -2x + y + 2z = -3

print("\n--- Parte 1: Representación del Sistema ---")

A = np.array([
    [2,  1, -1],
    [-3, -1,  2],
    [-2,  1,  2]
], dtype=float) # Es importante que los números sean flotantes para las divisiones.

b = np.array([8, -11, -3], dtype=float)

print("Matriz de coeficientes A:")
print(A)
print("\nVector de términos independientes b:")
print(b)

# --- Parte 2: Implementación de la Eliminación Gaussiana ---
# El proceso consta de dos fases:
# 1. Fase de Eliminación hacia Adelante: Transformar la matriz A en una matriz
#    triangular superior (todos los elementos debajo de la diagonal principal son cero).
# 2. Fase de Sustitución hacia Atrás: Resolver el sistema resultante.

def eliminacion_gaussiana(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando Eliminación Gaussiana.

    Parámetros:
        A (numpy.array): Matriz de coeficientes (cuadrada).
        b (numpy.array): Vector de términos independientes.

    Retorna:
        numpy.array: El vector solución x.
        None: Si el sistema no tiene solución única (matriz singular).
    """

    n = len(b) # Número de ecuaciones (y de incógnitas)

    # Creamos una matriz aumentada [A|b] para trabajar con ella.
    # np.hstack() une horizontalmente la matriz A y el vector b.
    matriz_aumentada = np.hstack((A, b.reshape(n, 1))) # b.reshape(n, 1) lo convierte en columna

    print("\n--- Parte 2: Ejecución de Eliminación Gaussiana ---")
    print("Matriz Aumentada Inicial:")
    print(matriz_aumentada)

    # --- Fase 1: Eliminación hacia Adelante ---
    for i in range(n): # Iteramos sobre cada fila (pivote)
        # Paso 1.1: Encontrar el pivote más grande (para estabilidad numérica)
        # Esto es opcional pero recomendado para evitar divisiones por números muy pequeños.
        # Se llama "pivoteo parcial".
        max_fila = i
        for k in range(i + 1, n):
            if abs(matriz_aumentada[k, i]) > abs(matriz_aumentada[max_fila, i]):
                max_fila = k
        # Intercambiar la fila actual con la fila del pivote más grande
        matriz_aumentada[[i, max_fila]] = matriz_aumentada[[max_fila, i]]

        # Paso 1.2: Hacer cero los elementos debajo del pivote
        # Verificamos si el elemento pivote es cero. Si lo es, la matriz es singular.
        if matriz_aumentada[i, i] == 0:
            print("\nError: La matriz es singular (elemento pivote es cero). El sistema no tiene solución única.")
            return None

        for k in range(i + 1, n):
            # Calculamos el factor por el cual multiplicaremos la fila pivote
            factor = matriz_aumentada[k, i] / matriz_aumentada[i, i]
            # Restamos la fila pivote multiplicada por el factor a la fila actual
            matriz_aumentada[k, i:] = matriz_aumentada[k, i:] - factor * matriz_aumentada[i, i:]

        print(f"\nMatriz Aumentada después de la columna {i+1} (eliminación):")
        print(matriz_aumentada)

    print("\nMatriz Aumentada en Forma Triangular Superior:")
    print(matriz_aumentada)

    # --- Fase 2: Sustitución hacia Atrás ---
    x = np.zeros(n) # Creamos un vector para almacenar las soluciones (inicialmente ceros)

    # Empezamos desde la última ecuación y subimos.
    for i in range(n - 1, -1, -1): # n-1 es la última fila, -1 es el límite (exclusivo), -1 es el paso (hacia atrás)
        # La incógnita actual (x[i]) se calcula despejando de la ecuación actual.
        # El término independiente es matriz_aumentada[i, n]
        # Restamos los términos ya conocidos (x[j] para j > i)
        x[i] = (matriz_aumentada[i, n] - np.dot(matriz_aumentada[i, i+1:n], x[i+1:n])) / matriz_aumentada[i, i]

    return x

# --- Parte 3: Aplicación del Método ---

print("\n--- Parte 3: Aplicación del Método ---")

solucion = eliminacion_gaussiana(A.copy(), b.copy()) # Usamos .copy() para no modificar las matrices originales

if solucion is not None:
    print("\nVector solución x:")
    print(solucion)

    # Verificación: Sustituimos la solución en las ecuaciones originales
    print("\nVerificación (A @ x):") # @ es el operador de producto matricial en Python 3.5+
    print(A @ solucion)
    print("Vector b original:")
    print(b)
    print("¿A @ x es aproximadamente igual a b?", np.allclose(A @ solucion, b))
    # np.allclose() es mejor para comparar flotantes que ==

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La Eliminación Gaussiana es fundamental en el análisis estructural, por ejemplo,")
print("para resolver las ecuaciones de equilibrio de nudos en armaduras o marcos.")
print("Cada ecuación representa el equilibrio de fuerzas en una dirección para un nudo,")
print("y las incógnitas son las fuerzas en las barras o las reacciones en los apoyos.")
print("También se usa en el análisis de circuitos eléctricos (leyes de Kirchhoff)")
print("y en problemas de transferencia de calor donde se discretiza un dominio y se")
print("establecen ecuaciones de balance de energía para cada nodo.")

print("\n¡Has completado el primer ejercicio del Capítulo 3!")
print("Ahora entiendes cómo la Eliminación Gaussiana resuelve sistemas de ecuaciones lineales,")
print("una herramienta indispensable en muchas áreas de la ingeniería.")
