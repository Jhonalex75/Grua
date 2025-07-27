# -*- coding: utf-8 -*-
"""
Capítulo 6: Ecuaciones Diferenciales Ordinarias (EDO)
Ejercicio 5: Simulación de un Sistema Masa-Resorte-Amortiguador

Este ejercicio demuestra cómo aplicar el solucionador genérico de Runge-Kutta
de 4to Orden (RK4) que hemos integrado en el Ejercicio 2 para simular un
sistema dinámico clásico en ingeniería mecánica: el sistema masa-resorte-amortiguador.

Un sistema masa-resorte-amortiguador es fundamental para entender las vibraciones
y la dinámica de muchos sistemas mecánicos, desde la suspensión de un coche
hasta el comportamiento de estructuras bajo cargas dinámicas.

La ecuación diferencial de segundo orden que describe este sistema es:

m * (d^2x/dt^2) + c * (dx/dt) + k * x = F_ext(t)

Donde:
- m: masa
- c: coeficiente de amortiguamiento
- k: constante del resorte
- x: desplazamiento
- F_ext(t): fuerza externa aplicada en función del tiempo

Para resolver esta EDO de segundo orden con un método como RK4, primero debemos
convertirla en un sistema de dos EDOs de primer orden. Hacemos esto definiendo
una nueva variable para la velocidad:

v = dx/dt

Entonces, el sistema de EDOs de primer orden es:
1. dx/dt = v
2. dv/dt = (F_ext(t) - c*v - k*x) / m

Ahora podemos usar nuestro solucionador RK4 para encontrar x y v en función del tiempo.
"""

import numpy as np
import matplotlib.pyplot as plt

# Importamos el solucionador RK4 genérico que definimos en el ejercicio 2.
# Asegúrate de que este script se ejecute en el mismo entorno o que la función
# solve_rk4_generico esté disponible (por ejemplo, copiándola aquí o importándola).
# Para este ejercicio, la incluiremos directamente para que sea autocontenido.

def solve_rk4_generico(system_of_odes, y0, t_span, dt):
    """
    Resuelve un sistema de EDOs de primer orden usando el método RK4.

    Parámetros:
        system_of_odes (function): La función que define el sistema de EDOs.
                                   Debe tomar `t` (tiempo) y `y` (un array de NumPy de variables de estado)
                                   como argumentos y retornar un array de NumPy de las derivadas (dy/dt).
        y0 (list or np.ndarray): Una lista o array de las condiciones iniciales para las variables de estado
                                 [y1(0), y2(0), ...].
        t_span (tuple): Una tupla que contiene el tiempo de inicio y fin para la simulación, ej., (0, 10).
        dt (float): El tamaño del paso (h) para la integración. Un `dt` más pequeño aumenta
                    la precisión pero también el tiempo de cálculo.

    Retorna:
        tuple: Una tupla que contiene dos arrays de NumPy:
               - t_values: El array de puntos de tiempo desde t_inicio hasta t_fin.
               - y_values: Un array de NumPy 2D donde cada fila corresponde a un punto de tiempo y cada
                           columna corresponde a una variable de estado en el sistema.
    """
    t_start, t_end = t_span
    num_steps = int((t_end - t_start) / dt)
    t_values = np.linspace(t_start, t_end, num_steps + 1)

    y0 = np.array(y0, dtype=float)
    num_variables = len(y0)
    y_values = np.zeros((num_steps + 1, num_variables))
    y_values[0, :] = y0

    for i in range(num_steps):
        t = t_values[i]
        y = y_values[i, :]

        k1 = np.array(system_of_odes(t, y), dtype=float)
        k2 = np.array(system_of_odes(t + 0.5 * dt, y + 0.5 * dt * k1), dtype=float)
        k3 = np.array(system_of_odes(t + 0.5 * dt, y + 0.5 * dt * k2), dtype=float)
        k4 = np.array(system_of_odes(t + dt, y + dt * k3), dtype=float)

        y_next = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        y_values[i + 1, :] = y_next

    return t_values, y_values

print("--- Ejercicio 5: Simulación de Sistema Masa-Resorte-Amortiguador ---")

# --- Parte 1: Definición del Modelo Físico (Sistema de EDOs) ---

