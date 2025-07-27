# -*- coding: utf-8 -*-
"""
Capítulo 3: Sistemas de Ecuaciones Lineales
Ejercicio 2: Descomposición LU

La Descomposición LU (Lower-Upper) es una técnica muy poderosa para resolver
sistemas de ecuaciones lineales Ax = b. Es una variación de la Eliminación
Gaussiana, pero en lugar de resolver el sistema directamente, descompone la
matriz de coeficientes A en el producto de dos matrices triangulares:

L (Lower): Una matriz triangular inferior (todos los elementos por encima
           de la diagonal principal son cero).
U (Upper): Una matriz triangular superior (todos los elementos por debajo
           de la diagonal principal son cero).

Es decir, A = L * U.

Una vez que tenemos A = LU, el sistema Ax = b se convierte en (LU)x = b.
Podemos resolver esto en dos pasos:
1.  Ly = b: Resolvemos para un vector intermedio 'y' usando sustitución hacia adelante.
2.  Ux = y: Resolvemos para la solución 'x' usando sustitución hacia atrás.

La gran ventaja de la Descomposición LU es que, una vez que A se descompone
en L y U, podemos resolver el sistema para diferentes vectores 'b' de forma
muy rápida, sin tener que repetir todo el proceso de eliminación cada vez.
Esto es muy útil en simulaciones donde las cargas (vector b) cambian, pero
la geometría o propiedades del sistema (matriz A) permanecen constantes.
"""

import numpy as np

print("--- Ejercicio 2: Descomposición LU ---")

# --- Parte 1: Definición del Sistema de Ecuaciones ---
# Usaremos el mismo sistema del ejercicio anterior para comparar.
# 2x + y - z = 8
# -3x - y + 2z = -11
# -2x + y + 2z = -3

print("\n--- Parte 1: Definición del Sistema ---")

A = np.array([
    [2,  1, -1],
    [-3, -1,  2],
    [-2,  1,  2]
], dtype=float)

b = np.array([8, -11, -3], dtype=float)

print("Matriz de coeficientes A:")
print(A)
print("\nVector de términos independientes b:")
print(b)

# --- Parte 2: Implementación de la Descomposición LU ---
# La descomposición LU se puede obtener directamente de la Eliminación Gaussiana.
# La matriz U es la matriz triangular superior resultante de la eliminación.
# La matriz L se forma con los factores que usamos para hacer ceros los elementos.

def descomposicion_lu(A):
    """
    Realiza la descomposición LU de una matriz A.

    Parámetros:
        A (numpy.array): Matriz cuadrada de coeficientes.

    Retorna:
        tuple: (L, U) donde L es la matriz triangular inferior y U es la superior.
        None: Si la matriz es singular o no se puede descomponer.
    """

    n = A.shape[0] # Obtener la dimensión de la matriz (número de filas)
    L = np.eye(n)  # Inicializamos L como una matriz identidad (diagonal de unos)
    U = A.copy()   # U comienza como una copia de A

    print("\n--- Parte 2: Ejecución de la Descomposición LU ---")
    print("Matriz A inicial para descomposición:")
    print(U)

    for i in range(n): # Iteramos sobre cada columna (pivote)
        # Verificamos si el elemento pivote es cero.
        if U[i, i] == 0:
            print("\nError: Elemento pivote es cero. La matriz es singular o requiere pivoteo.")
            return None, None # No podemos continuar con esta implementación simple

        for j in range(i + 1, n): # Iteramos sobre las filas debajo del pivote
            factor = U[j, i] / U[i, i]
            L[j, i] = factor # Guardamos el factor en la matriz L
            U[j, i:] = U[j, i:] - factor * U[i, i:] # Eliminación Gaussiana para U

        print(f"\nMatriz U después de la columna {i+1} (eliminación):")
        print(U)
        print(f"Matriz L parcial después de la columna {i+1}:")
        print(L)

    return L, U

