# -*- coding: utf-8 -*-
"""
Capítulo 8: Valores y Vectores Propios
Ejercicio 2: Cálculo de Valores y Vectores Propios con NumPy

En el ejercicio anterior, vimos la idea detrás de los valores y vectores propios.
En la práctica, no los calculamos "a mano" para matrices grandes. La biblioteca
NumPy, a través de su módulo `numpy.linalg` (álgebra lineal), proporciona
funciones eficientes y optimizadas para realizar estos cálculos.

Este ejercicio se centrará en cómo usar `np.linalg.eig` para obtener los
valores y vectores propios de una matriz, y cómo verificar que cumplen la
relación fundamental `Av = λv`.

Esto es como tener una calculadora avanzada que te da directamente las
propiedades intrínsecas de un sistema complejo, sin tener que hacer los
cálculos tediosos manualmente.
"""

import numpy as np

print("--- Ejercicio 2: Cálculo de Valores y Vectores Propios con NumPy ---")

# --- Parte 1: Definición de una Matriz de Ejemplo ---
# Usaremos una matriz 3x3 para demostrar el cálculo.
# Esta matriz podría representar, por ejemplo, un tensor de inercia o una matriz
# de rigidez simplificada en un sistema de 3 grados de libertad.

print("\n--- Parte 1: Matriz de Ejemplo ---")

A = np.array([
    [4, 2, 0],
    [2, 5, 0],
    [0, 0, 3]
])

print("Matriz A:")
print(A)

# --- Parte 2: Cálculo con `np.linalg.eig` ---
# La función `np.linalg.eig(A)` devuelve dos cosas:
# 1. Un array con los valores propios (eigenvalues).
# 2. Una matriz donde cada columna es un vector propio (eigenvector) correspondiente.

print("\n--- Parte 2: Cálculo con `np.linalg.eig` ---")

valores_propios, vectores_propios = np.linalg.eig(A)

print("Valores Propios (λ):")
print(valores_propios)
print("\nVectores Propios (v) (cada columna es un vector propio):")
print(vectores_propios)

# --- Parte 3: Verificación de la Ecuación Fundamental (Av = λv) ---
# Para cada par (valor propio, vector propio), debe cumplirse que A @ v = λ * v.
# Vamos a verificar esto para cada par.

print("\n--- Parte 3: Verificación de Av = λv ---")

for i in range(len(valores_propios)):
    lambda_i = valores_propios[i]
    v_i = vectores_propios[:, i] # Seleccionamos la i-ésima columna como el i-ésimo vector propio

    print(f"\n--- Par {i+1} ---")
    print(f"Valor Propio (λ{i+1}): {lambda_i:.4f}")
    print(f"Vector Propio (v{i+1}): {v_i}")

    # Calculamos A @ v_i
    Av_i = A @ v_i
    print(f"A @ v{i+1}: {Av_i}")

    # Calculamos λ_i * v_i
    lambda_v_i = lambda_i * v_i
    print(f"λ{i+1} * v{i+1}: {lambda_v_i}")

    # Comparamos si son aproximadamente iguales (importante para números flotantes)
    es_aproximadamente_igual = np.allclose(Av_i, lambda_v_i)
    print(f"¿A @ v{i+1} es aproximadamente igual a λ{i+1} * v{i+1}? {es_aproximadamente_igual}")

    if not es_aproximadamente_igual:
        print("¡Advertencia! La verificación falló para este par. Puede haber un problema.")

print("\n¡Excelente! Ahora sabes cómo calcular y verificar valores y vectores propios")
print("de cualquier matriz usando las potentes herramientas de NumPy.")
print("Esto es un paso crucial para el análisis de sistemas complejos en ingeniería.")