def mass_spring_damper_system(t, y_vector, m, c, k, F_ext_func):
    """
    Define el sistema de EDOs para un sistema masa-resorte-amortiguador.

    La EDO de 2do orden `m*x'' + c*x' + k*x = F(t)` se convierte en un
    sistema de dos EDOs de 1er orden:
    1. dx/dt = v          (donde y_vector[0] es el desplazamiento x, y_vector[1] es la velocidad v)
    2. dv/dt = (F_ext(t) - c*v - k*x) / m

    Parámetros:
        t (float): El tiempo actual.
        y_vector (np.ndarray): Un array de NumPy [desplazamiento, velocidad].
        m (float): Masa (kg).
        c (float): Coeficiente de amortiguamiento (N*s/m).
        k (float): Constante del resorte (N/m).
        F_ext_func (function): Una función que retorna la fuerza externa en el tiempo t.

    Retorna:
        np.ndarray: Un array de las derivadas [dx/dt, dv/dt].
    """
    desplazamiento, velocidad = y_vector
    
    d_desplazamiento_dt = velocidad
    d_velocidad_dt = (F_ext_func(t) - c * velocidad - k * desplazamiento) / m
    
    return np.array([d_desplazamiento_dt, d_velocidad_dt])

# --- Parte 2: Definición de la Fuerza Externa ---
# Podemos definir diferentes tipos de fuerzas externas. Aquí, una fuerza de impulso.

def fuerza_impulso(t):
    """
    Define una fuerza externa que es un impulso corto.
    """
    return 1000.0 if t < 0.1 else 0.0

# --- Parte 3: Parámetros del Modelo y Simulación ---

print("\n--- Parte 3: Parámetros del Modelo y Simulación ---")

m = 250.0  # Masa (kg)
c = 100.0  # Coeficiente de amortiguamiento (N*s/m)
k = 15000.0 # Constante del resorte (N/m)

condiciones_iniciales = [0.0, 0.0]  # [desplazamiento inicial, velocidad inicial]
tiempo_simulacion = (0.0, 5.0)           # (tiempo_inicio, tiempo_fin) en segundos
tamano_paso = 0.01                 # dt para el solucionador

# Para pasar los parámetros del modelo a la función `system_of_odes` que espera `solve_rk4_generico`,
# usamos una función lambda. Esto "envuelve" nuestra función del sistema y pre-llena los parámetros.
sistema_a_resolver = lambda t, y: mass_spring_damper_system(t, y, m, c, k, fuerza_impulso)

# --- Parte 4: Llamada al Solucionador RK4 Genérico ---

print("\n--- Parte 4: Llamada al Solucionador RK4 Genérico ---")

t_valores, y_valores = solve_rk4_generico(sistema_a_resolver, condiciones_iniciales, tiempo_simulacion, tamano_paso)

# Los resultados están en y_valores. La primera columna es el desplazamiento, la segunda es la velocidad.
desplazamiento_resultados = y_valores[:, 0]
velocidad_resultados = y_valores[:, 1]

print("Simulación completada. Graficando resultados...")

# --- Parte 5: Visualización de los Resultados ---

plt.style.use('seaborn-v0_8-whitegrid') # Un estilo de gráfico agradable
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Desplazamiento (m)', color='tab:blue')
ax1.plot(t_valores, desplazamiento_resultados, color='tab:blue', label='Desplazamiento')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True)

# Creamos un segundo eje Y para la velocidad
ax2 = ax1.twinx()
ax2.set_ylabel('Velocidad (m/s)', color='tab:red')
ax2.plot(t_valores, velocidad_resultados, color='tab:red', linestyle='--', label='Velocidad')
ax2.tick_params(axis='y', labelcolor='tab:red')

fig.suptitle('Respuesta del Sistema Masa-Resorte-Amortiguador (RK4)', fontsize=16)
fig.tight_layout(rect=[0, 0, 1, 0.96]) # Ajusta el diseño para que el título no se superponga
plt.show()

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La simulación de sistemas masa-resorte-amortiguador es fundamental para el diseño")
print("y análisis de sistemas de suspensión de vehículos, amortiguadores de vibración")
print("en maquinaria, o el comportamiento dinámico de edificios y puentes bajo cargas")
print("sísmicas o de viento. Permite a los ingenieros predecir cómo se moverá un sistema")
print("y cómo disipará energía, lo cual es crucial para garantizar la seguridad y el rendimiento.")

print("\n¡Has completado el quinto ejercicio del Capítulo 6!")
print("Ahora sabes cómo modelar y simular un sistema dinámico real utilizando")
print("un solucionador de EDOs genérico.")
