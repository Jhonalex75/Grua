# -*- coding: utf-8 -*-
"""
Capítulo 3: Sistemas de Ecuaciones Lineales
Ejercicio 3: Método de Jacobi

Además de los métodos directos como la Eliminación Gaussiana y la Descomposición LU,
que nos dan la solución en un número fijo de pasos, existen los métodos iterativos.
Estos métodos comienzan con una suposición inicial para la solución y la van
refinando paso a paso hasta que se acercan lo suficiente a la respuesta correcta.

El Método de Jacobi es uno de los métodos iterativos más sencillos para resolver
sistemas de ecuaciones lineales Ax = b. Es particularmente útil para sistemas
muy grandes, donde los métodos directos pueden ser computacionalmente costosos,
o para matrices con muchos ceros (matrices dispersas).

Imagina que tienes un grupo de ingenieros trabajando en un proyecto, y cada uno
necesita un valor (una incógnita) que depende de los valores de los demás.
En el método de Jacobi, cada ingeniero calcula su valor usando las últimas
estimaciones disponibles de los demás, sin esperar a que los demás terminen
sus cálculos actuales. Luego, todos actualizan sus valores simultáneamente.
Este proceso se repite hasta que los valores ya no cambian significativamente.
"""

import numpy as np

print("--- Ejercicio 3: Método de Jacobi ---")

# --- Parte 1: Definición del Sistema de Ecuaciones ---
# Para que el Método de Jacobi converja, la matriz A debe ser "diagonalmente dominante".
# Esto significa que el valor absoluto del elemento en la diagonal principal de cada fila
# debe ser mayor que la suma de los valores absolutos de los otros elementos en esa fila.

# Ejemplo de sistema (diagonalmente dominante):
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

# --- Parte 2: Implementación del Método de Jacobi ---
# La idea es despejar cada incógnita de su respectiva ecuación.
# Para la ecuación i-ésima: a_ii * x_i = b_i - sum(a_ij * x_j para j != i)
# x_i = (b_i - sum(a_ij * x_j para j != i)) / a_ii

def metodo_jacobi(A, b, x0, tolerancia, max_iteraciones):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el Método de Jacobi.

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
    x_actual = x0.copy() # Copia de la suposición inicial
    x_anterior = np.zeros(n) # Para guardar la solución de la iteración anterior

    print("\n--- Parte 2: Ejecución del Método de Jacobi ---")
    print(f"Suposición inicial x0: {x0}")
    print(f"Tolerancia deseada: {tolerancia}")

    # Verificación de diagonal dominante (simplificada, solo para advertir)
    for i in range(n):
        suma_no_diagonal = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
        if np.abs(A[i, i]) <= suma_no_diagonal:
            print(f"Advertencia: La matriz no es estrictamente diagonalmente dominante en la fila {i+1}. La convergencia no está garantizada.")

    for iteracion in range(1, max_iteraciones + 1):
        x_anterior = x_actual.copy() # Guardamos la solución actual como la anterior

        for i in range(n): # Para cada incógnita x_i
            suma_terminos = 0.0
            for j in range(n): # Sumamos los términos a_ij * x_j donde j != i
                if i != j:
                    suma_terminos += A[i, j] * x_anterior[j] # Usamos los valores de la iteración ANTERIOR
            
            # Despejamos x_i de la ecuación i-ésima
            # x_i = (b_i - (suma de a_ij * x_j para j != i)) / a_ii
            if A[i, i] == 0: # Evitar división por cero
                print(f"Error: Elemento diagonal A[{i},{i}] es cero. No se puede aplicar Jacobi.")
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

solucion_jacobi = metodo_jacobi(A.copy(), b.copy(), x_inicial, tol, max_iter)

if solucion_jacobi is not None:
    print("\nVector solución aproximada x (Jacobi):")
    print(solucion_jacobi)

    # Verificación: Sustituimos la solución en las ecuaciones originales
    print("\nVerificación (A @ x):")
    print(A @ solucion_jacobi)
    print("Vector b original:")
    print(b)
    print("¿A @ x es aproximadamente igual a b?", np.allclose(A @ solucion_jacobi, b, atol=tol))
    # Usamos atol=tol para comparar con la tolerancia del método iterativo.

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El Método de Jacobi es muy relevante en el análisis de grandes redes,")
print("como redes de tuberías para distribución de fluidos o redes eléctricas.")
print("En el análisis de flujo en redes de tuberías, cada ecuación representa")
print("el balance de masa o energía en un nodo, y las incógnitas pueden ser")
print("las presiones en los nodos o los caudales en las tuberías. Cuando la red")
print("es muy grande, los métodos directos pueden ser ineficientes. Jacobi (y")
print("otros métodos iterativos) son preferidos porque solo necesitan almacenar")
print("los elementos no nulos de la matriz y son más eficientes para matrices dispersas.")
print("También se usa en la solución de ecuaciones diferenciales parciales discretizadas,")
print("como las que surgen en problemas de transferencia de calor o mecánica de fluidos.")

print("\n¡Has completado el tercer ejercicio del Capítulo 3!")
print("Ahora entiendes el Método de Jacobi, un método iterativo para resolver")
print("sistemas de ecuaciones lineales, especialmente útil para grandes sistemas.")
