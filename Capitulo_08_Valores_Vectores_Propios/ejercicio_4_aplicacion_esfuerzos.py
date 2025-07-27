# -*- coding: utf-8 -*-
"""
Capítulo 8: Valores y Vectores Propios
Ejercicio 4: Aplicación en Análisis de Esfuerzos (Esfuerzos Principales)

En el análisis de resistencia de materiales, es crucial entender cómo se distribuyen
los esfuerzos dentro de un componente. Un estado de esfuerzo en un punto puede
ser complejo, con componentes normales (perpendiculares a una superficie) y
cortantes (paralelas a una superficie) en diferentes direcciones.

Sin embargo, siempre existen ciertas orientaciones en las que los esfuerzos
cortantes son cero y los esfuerzos normales alcanzan sus valores máximos o
mínimos. Estos son los **esfuerzos principales**, y las direcciones en las que
actúan son las **direcciones principales**.

Los valores y vectores propios son la herramienta matemática perfecta para
encontrar estos esfuerzos y direcciones principales a partir del tensor de
esfuerzos. Los valores propios serán los esfuerzos principales, y los vectores
propios serán las direcciones principales.

Imagina que estás analizando una pieza sometida a cargas complejas. En lugar
de preocuparte por los esfuerzos en cada orientación posible, los esfuerzos
principales te dan los valores críticos que debes considerar para el diseño
y la seguridad de la pieza.
"""

import numpy as np

print("--- Ejercicio 4: Aplicación en Análisis de Esfuerzos (Esfuerzos Principales) ---")

# --- Parte 1: Definición del Tensor de Esfuerzos (Estado de Esfuerzo Plano) ---
# En un estado de esfuerzo plano (2D), el tensor de esfuerzos se representa como una matriz 2x2:
# Sigma = [[sigma_x, tau_xy],
#          [tau_yx,  sigma_y]]
# Donde sigma_x y sigma_y son los esfuerzos normales, y tau_xy (o tau_yx) es el esfuerzo cortante.
# Por equilibrio, tau_xy = tau_yx.

print("\n--- Parte 1: Tensor de Esfuerzos ---")

# Ejemplo de un estado de esfuerzo plano (unidades en MPa)
sigma_x = 50.0
sigma_y = -30.0 # Compresión
tau_xy = 20.0

tensor_esfuerzos = np.array([
    [sigma_x, tau_xy],
    [tau_xy,  sigma_y]
])

print("Tensor de Esfuerzos (MPa):")
print(tensor_esfuerzos)

# --- Parte 2: Cálculo de Esfuerzos y Direcciones Principales ---
# Los esfuerzos principales son los valores propios del tensor de esfuerzos.
# Las direcciones principales son los vectores propios correspondientes.

print("\n--- Parte 2: Cálculo de Esfuerzos y Direcciones Principales ---")

esfuerzos_principales, direcciones_principales = np.linalg.eig(tensor_esfuerzos)

# Los valores propios son los esfuerzos principales (sigma_1, sigma_2)
sigma1 = esfuerzos_principales[0]
sigma2 = esfuerzos_principales[1]

# Los vectores propios son las direcciones principales (v1, v2)
v1 = direcciones_principales[:, 0]
v2 = direcciones_principales[:, 1]

print("\nEsfuerzos Principales (MPa):")
print(f"Sigma_1 (Esfuerzo Principal Mayor): {sigma1:.2f} MPa")
print(f"Sigma_2 (Esfuerzo Principal Menor): {sigma2:.2f} MPa")

print("\nDirecciones Principales (Vectores Propios):")
print(f"Dirección Principal 1 (v1): {v1}")
print(f"Dirección Principal 2 (v2): {v2}")

# --- Parte 3: Interpretación de las Direcciones Principales ---
# Los vectores propios nos dan la dirección. Podemos convertirlos a ángulos.
# El ángulo se mide desde el eje x positivo.

print("\n--- Parte 3: Interpretación de Direcciones ---")

# Ángulo de la primera dirección principal (en radianes y grados)
# np.arctan2(y, x) es mejor que arctan(y/x) porque maneja todos los cuadrantes.
angulo1_rad = np.arctan2(v1[1], v1[0])
angulo1_deg = np.degrees(angulo1_rad)
print(f"Ángulo de la Dirección Principal 1: {angulo1_deg:.2f}°")

# Ángulo de la segunda dirección principal
angulo2_rad = np.arctan2(v2[1], v2[0])
angulo2_deg = np.degrees(angulo2_rad)
print(f"Ángulo de la Dirección Principal 2: {angulo2_deg:.2f}°")

print("\nLas dos direcciones principales son perpendiculares entre sí (90° de diferencia).")
print("En estas direcciones, los esfuerzos cortantes son cero.")

# --- Verificación (Opcional) ---
# Podemos verificar que el tensor de esfuerzos transformado a las direcciones principales
# es una matriz diagonal con los esfuerzos principales en la diagonal.

# Matriz de transformación de coordenadas (matriz de rotación)
# Las columnas son los vectores propios normalizados
Q = direcciones_principales

# Tensor de esfuerzos en el sistema de coordenadas principal: Sigma_p = Q_T @ Sigma @ Q
sigma_principal_matriz = Q.T @ tensor_esfuerzos @ Q

print("\nTensor de Esfuerzos en el Sistema de Coordenadas Principal:")
print(sigma_principal_matriz)
print("\nObserva que los elementos fuera de la diagonal son muy cercanos a cero (errores de redondeo).")
print("Los elementos de la diagonal son los esfuerzos principales.")

print("\n¡Has aplicado valores y vectores propios para el análisis de esfuerzos!")
print("Esto es crucial para el diseño seguro y eficiente de componentes mecánicos.")