def resolver_lu(L, U, b):
    """
    Resuelve el sistema Ax = b usando las matrices L y U obtenidas de la descomposición LU.

    Parámetros:
        L (numpy.array): Matriz triangular inferior.
        U (numpy.array): Matriz triangular superior.
        b (numpy.array): Vector de términos independientes.

    Retorna:
        numpy.array: El vector solución x.
    """
    n = L.shape[0]

    # Paso 1: Resolver Ly = b (Sustitución hacia adelante)
    y = np.zeros(n)
    print("\n--- Paso 1: Resolviendo Ly = b (Sustitución hacia adelante) ---")
    for i in range(n):
        # y[i] = (b[i] - sum(L[i, j] * y[j] for j in range(i))) / L[i, i]
        # Como L[i,i] es 1 en nuestra implementación, se simplifica.
        suma_ly = np.dot(L[i, :i], y[:i]) # Suma de L[i,j]*y[j] para j < i
        y[i] = (b[i] - suma_ly) / L[i, i] # L[i,i] es 1 en esta implementación
        print(f"Calculando y[{i}]: {y[i]:.6f}")

    print("Vector intermedio y:")
    print(y)

    # Paso 2: Resolver Ux = y (Sustitución hacia atrás)
    x = np.zeros(n)
    print("\n--- Paso 2: Resolviendo Ux = y (Sustitución hacia atrás) ---")
    for i in range(n - 1, -1, -1): # Desde la última fila hasta la primera
        # x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, n))) / U[i, i]
        suma_ux = np.dot(U[i, i+1:], x[i+1:]) # Suma de U[i,j]*x[j] para j > i
        x[i] = (y[i] - suma_ux) / U[i, i]
        print(f"Calculando x[{i}]: {x[i]:.6f}")

    return x

# --- Parte 3: Aplicación del Método ---

print("\n--- Parte 3: Aplicación del Método ---")

L, U = descomposicion_lu(A.copy()) # Obtenemos L y U

if L is not None and U is not None:
    print("\nMatriz L (Lower):")
    print(L)
    print("\nMatriz U (Upper):")
    print(U)

    # Verificación: A = L @ U
    print("\nVerificación: L @ U es aproximadamente igual a A?")
    print(L @ U)
    print(np.allclose(L @ U, A))

    solucion = resolver_lu(L, U, b.copy()) # Resolvemos el sistema

    print("\nVector solución x:")
    print(solucion)

    # Verificación final: A @ x = b
    print("\nVerificación final: A @ x es aproximadamente igual a b?")
    print(A @ solucion)
    print(np.allclose(A @ solucion, b))

    # Ejemplo de la ventaja: Resolver con un nuevo vector b_nuevo
    b_nuevo = np.array([10, -15, -5], dtype=float)
    print("\nResolviendo para un nuevo vector b_nuevo:")
    print(b_nuevo)
    solucion_nueva = resolver_lu(L, U, b_nuevo.copy())
    print("Vector solución x_nuevo:")
    print(solucion_nueva)
    print("Verificación final para b_nuevo: A @ x_nuevo es aproximadamente igual a b_nuevo?")
    print(A @ solucion_nueva)
    print(np.allclose(A @ solucion_nueva, b_nuevo))

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La Descomposición LU es crucial en el análisis de elementos finitos (FEM),")
print("donde se resuelven sistemas de ecuaciones lineales muy grandes. Si la")
print("estructura se somete a diferentes conjuntos de cargas (diferentes vectores b),")
print("la matriz de rigidez (matriz A) permanece la misma. Descomponerla una vez")
print("en L y U permite resolver para cada nueva carga de forma muy eficiente.")
print("También se usa en dinámica de fluidos computacional (CFD) y en el análisis")
print("de vibraciones, donde se resuelven sistemas lineales repetidamente.")

print("\n¡Has completado el segundo ejercicio del Capítulo 3!")
print("Ahora entiendes la Descomposición LU y su eficiencia para resolver múltiples")
print("sistemas con la misma matriz de coeficientes.")
