# -*- coding: utf-8 -*-
"""
Capítulo 9: Problemas de Valor en la Frontera (PVF)
Ejercicio 3: Aplicación en Transferencia de Calor (Aleta de Enfriamiento)

Los Problemas de Valor en la Frontera (PVF) son muy comunes en la transferencia
de calor. Un ejemplo clásico es la distribución de temperatura en una aleta de
enfriamiento. Las aletas se utilizan para aumentar la superficie de transferencia
de calor y disipar energía de un objeto caliente al ambiente.

La ecuación diferencial que describe la distribución de temperatura `T(x)` a lo
largo de una aleta de sección transversal uniforme, en estado estacionario y
con convección en la superficie, es una EDO de segundo orden:

d^2T/dx^2 - (hP / kA_c) * (T - T_ambiente) = 0

Donde:
- `T(x)`: Temperatura en la posición `x` a lo largo de la aleta.
- `h`: Coeficiente de transferencia de calor por convección.
- `P`: Perímetro de la aleta.
- `k`: Conductividad térmica del material de la aleta.
- `A_c`: Área de la sección transversal de la aleta.
- `T_ambiente`: Temperatura del ambiente.

Esta EDO se resuelve con condiciones de frontera. Por ejemplo, la temperatura
en la base de la aleta es conocida, y en la punta de la aleta puede haber
convección, ser adiabática, o tener una temperatura conocida.

Resolver este PVF nos permite diseñar aletas eficientes para sistemas de
enfriamiento en motores, electrónica, etc.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 3: Aplicación en Transferencia de Calor (Aleta de Enfriamiento) ---")

# --- Parte 1: Definición del PVF para la Aleta ---
# La EDO es: d^2T/dx^2 - m^2 * (T - T_ambiente) = 0
# Donde m^2 = hP / kA_c

print("\n--- Parte 1: PVF para la Aleta ---")

# Parámetros de la aleta
h = 10.0    # Coeficiente de convección (W/m^2.K)
P = 0.1     # Perímetro de la aleta (m) (ej. aleta rectangular de 0.025m x 0.05m -> P = 2*(0.025+0.05) = 0.15m, ajustado para ejemplo)
k = 200.0   # Conductividad térmica (W/m.K) (ej. Aluminio)
A_c = 0.0005 # Área de la sección transversal (m^2) (ej. 0.025m x 0.02m = 0.0005m^2)
L = 0.1     # Longitud de la aleta (m)
T_ambiente = 25.0 # Temperatura ambiente (°C)
T_base = 100.0 # Temperatura en la base de la aleta (°C)

m_squared = (h * P) / (k * A_c)
print(f"Parámetro m^2 = {m_squared:.4f} (1/m^2)")

# La EDO se puede reescribir como: d^2T/dx^2 = m^2 * T - m^2 * T_ambiente
# Para el método de diferencias finitas, necesitamos la forma: a_i T_i-1 + b_i T_i + c_i T_i+1 = d_i
# Usando la aproximación de diferencia central para la segunda derivada:
# (T_{i-1} - 2T_i + T_{i+1}) / (Δx)^2 - m^2 * T_i = -m^2 * T_ambiente
# T_{i-1} + (-2 - m^2 * (Δx)^2)T_i + T_{i+1} = -m^2 * T_ambiente * (Δx)^2

# --- Parte 2: Implementación del Método de Diferencias Finitas para la Aleta ---

def resolver_aleta_diferencias_finitas(n_nodos, L, T_base, T_ambiente, h_conv, P, k_mat, A_c):
    """
    Resuelve la distribución de temperatura en una aleta usando Diferencias Finitas.
    """
    dx = L / (n_nodos - 1) # Tamaño del paso espacial
    x_valores = np.linspace(0, L, n_nodos)

    # Calculamos el parámetro m_squared
    m_squared_local = (h_conv * P) / (k_mat * A_c)

    # Número de incógnitas (nodos internos)
    num_incognitas = n_nodos - 2

    # Construimos la matriz de coeficientes A y el vector b
    A = np.zeros((num_incognitas, num_incognitas))
b_vector = np.zeros(num_incognitas)

    print(f"\n--- Parte 2: Construyendo el Sistema Lineal para la Aleta (Nodos={n_nodos}, dx={dx:.4f}) ---")

    for i in range(num_incognitas):
        # Coeficiente diagonal
        A[i, i] = (-2 - m_squared_local * (dx**2))

        # Coeficientes fuera de la diagonal
        if i > 0:
            A[i, i-1] = 1
        if i < num_incognitas - 1:
            A[i, i+1] = 1
        
        # Término independiente
        b_vector[i] = -m_squared_local * (dx**2) * T_ambiente

        # Manejo de las condiciones de frontera
        if i == 0: # Primera ecuación interna (afectada por T_base)
            b_vector[i] -= T_base # T_base se pasa al lado derecho
        
        # Condición de frontera en la punta de la aleta (x=L)
        # Asumimos punta adiabática (dT/dx = 0 en x=L) para simplificar.
        # Usando diferencia central: (T_{N-1} - T_{N-3}) / (2*dx) = 0 => T_{N-1} = T_{N-3}
        # O más simple, diferencia hacia atrás: (T_N - T_{N-1}) / dx = 0 => T_N = T_{N-1}
        # Para una punta adiabática, la ecuación en el último nodo interno (i = num_incognitas - 1)
        # se modifica. La ecuación para el nodo N-1 (último interno) es:
        # T_{N-2} + (-2 - m^2*dx^2)T_{N-1} + T_N = -m^2*dx^2*T_ambiente
        # Si T_N = T_{N-1} (adiabática), entonces:
        # T_{N-2} + (-2 - m^2*dx^2 + 1)T_{N-1} = -m^2*dx^2*T_ambiente
        # T_{N-2} + (-1 - m^2*dx^2)T_{N-1} = -m^2*dx^2*T_ambiente
        if i == num_incognitas - 1: # Última ecuación interna
            # Modificamos el coeficiente diagonal para reflejar T_N = T_{N-1}
            A[i, i] = (-1 - m_squared_local * (dx**2)) # El +1 viene de T_N
            # El término T_{N-1} (que era T_N) ya está incluido en el lado izquierdo.

    print("Matriz de Coeficientes A:")
    print(A)
    print("\nVector b:")
    print(b_vector)

    # Resolvemos el sistema lineal para las temperaturas internas
    T_internas = np.linalg.solve(A, b_vector)

    # Construimos la solución completa incluyendo la temperatura de la base
    T_valores = np.concatenate(([T_base], T_internas))
    # Para la punta adiabática, la temperatura en el último nodo es igual a la del penúltimo.
    T_valores = np.append(T_valores, T_internas[-1]) # Añadimos el último nodo

    return x_valores, T_valores

# --- Parte 3: Aplicación y Visualización ---

print("\n--- Parte 3: Aplicación y Visualización ---")

num_nodos_aleta = 10 # Número de nodos. Experimenta con más.

x_sol_aleta, T_sol_aleta = resolver_aleta_diferencias_finitas(num_nodos_aleta, L, T_base, T_ambiente, h, P, k, A_c)

# Solución analítica para una aleta con punta adiabática:
# (T(x) - T_ambiente) / (T_base - T_ambiente) = cosh(m(L-x)) / cosh(mL)
# Donde m = sqrt(hP/kA_c)

def solucion_analitica_aleta(x, L, T_base, T_ambiente, h_conv, P, k_mat, A_c):
    m_val = np.sqrt((h_conv * P) / (k_mat * A_c))
    return T_ambiente + (T_base - T_ambiente) * (np.cosh(m_val * (L - x)) / np.cosh(m_val * L))

x_analitica_aleta = np.linspace(0, L, 100)
T_analitica_aleta = solucion_analitica_aleta(x_analitica_aleta, L, T_base, T_ambiente, h, P, k, A_c)

plt.figure(figsize=(10, 6))
plt.plot(x_analitica_aleta, T_analitica_aleta, color='blue', linestyle='-', label='Solución Analítica')
plt.plot(x_sol_aleta, T_sol_aleta, color='red', linestyle='--', marker='o', markersize=6, label=f'Solución Numérica (Nodos={num_nodos_aleta})')

plt.title('Distribución de Temperatura en una Aleta (Punta Adiabática)')
plt.xlabel('Posición a lo largo de la aleta, x (m)')
plt.ylabel('Temperatura, T (°C)')
plt.grid(True)
plt.legend()
plt.show()

print("\n¡Has modelado la transferencia de calor en una aleta usando diferencias finitas!")
print("Esto es fundamental para el diseño de sistemas de enfriamiento.")
