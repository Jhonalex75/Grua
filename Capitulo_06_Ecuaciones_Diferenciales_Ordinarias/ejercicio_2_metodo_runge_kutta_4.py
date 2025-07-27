# -*- coding: utf-8 -*-
"""
Capítulo 6: Ecuaciones Diferenciales Ordinarias (EDO)
Ejercicio 2: Método de Runge-Kutta de 4to Orden (RK4)

El Método de Euler es simple, pero su precisión es limitada, especialmente
cuando el tamaño del paso (h) es grande. Para obtener soluciones más precisas
de EDOs, necesitamos métodos más avanzados. Uno de los más populares y efectivos
es el Método de Runge-Kutta de 4to Orden, comúnmente abreviado como RK4.

RK4 es un método de "paso a paso" como Euler, pero en lugar de usar solo la
pendiente al inicio del intervalo, calcula un promedio ponderado de varias
pendientes dentro del intervalo para estimar el siguiente punto. Esto lo hace
mucho más preciso.

Imagina que estás en la montaña y quieres estimar tu nueva posición. En lugar
de solo mirar la pendiente justo donde estás (Euler), RK4 mira la pendiente
donde estás, luego estima la pendiente a mitad de camino, luego otra vez a
mitad de camino con una mejor estimación, y finalmente la pendiente al final
del paso. Con todas esas "pistas", hace una estimación mucho más precisa de
dónde terminarás.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 2: Método de Runge-Kutta de 4to Orden (RK4) ---")

# --- Parte 1: Definición de la EDO y la Condición Inicial ---
# Resolveremos la misma EDO del ejercicio anterior para comparar:
# dy/dx = -2y + x
# Con la condición inicial: y(0) = 1
# La solución analítica de esta EDO es: y(x) = (3/4)e^(-2x) + (1/2)x - (1/4)

def f_edo_rk4(x, y):
    """
    Define la función f(x, y) = dy/dx para la EDO.
    """
    return -2*y + x

def solucion_analitica_rk4(x):
    """
    Solución analítica de la EDO dy/dx = -2y + x con y(0)=1.
    """
    return (3/4) * np.exp(-2*x) + (1/2) * x - (1/4)

# Condición inicial
x0 = 0.0
y0 = 1.0

print("\n--- Parte 1: EDO y Condición Inicial ---")
print(f"EDO: dy/dx = f(x, y) = -2y + x")
print(f"Condición inicial: y({x0}) = {y0}")

# --- Parte 2: Implementación del Método de Runge-Kutta de 4to Orden ---
# Las fórmulas para RK4 son:
# k1 = h * f(x_i, y_i)
# k2 = h * f(x_i + h/2, y_i + k1/2)
# k3 = h * f(x_i + h/2, y_i + k2/2)
# k4 = h * f(x_i + h, y_i + k3)
# y_{i+1} = y_i + (k1 + 2*k2 + 2*k3 + k4) / 6

def metodo_runge_kutta_4(func_edo, x0, y0, x_final, h):
    """
    Resuelve una EDO de primer orden usando el Método de Runge-Kutta de 4to Orden.

    Parámetros:
        func_edo (function): La función f(x, y) = dy/dx.
        x0 (float): Valor inicial de x.
        y0 (float): Valor inicial de y (condición inicial).
        x_final (float): Valor de x hasta donde queremos integrar.
        h (float): Tamaño del paso.

    Retorna:
        tuple: (x_valores, y_valores) arrays con la solución aproximada.
    """

    x_valores = [x0]
    y_valores = [y0]

    x_actual = x0
    y_actual = y0

    print(f"\n--- Parte 2: Ejecución del Método de Runge-Kutta 4to Orden con paso h = {h} ---")

    while x_actual < x_final:
        # Aseguramos que el último paso no exceda x_final
        if x_actual + h > x_final:
            h = x_final - x_actual

        # Calculamos las cuatro pendientes (k1, k2, k3, k4)
        k1 = h * func_edo(x_actual, y_actual)
        k2 = h * func_edo(x_actual + h/2, y_actual + k1/2)
        k3 = h * func_edo(x_actual + h/2, y_actual + k2/2)
        k4 = h * func_edo(x_actual + h, y_actual + k3)

        # Calculamos el nuevo valor de y usando el promedio ponderado de las pendientes
        y_siguiente = y_actual + (k1 + 2*k2 + 2*k3 + k4) / 6

        # Actualizamos x para el siguiente paso
        x_siguiente = x_actual + h

        x_valores.append(x_siguiente)
        y_valores.append(y_siguiente)

        print(f"  x={x_actual:.4f}, y={y_actual:.4f} -> x_siguiente={x_siguiente:.4f}, y_siguiente={y_siguiente:.4f}")

        x_actual = x_siguiente
        y_actual = y_siguiente

    return np.array(x_valores), np.array(y_valores)

# --- Parte 3: Aplicación y Visualización ---

print("\n--- Parte 3: Aplicación y Visualización ---")

x_final_integracion = 2.0 # Integrar hasta x = 2.0
h_paso = 0.2 # Mismo tamaño de paso que en Euler para comparar

x_rk4, y_rk4 = metodo_runge_kutta_4(f_edo_rk4, x0, y0, x_final_integracion, h_paso)

# Calculamos la solución analítica para comparar
x_analitica = np.linspace(x0, x_final_integracion, 100) # Muchos puntos para una curva suave
y_analitica = solucion_analitica_rk4(x_analitica)

plt.figure(figsize=(10, 7))
plt.plot(x_analitica, y_analitica, color='blue', linestyle='-', label='Solución Analítica')
plt.plot(x_rk4, y_rk4, color='green', linestyle='--', marker='s', label=f'Método RK4 (h={h_paso})')

# Opcional: Añadir la solución de Euler para una comparación directa
# from ejercicio_1_metodo_euler import metodo_euler # Si quisieras importarlo
# x_euler, y_euler = metodo_euler(f_edo_rk4, x0, y0, x_final_integracion, h_paso)
# plt.plot(x_euler, y_euler, color='red', linestyle=':', marker='o', label=f'Método de Euler (h={h_paso})')

plt.title('Solución de EDO con el Método de Runge-Kutta de 4to Orden')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

print("\nObserva cómo la solución de RK4 se ajusta mucho mejor a la solución analítica")
print("que el Método de Euler, incluso con el mismo tamaño de paso.")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El Método de Runge-Kutta de 4to Orden es el caballo de batalla para simular")
print("sistemas dinámicos complejos en ingeniería mecánica. Se utiliza para modelar:")
print("- El movimiento de vehículos, cohetes o satélites (ecuaciones de movimiento).")
print("- Sistemas de vibración amortiguados o forzados (EDOs de segundo orden).")
print("- La respuesta de sistemas de control (EDOs que describen la dinámica del sistema).")
print("- La transferencia de calor transitoria en objetos (EDOs que describen el cambio de temperatura).")
print("Su precisión y estabilidad lo hacen indispensable en simulaciones de ingeniería.")

print("\n¡Has completado el segundo ejercicio del Capítulo 6!")
print("Ahora entiendes cómo el Método de Runge-Kutta de 4to Orden proporciona")
print("soluciones mucho más precisas para las ecuaciones diferenciales ordinarias.")

# --- Parte 4: Implementación Genérica del Solucionador RK4 para Sistemas (desde runge_kutta_solver.py) ---
# Esta función es una implementación genérica del método RK4 que puede resolver
# cualquier sistema de EDOs de primer orden. Es ideal para ser reutilizada.

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
    # --- 1. Configurar el array de tiempo ---
    t_start, t_end = t_span
    # Asegurar que el número de pasos sea un entero
    num_steps = int((t_end - t_start) / dt)
    t_values = np.linspace(t_start, t_end, num_steps + 1)

    # --- 2. Inicializar el array de la solución ---
    # Convertir las condiciones iniciales a un array de NumPy para operaciones vectoriales
    y0 = np.array(y0, dtype=float)
    num_variables = len(y0)
    y_values = np.zeros((num_steps + 1, num_variables))
    y_values[0, :] = y0

    # --- 3. El Bucle de Integración RK4 ---
    # Este bucle itera a través de cada paso de tiempo para resolver el sistema.
    for i in range(num_steps):
        t = t_values[i]
        y = y_values[i, :]

        # El núcleo del método RK4 es calcular cuatro "pendientes" (k1, k2, k3, k4)
        # a lo largo del intervalo. Cada 'k' es un array de derivadas para todas las variables.
        k1 = np.array(system_of_odes(t, y), dtype=float)
        k2 = np.array(system_of_odes(t + 0.5 * dt, y + 0.5 * dt * k1), dtype=float)
        k3 = np.array(system_of_odes(t + 0.5 * dt, y + 0.5 * dt * k2), dtype=float)
        k4 = np.array(system_of_odes(t + dt, y + dt * k3), dtype=float)

        # El siguiente valor de y se calcula usando un promedio ponderado de las cuatro pendientes.
        # Las pendientes intermedias (k2, k3) reciben más peso, lo cual es clave para la precisión del método.
        y_next = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        y_values[i + 1, :] = y_next

    return t_values, y_values