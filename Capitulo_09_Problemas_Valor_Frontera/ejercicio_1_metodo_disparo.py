# -*- coding: utf-8 -*-
"""
Capítulo 9: Problemas de Valor en la Frontera (PVF)
Ejercicio 1: Método de Disparo (Shooting Method)

En los capítulos anteriores, resolvimos Ecuaciones Diferenciales Ordinarias (EDO)
como Problemas de Valor Inicial (PVI), donde todas las condiciones se conocían
en un solo punto (el inicio). Sin embargo, en muchos problemas de ingeniería,
las condiciones se conocen en diferentes puntos, generalmente en los límites
o "fronteras" del dominio. Estos son los Problemas de Valor en la Frontera (PVF).

El Método de Disparo es una técnica para resolver PVF que los convierte en PVI.
La idea es "adivinar" una condición inicial desconocida (por ejemplo, la pendiente
inicial), resolver el PVI resultante, y luego ajustar iterativamente esa adivinanza
hasta que la solución del PVI satisfaga la condición en la otra frontera.

Imagina que estás disparando un cañón a un objetivo. No sabes el ángulo exacto
para dar en el blanco. El método de disparo es como ajustar el ángulo de cada
disparo hasta que la trayectoria final (la solución de la EDO) impacta el objetivo
(la condición de frontera).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve # Para encontrar la raíz de la función de error

print("--- Ejercicio 1: Método de Disparo ---")

# --- Parte 1: Definición del PVF de Ejemplo ---
# Resolveremos el siguiente PVF lineal de segundo orden:
# y'' = -y
# Con condiciones de frontera: y(0) = 0, y(pi/2) = 1
# La solución analítica es: y(x) = sin(x)

print("\n--- Parte 1: PVF de Ejemplo ---")

# Convertimos la EDO de segundo orden en un sistema de dos EDOs de primer orden:
# y1 = y
# y2 = y'
# Entonces:
# y1' = y2
# y2' = -y1

def sistema_edos_pvf(x, y_vector):
    """
    Define el sistema de EDOs para el PVF.
    y_vector[0] = y (desplazamiento)
    y_vector[1] = y' (velocidad/pendiente)
    """
    y1, y2 = y_vector
    dy1_dx = y2
    dy2_dx = -y1
    return [dy1_dx, dy2_dx]

# Condiciones de frontera
x_inicio = 0.0
y_inicio = 0.0 # y(0) = 0
x_fin = np.pi / 2
y_fin = 1.0 # y(pi/2) = 1

print(f"PVF: y'' = -y")
print(f"Condiciones de frontera: y({x_inicio}) = {y_inicio}, y({x_fin:.2f}) = {y_fin}")

# --- Parte 2: Implementación del Método de Disparo ---
# La idea es adivinar y'(0) (que es y2(0)), resolver el PVI, y ver si y(pi/2) es 1.
# Si no lo es, ajustamos y'(0) y repetimos.

def funcion_error_disparo(pendiente_inicial_adivinada):
    """
    Esta función toma una pendiente inicial adivinada (y'(0)),
    resuelve el PVI y devuelve la diferencia entre la y calculada en x_fin
    y la y_fin deseada. Queremos que esta diferencia sea cero.
    """
    # La condición inicial para el PVI es [y(0), y'(0)]
    condiciones_iniciales_pvi = [y_inicio, pendiente_inicial_adivinada]

    # Resolvemos el PVI usando solve_ivp
    solucion = solve_ivp(sistema_edos_pvf, [x_inicio, x_fin], condiciones_iniciales_pvi,
                         dense_output=True) # dense_output=True permite evaluar la solución en cualquier punto

    # Evaluamos la solución en x_fin
    y_en_x_fin_calculada = solucion.sol(x_fin)[0] # [0] porque queremos y1 (el desplazamiento)

    # Calculamos el error: la diferencia entre el valor calculado y el deseado en la frontera final
    error = y_en_x_fin_calculada - y_fin
    return error

# --- Parte 3: Aplicación del Método de Disparo ---

print("\n--- Parte 3: Aplicación del Método de Disparo ---")

# Hacemos una suposición inicial para la pendiente y'(0).
# Si no tenemos una buena idea, podemos probar con 0 o 1.
primera_adivinanza_pendiente = 1.0

print(f"Intentando con una pendiente inicial adivinada: {primera_adivinanza_pendiente}")
error_inicial = funcion_error_disparo(primera_adivinanza_pendiente)
print(f"Error inicial en y({x_fin:.2f}): {error_inicial:.4f}")

# Usamos fsolve para encontrar la pendiente inicial que hace que la función_error_disparo sea cero.
# fsolve es un solucionador de raíces (como Newton-Raphson) para funciones.
print("\nBuscando la pendiente inicial correcta usando fsolve...")
pendiente_inicial_correcta = fsolve(funcion_error_disparo, primera_adivinanza_pendiente)[0]

print(f"Pendiente inicial correcta (y'(0)): {pendiente_inicial_correcta:.6f}")

# Ahora, con la pendiente inicial correcta, resolvemos el PVI final para obtener la solución completa.
condiciones_iniciales_final = [y_inicio, pendiente_inicial_correcta]
solucion_final = solve_ivp(sistema_edos_pvf, [x_inicio, x_fin], condiciones_iniciales_final,
                           dense_output=True, t_eval=np.linspace(x_inicio, x_fin, 100))

x_sol = solucion_final.t
y_sol = solucion_final.y[0, :]

# --- Parte 4: Visualización de la Solución ---

print("\n--- Parte 4: Visualización de la Solución ---")

# Solución analítica para comparar: y(x) = sin(x)
x_analitica = np.linspace(x_inicio, x_fin, 100)
y_analitica = np.sin(x_analitica)

plt.figure(figsize=(10, 6))
plt.plot(x_analitica, y_analitica, color='blue', linestyle='-', label='Solución Analítica: sin(x)')
plt.plot(x_sol, y_sol, color='red', linestyle='--', marker='o', markersize=4, label='Solución Numérica (Método de Disparo)')
plt.scatter([x_inicio, x_fin], [y_inicio, y_fin], color='green', s=100, zorder=5, label='Condiciones de Frontera')

plt.title('Solución de PVF con el Método de Disparo')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

print("\n¡Has resuelto un Problema de Valor en la Frontera usando el Método de Disparo!")
print("Este método es muy útil cuando las condiciones se conocen en diferentes puntos del dominio.")
