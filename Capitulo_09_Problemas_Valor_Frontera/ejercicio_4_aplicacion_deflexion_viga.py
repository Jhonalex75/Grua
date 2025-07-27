# -*- coding: utf-8 -*-
"""
Capítulo 9: Problemas de Valor en la Frontera (PVF)
Ejercicio 4: Aplicación en Mecánica de Materiales (Deflexión de Vigas)

Otro problema clásico de valor en la frontera en ingeniería mecánica es el
cálculo de la deflexión de vigas bajo carga. La deflexión de una viga es la
cantidad en que se dobla o se desplaza bajo la acción de fuerzas externas.

La ecuación diferencial que describe la deflexión `v(x)` de una viga elástica
lineal, en el caso de una carga distribuida `w(x)`, es una EDO de cuarto orden:

E * I * (d^4v/dx^4) = w(x)

Donde:
- `E`: Módulo de elasticidad del material de la viga.
- `I`: Momento de inercia de la sección transversal de la viga.
- `w(x)`: Carga distribuida a lo largo de la viga.

Para resolver esta EDO de cuarto orden con el Método de Diferencias Finitas,
la convertimos en un sistema de EDOs de primer orden o aplicamos directamente
aproximaciones de diferencias finitas para la cuarta derivada. Las condiciones
de frontera dependen de los tipos de apoyo de la viga (empotrada, simplemente
apoyada, libre).

Calcular la deflexión es crucial para asegurar que una estructura sea segura
y cumpla con los requisitos de servicio (que no se deforme excesivamente).
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 4: Aplicación en Mecánica de Materiales (Deflexión de Vigas) ---")

# --- Parte 1: Definición del PVF para la Deflexión de Viga ---
# Resolveremos la deflexión de una viga simplemente apoyada con carga uniforme.
# Ecuación: E * I * v'''' = -w0 (carga uniforme hacia abajo)
# Condiciones de frontera para viga simplemente apoyada de longitud L:
# v(0) = 0 (deflexión cero en el inicio)
# v(L) = 0 (deflexión cero en el final)
# v''(0) = 0 (momento flector cero en el inicio)
# v''(L) = 0 (momento flector cero en el final)

print("\n--- Parte 1: PVF para la Deflexión de Viga ---")

# Parámetros de la viga
E = 200e9 # Módulo de elasticidad (Pa) - Acero
I = 1.0e-6 # Momento de inercia (m^4) - Sección rectangular pequeña
L = 5.0 # Longitud de la viga (m)
w0 = 1000.0 # Carga uniforme distribuida (N/m)

print(f"Viga de longitud {L} m, E={E:.1e} Pa, I={I:.1e} m^4, w0={w0} N/m")

# La EDO de cuarto orden se puede aproximar con diferencias finitas.
# v''''(x) ≈ (v_{i-2} - 4v_{i-1} + 6v_i - 4v_{i+1} + v_{i+2}) / (Δx)^4
# Sustituyendo en la EDO: E * I * (v_{i-2} - 4v_{i-1} + 6v_i - 4v_{i+1} + v_{i+2}) / (Δx)^4 = -w0
# (v_{i-2} - 4v_{i-1} + 6v_i - 4v_{i+1} + v_{i+2}) = -w0 * (Δx)^4 / (E * I)

# --- Parte 2: Implementación del Método de Diferencias Finitas para la Viga ---

def resolver_deflexion_viga_diferencias_finitas(n_nodos, L, E, I, w0):
    """
    Resuelve la deflexión de una viga simplemente apoyada usando Diferencias Finitas.
    """
    dx = L / (n_nodos - 1) # Tamaño del paso espacial
    x_valores = np.linspace(0, L, n_nodos)

    # El número de incógnitas es n_nodos - 2 (excluyendo los nodos de frontera v(0) y v(L))
    # Sin embargo, las condiciones de momento flector (v''(0)=0, v''(L)=0) requieren nodos "ficticios"
    # o una modificación de las ecuaciones en la frontera.
    # Para una viga simplemente apoyada, v(0)=0 y v(L)=0 son las condiciones primarias.
    # Las condiciones de momento flector se incorporan en las ecuaciones de los nodos adyacentes a la frontera.

    # Para una viga simplemente apoyada, las condiciones v''(0)=0 y v''(L)=0 implican:
    # v_{-1} = -v_1 (para x=0)
    # v_{N} = -v_{N-2} (para x=L)
    # Esto reduce el número de incógnitas a n_nodos - 2.

    num_incognitas = n_nodos - 2 # Nodos internos (desde i=1 hasta i=n_nodos-2)

    # Construimos la matriz de coeficientes A y el vector b para el sistema lineal Av = b
    A = np.zeros((num_incognitas, num_incognitas))
    b_vector = np.zeros(num_incognitas)

    print(f"\n--- Parte 2: Construyendo el Sistema Lineal para la Viga (Nodos={n_nodos}, dx={dx:.4f}) ---")

    # Llenamos la matriz A y el vector b
    # Las ecuaciones se forman para los nodos internos i = 1, ..., n_nodos-2
    # La ecuación para el nodo i es:
    # v_{i-2} - 4v_{i-1} + 6v_i - 4v_{i+1} + v_{i+2} = -w0 * (Δx)^4 / (E * I)

    constante_rhs = -w0 * (dx**4) / (E * I)

    for i in range(num_incognitas): # i_ecuacion va de 0 a num_incognitas-1
        # El nodo real en la viga es i_real = i + 1
        # v_{i_real-2} - 4v_{i_real-1} + 6v_{i_real} - 4v_{i_real+1} + v_{i_real+2} = RHS

        # Coeficiente para v_i (diagonal principal)
        A[i, i] = 6

        # Coeficientes para v_{i-1} y v_{i+1}
        if i > 0: # v_{i-1}
            A[i, i-1] = -4
        if i < num_incognitas - 1: # v_{i+1}
            A[i, i+1] = -4

        # Coeficientes para v_{i-2} y v_{i+2}
        if i > 1: # v_{i-2}
            A[i, i-2] = 1
        if i < num_incognitas - 2: # v_{i+2}
            A[i, i+2] = 1

        # Manejo de las condiciones de frontera (v(0)=0, v(L)=0, v''(0)=0, v''(L)=0)
        # Para v''(0)=0, implica v_{-1} = v_1. En la ecuación para i=1 (primer nodo interno):
        # v_{-1} - 4v_0 + 6v_1 - 4v_2 + v_3 = RHS
        # Como v_0=0 y v_{-1}=v_1, se convierte en:
        # v_1 + 6v_1 - 4v_2 + v_3 = RHS => 7v_1 - 4v_2 + v_3 = RHS
        if i == 0: # Ecuación para el nodo 1 (i_real=1)
            A[i, i] += 1 # Suma 1 a 6, haciendo 7 (por v_{-1} = v_1)
            # El término v_0 es 0, así que no afecta el RHS.

        # Para v''(L)=0, implica v_{N} = v_{N-2}. En la ecuación para i=n_nodos-2 (último nodo interno):
        # v_{N-4} - 4v_{N-3} + 6v_{N-2} - 4v_{N-1} + v_N = RHS
        # Como v_{N-1}=0 y v_N=v_{N-2}, se convierte en:
        # v_{N-4} - 4v_{N-3} + 6v_{N-2} + v_{N-2} = RHS => v_{N-4} - 4v_{N-3} + 7v_{N-2} = RHS
        if i == num_incognitas - 1: # Ecuación para el nodo n_nodos-2 (i_real=n_nodos-2)
            A[i, i] += 1 # Suma 1 a 6, haciendo 7 (por v_N = v_{N-2})
            # El término v_{N-1} es 0, así que no afecta el RHS.

        b_vector[i] = constante_rhs

    print("Matriz de Coeficientes A:")
    print(A)
    print("\nVector b:")
    print(b_vector)

    # Resolvemos el sistema lineal para las deflexiones internas
    v_internas = np.linalg.solve(A, b_vector)

    # Construimos la solución completa incluyendo los valores de frontera (v(0)=0, v(L)=0)
    v_valores = np.concatenate(([0.0], v_internas, [0.0]))

    return x_valores, v_valores

# --- Parte 3: Aplicación y Visualización ---

print("\n--- Parte 3: Aplicación y Visualización ---")

num_nodos_viga = 10 # Número de nodos. Experimenta con más.

x_sol_viga, v_sol_viga = resolver_deflexion_viga_diferencias_finitas(num_nodos_viga, L, E, I, w0)

# Solución analítica para una viga simplemente apoyada con carga uniforme:
# v(x) = (w0 / (24 * E * I)) * (x^4 - 2 * L * x^3 + L^3 * x)

def solucion_analitica_viga(x, L, E, I, w0):
    return (w0 / (24 * E * I)) * (x**4 - 2 * L * x**3 + L**3 * x)

x_analitica_viga = np.linspace(0, L, 100)
v_analitica_viga = solucion_analitica_viga(x_analitica_viga, L, E, I, w0)

plt.figure(figsize=(10, 6))
plt.plot(x_analitica_viga, v_analitica_viga, color='blue', linestyle='-', label='Solución Analítica')
plt.plot(x_sol_viga, v_sol_viga, color='red', linestyle='--', marker='o', markersize=6, label=f'Solución Numérica (Nodos={num_nodos_viga})')

plt.title('Deflexión de Viga Simplemente Apoyada con Carga Uniforme')
plt.xlabel('Posición a lo largo de la viga, x (m)')
plt.ylabel('Deflexión, v (m)')
plt.grid(True)
plt.legend()
plt.show()

print("\n¡Has modelado la deflexión de una viga usando diferencias finitas!")
print("Esto es esencial para el diseño estructural y la seguridad.")
