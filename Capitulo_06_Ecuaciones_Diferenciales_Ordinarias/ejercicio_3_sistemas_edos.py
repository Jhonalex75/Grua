# -*- coding: utf-8 -*-
"""
Capítulo 6: Ecuaciones Diferenciales Ordinarias (EDO)
Ejercicio 3: Sistemas de Ecuaciones Diferenciales Ordinarias

En la realidad, muchos sistemas dinámicos en ingeniería no se describen con
una sola EDO, sino con un conjunto de EDOs interconectadas. Por ejemplo,
el movimiento de un objeto en 2D o 3D (donde la posición en x, y, z y la
velocidad en x, y, z son variables que cambian con el tiempo), o la interacción
de múltiples componentes en un sistema de control.

Un sistema de EDOs de primer orden se puede escribir de la forma:

dy1/dx = f1(x, y1, y2, ..., yn)
dy2/dx = f2(x, y1, y2, ..., yn)
...
dyn/dx = fn(x, y1, y2, ..., yn)

Donde y1, y2, ..., yn son las variables dependientes que cambian con x.

La buena noticia es que los métodos numéricos como Euler o Runge-Kutta
pueden extenderse para resolver sistemas de EDOs. La idea es aplicar el
mismo principio de "paso a paso" a cada ecuación del sistema simultáneamente.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 3: Sistemas de Ecuaciones Diferenciales Ordinarias ---")

# --- Parte 1: Definición del Sistema de EDOs y Condiciones Iniciales ---
# Resolveremos un sistema simple de dos EDOs acopladas:
# dy1/dx = y2
# dy2/dx = -y1
# Esto describe un oscilador armónico simple (como un resorte sin amortiguamiento).
# Con condiciones iniciales: y1(0) = 0, y2(0) = 1
# La solución analítica es: y1(x) = sin(x), y2(x) = cos(x)

def sistema_edos(x, y_vector):
    """
    Define el sistema de EDOs. y_vector es un array de NumPy donde:
    y_vector[0] = y1
    y_vector[1] = y2

    Retorna un array con las derivadas [dy1/dx, dy2/dx].
    """
    y1 = y_vector[0]
    y2 = y_vector[1]

    dy1_dx = y2
    dy2_dx = -y1

    return np.array([dy1_dx, dy2_dx])

def solucion_analitica_sistema(x):
    """
    Solución analítica del sistema de EDOs.
    """
    y1_sol = np.sin(x)
    y2_sol = np.cos(x)
    # Retornar un array 2D donde cada fila es una variable dependiente
    return np.vstack([y1_sol, y2_sol])

# Condiciones iniciales
x0 = 0.0
y_inicial_vector = np.array([0.0, 1.0]) # [y1(0), y2(0)]

print("\n--- Parte 1: Sistema de EDOs y Condiciones Iniciales ---")
print(f"Sistema de EDOs: dy1/dx = y2, dy2/dx = -y1")
print(f"Condiciones iniciales: y1({x0}) = {y_inicial_vector[0]}, y2({x0}) = {y_inicial_vector[1]}")

# --- Parte 2: Implementación del Método de Runge-Kutta de 4to Orden para Sistemas ---
# La extensión de RK4 para sistemas es directa: las k1, k2, k3, k4 se convierten
# en vectores, y las operaciones se realizan elemento a elemento.

def metodo_runge_kutta_4_sistema(func_sistema_edos, x0, y_inicial_vector, x_final, h):
    """
    Resuelve un sistema de EDOs de primer orden usando el Método de Runge-Kutta de 4to Orden.

    Parámetros:
        func_sistema_edos (function): La función que define el sistema de EDOs.
                                      Debe tomar (x, y_vector) y retornar un array de derivadas.
        x0 (float): Valor inicial de x.
        y_inicial_vector (numpy.array): Vector de valores iniciales de las variables dependientes.
        x_final (float): Valor de x hasta donde queremos integrar.
        h (float): Tamaño del paso.

    Retorna:
        tuple: (x_valores, y_valores_matriz) donde x_valores es un array de x,
               y y_valores_matriz es una matriz donde cada fila es el vector y en un x dado.
    """

    x_valores = [x0]
    y_valores_matriz = [y_inicial_vector]

    x_actual = x0
    y_actual_vector = y_inicial_vector.copy()

    print(f"\n--- Parte 2: Ejecución de RK4 para Sistemas con paso h = {h} ---")

    while x_actual < x_final:
        if x_actual + h > x_final:
            h = x_final - x_actual

        # Calculamos las cuatro pendientes (k1, k2, k3, k4) como VECTORES
        k1 = h * func_sistema_edos(x_actual, y_actual_vector)
        k2 = h * func_sistema_edos(x_actual + h/2, y_actual_vector + k1/2)
        k3 = h * func_sistema_edos(x_actual + h/2, y_actual_vector + k2/2)
        k4 = h * func_sistema_edos(x_actual + h, y_actual_vector + k3)

        # Calculamos el nuevo vector y usando el promedio ponderado de las pendientes
        y_siguiente_vector = y_actual_vector + (k1 + 2*k2 + 2*k3 + k4) / 6

        x_siguiente = x_actual + h

        x_valores.append(x_siguiente)
        y_valores_matriz.append(y_siguiente_vector)

        print(f"  x={x_actual:.4f}, y={y_actual_vector} -> x_siguiente={x_siguiente:.4f}, y_siguiente={y_siguiente_vector}")

        x_actual = x_siguiente
        y_actual_vector = y_siguiente_vector

    return np.array(x_valores), np.array(y_valores_matriz)

# --- Parte 3: Aplicación y Visualización ---

print("\n--- Parte 3: Aplicación y Visualización ---")

x_final_integracion = 4 * np.pi # Integrar por dos ciclos completos
h_paso = 0.1 # Tamaño del paso

x_sol, y_sol_matriz = metodo_runge_kutta_4_sistema(sistema_edos, x0, y_inicial_vector, x_final_integracion, h_paso)

# Extraemos las soluciones para y1 y y2
y1_sol_numerica = y_sol_matriz[:, 0] # Primera columna es y1
y2_sol_numerica = y_sol_matriz[:, 1] # Segunda columna es y2

# Calculamos la solución analítica para comparar
x_analitica = np.linspace(x0, x_final_integracion, 200) # Muchos puntos para una curva suave
y_analitica_matriz = solucion_analitica_sistema(x_analitica)
y1_sol_analitica = y_analitica_matriz[0, :]
y2_sol_analitica = y_analitica_matriz[1, :]

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1) # Gráfico 1 de 2
plt.plot(x_analitica, y1_sol_analitica, color='blue', linestyle='-', label='y1 Analítica')
plt.plot(x_sol, y1_sol_numerica, color='red', linestyle='--', marker='o', markersize=4, label='y1 RK4')
plt.title('Solución de y1(x)')
plt.xlabel('x')
plt.ylabel('y1')
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2) # Gráfico 2 de 2
plt.plot(x_analitica, y2_sol_analitica, color='blue', linestyle='-', label='y2 Analítica')
plt.plot(x_sol, y2_sol_numerica, color='red', linestyle='--', marker='s', markersize=4, label='y2 RK4')
plt.title('Solución de y2(x)')
plt.xlabel('x')
plt.ylabel('y2')
plt.grid(True)
plt.legend()

plt.tight_layout() # Ajusta el diseño para evitar superposiciones
plt.show()

# También podemos graficar la trayectoria en el espacio de fase (y1 vs y2)
plt.figure(figsize=(7, 7))
plt.plot(y1_sol_analitica, y2_sol_analitica, color='blue', linestyle='-', label='Trayectoria Analítica')
plt.plot(y1_sol_numerica, y2_sol_numerica, color='red', linestyle='--', marker='.', label='Trayectoria RK4')
plt.scatter(y_inicial_vector[0], y_inicial_vector[1], color='green', s=100, zorder=5, label='Punto Inicial')
plt.title('Espacio de Fase (y2 vs y1)')
plt.xlabel('y1')
plt.ylabel('y2')
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.legend()
plt.show()

print("\nObserva cómo el método RK4 sigue de cerca la solución analítica para ambas variables.")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La resolución de sistemas de EDOs es fundamental para modelar sistemas")
print("dinámicos complejos. Por ejemplo:")
print("- **Vibraciones:** Un sistema masa-resorte-amortiguador se describe con")
print("  una EDO de segundo orden, que se puede convertir en un sistema de dos EDOs")
print("  de primer orden (posición y velocidad).")
print("- **Dinámica de Fluidos:** Modelado de flujos no estacionarios o reacciones")
print("  químicas en reactores.")
print("- **Robótica:** Simulación del movimiento de brazos robóticos o vehículos")
print("  autónomos, donde las ecuaciones de movimiento son un sistema de EDOs.")
print("- **Termodinámica:** Análisis de sistemas de transferencia de calor con")
print("  múltiples componentes interactuando.")

print("\n¡Has completado el tercer ejercicio del Capítulo 6!")
print("Ahora entiendes cómo extender los métodos numéricos para resolver sistemas")
print("de ecuaciones diferenciales ordinarias, lo que abre la puerta a la simulación")
print("de sistemas dinámicos más realistas.")
