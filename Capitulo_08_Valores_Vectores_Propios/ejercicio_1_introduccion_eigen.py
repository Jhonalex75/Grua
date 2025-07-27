# -*- coding: utf-8 -*-
"""
Capítulo 8: Valores y Vectores Propios
Ejercicio 1: Introducción a Valores y Vectores Propios

Este ejercicio introduce de manera intuitiva los conceptos de valores y vectores
propios. Imagina que tienes una transformación (como estirar, rotar o reflejar)
que aplicas a diferentes vectores. Un vector propio es especial porque, después
de la transformación, sigue apuntando en la misma dirección (o exactamente en la
dirección opuesta), solo que su longitud cambia. El factor por el que cambia su
longitud es el valor propio.

En ingeniería, esto es crucial porque nos ayuda a entender las "direcciones
fundamentales" o los "modos naturales" de un sistema. Por ejemplo, en vibraciones,
los vectores propios nos dicen cómo se deforma una estructura cuando vibra a
ciertas frecuencias (los valores propios).
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 1: Introducción a Valores y Vectores Propios ---")

# --- Parte 1: Definición de una Matriz de Transformación ---
# Una matriz puede representar una transformación lineal. Vamos a usar una matriz 2x2
# para que podamos visualizar fácilmente lo que le hace a los vectores en un plano.

print("\n--- Parte 1: Matriz de Transformación ---")

A = np.array([
    [2, 1],
    [1, 2]
])

print("Matriz de Transformación A:")
print(A)

# --- Parte 2: Visualización de la Transformación en Vectores Aleatorios ---
# Vamos a ver qué le sucede a algunos vectores "normales" cuando los multiplicamos por A.

print("\n--- Parte 2: Transformación de Vectores Aleatorios ---")

vectores_originales = np.array([
    [1, 0],  # Vector en el eje X
    [0, 1],  # Vector en el eje Y
    [1, 1],  # Vector diagonal
    [-1, 2]  # Otro vector
]).T # .T transpone la matriz para que cada columna sea un vector

vectores_transformados = A @ vectores_originales # Multiplicación matricial

plt.figure(figsize=(8, 8))
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.grid(True, linestyle=':')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.gca().set_aspect('equal', adjustable='box') # Asegura que los ejes tengan la misma escala

for i in range(vectores_originales.shape[1]):
    plt.quiver(0, 0, vectores_originales[0, i], vectores_originales[1, i], 
               angles='xy', scale_units='xy', scale=1, color='blue', width=0.008, 
               label='Vector Original' if i == 0 else "")
    plt.quiver(0, 0, vectores_transformados[0, i], vectores_transformados[1, i], 
               angles='xy', scale_units='xy', scale=1, color='red', width=0.005, 
               label='Vector Transformado' if i == 0 else "")

plt.title('Transformación de Vectores por la Matriz A')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

print("Observa cómo la mayoría de los vectores cambian tanto de dirección como de longitud.")

# --- Parte 3: Encontrando y Visualizando un Vector Propio ---
# Ahora, vamos a encontrar los valores y vectores propios de esta matriz.
# NumPy tiene una función para esto.

print("\n--- Parte 3: Vector Propio ---")

valores_propios, vectores_propios = np.linalg.eig(A)

print("Valores Propios (λ):")
print(valores_propios)
print("\nVectores Propios (v) (cada columna es un vector propio):")
print(vectores_propios)

# Seleccionamos el primer par (valor propio, vector propio)
lambda1 = valores_propios[0]
v1 = vectores_propios[:, 0]

print(f"\nPrimer Valor Propio (λ1): {lambda1:.2f}")
print(f"Primer Vector Propio (v1): {v1}")

# Multiplicamos la matriz A por el vector propio v1
Av1 = A @ v1

print(f"\nA @ v1: {Av1}")
print(f"λ1 * v1: {lambda1 * v1}")

print("Observa que A @ v1 es un múltiplo escalar de v1. ¡Esa es la definición de un vector propio!")

# Visualizamos el vector propio y su transformación
plt.figure(figsize=(8, 8))
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.grid(True, linestyle=':')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.gca().set_aspect('equal', adjustable='box')

plt.quiver(0, 0, v1[0], v1[1], 
           angles='xy', scale_units='xy', scale=1, color='blue', width=0.008, 
           label='Vector Propio Original (v1)')
plt.quiver(0, 0, Av1[0], Av1[1], 
           angles='xy', scale_units='xy', scale=1, color='red', width=0.005, 
           label='Vector Propio Transformado (A @ v1)')

plt.title(f'Transformación de un Vector Propio (λ={lambda1:.2f})')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

print("\n¡Felicidades! Has dado tus primeros pasos en el mundo de los valores y vectores propios.")
print("Estos conceptos son la clave para entender el comportamiento intrínseco de muchos sistemas de ingeniería.")
