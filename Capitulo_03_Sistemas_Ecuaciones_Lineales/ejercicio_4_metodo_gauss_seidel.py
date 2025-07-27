# -*- coding: utf-8 -*-
"""
Capítulo 3: Sistemas de Ecuaciones Lineales
Ejercicio 4: Método de Gauss-Seidel

El Método de Gauss-Seidel es una mejora del Método de Jacobi para resolver
sistemas de ecuaciones lineales Ax = b de forma iterativa. Al igual que Jacobi,
es muy útil para sistemas grandes y dispersos.

La principal diferencia y ventaja de Gauss-Seidel es que, al calcular una
nueva incógnita (x_i), utiliza los valores de las incógnitas que ya han sido
actualizadas en la *misma iteración*.

Volviendo a la analogía de los ingenieros: en Jacobi, todos calculaban sus
valores usando las estimaciones de la iteración anterior y luego actualizaban
simultáneamente. En Gauss-Seidel, el primer ingeniero calcula su valor, luego
el segundo ingeniero usa el valor *recién calculado* por el primero (y los
demás de la iteración anterior), el tercero usa los valores *recién calculados*
por el primero y el segundo, y así sucesivamente. Esto hace que la información
se propague más rápidamente y, por lo general, el método converge más rápido.
"""

import numpy as np

print("--- Ejercicio 4: Método de Gauss-Seidel ---")

# --- Parte 1: Definición del Sistema de Ecuaciones ---
# Usaremos el mismo sistema del ejercicio de Jacobi, que es diagonalmente dominante,
# lo que ayuda a garantizar la convergencia.
# 10x1 - 2x2 - x3 = 7
# -2x1 + 10x2 - x3 = 13
# -x1 - 2x2 + 10x3 = 20

print("\n--- Parte 1: Definición del Sistema ---")

A = np.array([
    [10, -2, -1],
    [-2, 10, -1],
    [-1, -2, 10]
], dtype=float)

b = np.array([7, 13, 20], dtype=float)

print("Matriz de coeficientes A:")
print(A)
print("\nVector de términos independientes b:")
print(b)

# --- Parte 2: Implementación del Método de Gauss-Seidel ---
# La fórmula de iteración es similar a Jacobi, pero con la actualización en el mismo bucle:
# x_i = (b_i - sum(a_ij * x_j para j < i) - sum(a_ij * x_j para j > i)) / a_ii
# Donde los x_j para j < i ya son los valores actualizados de la iteración actual.

def metodo_gauss_seidel(A, b, x0, tolerancia, max_iteraciones):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el Método de Gauss-Seidel.

    Parámetros:
        A (numpy.array): Matriz de coeficientes (cuadrada).
        b (numpy.array): Vector de términos independientes.
        x0 (numpy.array): Vector de suposiciones iniciales para las incógnitas.
        tolerancia (float): Criterio de parada: cuando el cambio en la solución
                            entre iteraciones sea menor que este valor.
        max_iteraciones (int): Número máximo de iteraciones para evitar bucles infinitos.

    Retorna:
        numpy.array: El vector solución aproximada x.
        None: Si no converge dentro del número máximo de iteraciones.
    """

    n = len(b) # Número de ecuaciones (y de incógnitas)
    x_actual = x0.copy() # Copia de la suposición inicial, que se irá actualizando
    x_anterior = np.zeros(n) # Para guardar la solución de la iteración anterior para el cálculo del error

    print("\n--- Parte 2: Ejecución del Método de Gauss-Seidel ---")
    print(f"Suposición inicial x0: {x0}")
    print(f"Tolerancia deseada: {tolerancia}")

    # Verificación de diagonal dominante (simplificada, solo para advertir)
    for i in range(n):
        suma_no_diagonal = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
        if np.abs(A[i, i]) <= suma_no_diagonal:
            print(f"Advertencia: La matriz no es estrictamente diagonalmente dominante en la fila {i+1}. La convergencia no está garantizada.")

    for iteracion in range(1, max_iteraciones + 1):
        x_anterior[:] = x_actual # Guardamos la solución actual antes de actualizarla

        for i in range(n): # Para cada incógnita x_i
            suma_terminos = 0.0
            for j in range(n): # Sumamos los términos a_ij * x_j
                if i != j:
                    # Aquí está la clave: si j < i, usamos x_actual[j] (ya actualizado en esta iteración)
                    # si j > i, usamos x_anterior[j] (de la iteración previa)
                    suma_terminos += A[i, j] * x_actual[j] # Gauss-Seidel usa los valores más recientes
            
            # Despejamos x_i de la ecuación i-ésima
            if A[i, i] == 0: # Evitar división por cero
                print(f"Error: Elemento diagonal A[{i},{i}] es cero. No se puede aplicar Gauss-Seidel.")
                return None
            x_actual[i] = (b[i] - suma_terminos) / A[i, i]

        # Calculamos el error (cambio máximo entre la solución actual y la anterior)
        error = np.max(np.abs(x_actual - x_anterior))

        print(f"Iteración {iteracion}: x = {x_actual}, Error = {error:.6e}")

        # Criterio de parada: si el error es menor que la tolerancia
        if error < tolerancia:
            print(f"\nConvergencia alcanzada en {iteracion} iteraciones.")
            return x_actual

    print("\nAdvertencia: Se alcanzó el número máximo de iteraciones sin cumplir la tolerancia.")
    return x_actual # Devolvemos la mejor aproximación encontrada

# --- Parte 3: Aplicación del Método ---

print("\n--- Parte 3: Aplicación del Método ---")

# Suposición inicial (a menudo se usa un vector de ceros)
x_inicial = np.array([0.0, 0.0, 0.0], dtype=float)

# Definimos la tolerancia y el número máximo de iteraciones
tol = 0.0001
max_iter = 100

solucion_gauss_seidel = metodo_gauss_seidel(A.copy(), b.copy(), x_inicial, tol, max_iter)

if solucion_gauss_seidel is not None:
    print("\nVector solución aproximada x (Gauss-Seidel):")
    print(solucion_gauss_seidel)

    # Verificación: Sustituimos la solución en las ecuaciones originales
    print("\nVerificación (A @ x):")
    print(A @ solucion_gauss_seidel)
    print("Vector b original:")
    print(b)
    print("¿A @ x es aproximadamente igual a b?", np.allclose(A @ solucion_gauss_seidel, b, atol=tol))
    # Usamos atol=tol para comparar con la tolerancia del método iterativo.

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El Método de Gauss-Seidel es ampliamente utilizado en la solución de")
print("problemas de transferencia de calor en estado estacionario, donde se")
print("discretiza un dominio y se establecen ecuaciones de balance de energía")
print("para cada nodo. Las temperaturas de los nodos son las incógnitas.")
print("También es fundamental en el análisis de redes de fluidos y circuitos")
print("eléctricos complejos, especialmente cuando se modelan con mallas o nodos.")
print("Su eficiencia en la convergencia lo hace preferible a Jacobi en muchas")
print("aplicaciones prácticas de ingeniería.")

print("\n¡Has completado el cuarto y último ejercicio del Capítulo 3!")
print("Ahora entiendes el Método de Gauss-Seidel, un método iterativo más rápido")
print("que Jacobi para resolver sistemas de ecuaciones lineales.")
print("¡Felicidades por completar el Capítulo 3: Sistemas de Ecuaciones Lineales!")
