# -*- coding: utf-8 -*-
"""
Capítulo 8: Valores y Vectores Propios
Ejercicio 3: Aplicación en Análisis de Vibraciones

Una de las aplicaciones más importantes de los valores y vectores propios en
ingeniería mecánica es el análisis de vibraciones. Muchos sistemas mecánicos
pueden modelarse como un conjunto de masas interconectadas por resortes y
amortiguadores. Cuando estos sistemas vibran, lo hacen a ciertas frecuencias
"naturales" y con patrones de movimiento específicos, llamados "modos de vibración".

Los valores propios de la matriz de un sistema vibratorio nos dan las frecuencias
naturales al cuadrado, y los vectores propios nos describen las formas de esos
modos de vibración. Comprender esto es vital para diseñar estructuras que eviten
la resonancia (vibraciones excesivas) o para diagnosticar problemas en máquinas.

Imagina que tienes un edificio y quieres saber cómo se moverá cuando haya un
terremoto. Los valores y vectores propios te dirán a qué frecuencias es más
vulnerable el edificio y cómo se balanceará en cada una de esas frecuencias.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 3: Aplicación en Análisis de Vibraciones ---")

# --- Parte 1: Definición del Sistema Vibratorio (2 Grados de Libertad) ---
# Consideremos un sistema simple de dos masas (m1, m2) y dos resortes (k1, k2).
# Las ecuaciones de movimiento, sin amortiguamiento ni fuerzas externas, se pueden
# escribir en forma matricial como: M * x'' + K * x = 0
# Donde M es la matriz de masa y K es la matriz de rigidez.

print("\n--- Parte 1: Sistema Vibratorio ---")

# Parámetros del sistema
m1 = 1.0 # kg
m2 = 1.0 # kg
k1 = 100.0 # N/m
k2 = 100.0 # N/m

# Matriz de Masa (M) - Diagonal, con las masas en la diagonal
M = np.array([
    [m1, 0],
    [0, m2]
])

# Matriz de Rigidez (K) - Depende de cómo están conectados los resortes
# Para este sistema simple (masas en serie con resortes):
# K = [[k1+k2, -k2],
#      [-k2,    k2]]
K = np.array([
    [k1 + k2, -k2],
    [-k2,      k2]
])

print("Matriz de Masa (M):")
print(M)
print("\nMatriz de Rigidez (K):")
print(K)

# --- Parte 2: Formulación del Problema de Valores Propios ---
# El problema de valores propios para vibraciones libres no amortiguadas es:
# (K - ω^2 * M) * φ = 0
# Donde ω^2 son los valores propios (frecuencias naturales al cuadrado)
# y φ son los vectores propios (modos de vibración).
# Esto se puede reescribir como: (M^-1 * K) * φ = ω^2 * φ
# Así, los valores propios de la matriz (M^-1 * K) son las frecuencias naturales al cuadrado.

print("\n--- Parte 2: Cálculo de Frecuencias y Modos ---")

M_inv = np.linalg.inv(M) # Inversa de la matriz de masa

A_vibracion = M_inv @ K # Matriz para el problema de valores propios

print("\nMatriz A para el problema de vibración (M^-1 * K):")
print(A_vibracion)

# Calculamos los valores y vectores propios de A_vibracion
# Los valores propios serán ω^2 (frecuencias naturales al cuadrado)
# Los vectores propios serán los modos de vibración
valores_propios_omega_cuadrado, modos_vibracion = np.linalg.eig(A_vibracion)

# Las frecuencias naturales (ω) son la raíz cuadrada de los valores propios.
# Aseguramos que sean reales y positivas.
frecuencias_naturales_rad_s = np.sqrt(np.abs(valores_propios_omega_cuadrado))

# Convertimos a Hertz (Hz): f = ω / (2π)
frecuencias_naturales_hz = frecuencias_naturales_rad_s / (2 * np.pi)

print("\nValores Propios (ω^2) (rad^2/s^2):")
print(valores_propios_omega_cuadrado)
print("\nFrecuencias Naturales (ω) (rad/s):")
print(frecuencias_naturales_rad_s)
print("\nFrecuencias Naturales (f) (Hz):")
print(frecuencias_naturales_hz)

print("\nModos de Vibración (vectores propios - cada columna es un modo):")
print(modos_vibracion)

# --- Parte 3: Interpretación y Visualización de los Modos de Vibración ---
# Los modos de vibración nos dicen las formas en que el sistema tiende a vibrar.
# Para un sistema de 2 masas, el vector propio [x1, x2] nos dice la relación
# de amplitudes entre las dos masas para ese modo.

print("\n--- Parte 3: Interpretación de Modos de Vibración ---")

# Modo 1
modo1 = modos_vibracion[:, 0]
print(f"\nModo de Vibración 1 (Frecuencia: {frecuencias_naturales_hz[0]:.2f} Hz): {modo1}")
# Normalizamos el modo para que la primera componente sea 1 (o -1) para facilitar la visualización
modo1_normalizado = modo1 / modo1[0]
print(f"  (Normalizado respecto a la primera masa): {modo1_normalizado}")
print("  Esto significa que la masa 2 se mueve {modo1_normalizado[1]:.2f} veces la amplitud de la masa 1 en este modo.")

# Modo 2
modo2 = modos_vibracion[:, 1]
print(f"\nModo de Vibración 2 (Frecuencia: {frecuencias_naturales_hz[1]:.2f} Hz): {modo2}")
modo2_normalizado = modo2 / modo2[0]
print(f"  (Normalizado respecto a la primera masa): {modo2_normalizado}")
print("  Esto significa que la masa 2 se mueve {modo2_normalizado[1]:.2f} veces la amplitud de la masa 1 en este modo.")

# Visualización conceptual de los modos (simplificada)
plt.figure(figsize=(10, 5))

# Dibujar el sistema en equilibrio
plt.subplot(1, 3, 1)
plt.plot([0, 0], [0, 1], 'k-', linewidth=2) # Pared
plt.plot([-0.5, 0.5], [1, 1], 'k-', linewidth=2) # Resorte 1
plt.plot([-0.5, 0.5], [2, 2], 'k-', linewidth=2) # Resorte 2
plt.plot([-0.2, 0.2], [1.5, 1.5], 's', markersize=20, color='gray', label='Masa 1')
plt.plot([-0.2, 0.2], [2.5, 2.5], 's', markersize=20, color='darkgray', label='Masa 2')
plt.title('Sistema en Equilibrio')
plt.xlim(-1, 1)
plt.ylim(0, 3)
plt.axis('off')

# Dibujar Modo 1
plt.subplot(1, 3, 2)
plt.plot([0, 0], [0, 1], 'k-', linewidth=2)
plt.plot([-0.5, 0.5], [1, 1], 'k-', linewidth=2)
plt.plot([-0.5, 0.5], [2, 2], 'k-', linewidth=2)
plt.plot([-0.2 + modo1_normalizado[0]*0.5, 0.2 + modo1_normalizado[0]*0.5], [1.5, 1.5], 's', markersize=20, color='gray')
plt.plot([-0.2 + modo1_normalizado[1]*0.5, 0.2 + modo1_normalizado[1]*0.5], [2.5, 2.5], 's', markersize=20, color='darkgray')
plt.title(f'Modo 1 ({frecuencias_naturales_hz[0]:.2f} Hz)')
plt.xlim(-1, 1)
plt.ylim(0, 3)
plt.axis('off')

# Dibujar Modo 2
plt.subplot(1, 3, 3)
plt.plot([0, 0], [0, 1], 'k-', linewidth=2)
plt.plot([-0.5, 0.5], [1, 1], 'k-', linewidth=2)
plt.plot([-0.5, 0.5], [2, 2], 'k-', linewidth=2)
plt.plot([-0.2 + modo2_normalizado[0]*0.5, 0.2 + modo2_normalizado[0]*0.5], [1.5, 1.5], 's', markersize=20, color='gray')
plt.plot([-0.2 + modo2_normalizado[1]*0.5, 0.2 + modo2_normalizado[1]*0.5], [2.5, 2.5], 's', markersize=20, color='darkgray')
plt.title(f'Modo 2 ({frecuencias_naturales_hz[1]:.2f} Hz)')
plt.xlim(-1, 1)
plt.ylim(0, 3)
plt.axis('off')

plt.tight_layout()
plt.show()

print("\n¡Has aplicado valores y vectores propios para entender las vibraciones de un sistema!")
print("Esto es fundamental para el diseño de máquinas y estructuras seguras y eficientes.")
