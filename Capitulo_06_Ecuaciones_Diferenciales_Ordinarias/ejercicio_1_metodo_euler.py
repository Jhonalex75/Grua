# -*- coding: utf-8 -*-
"""
Capítulo 6: Ecuaciones Diferenciales Ordinarias (EDO)
Ejercicio 1: Método de Euler

En ingeniería, muchos fenómenos se describen mediante Ecuaciones Diferenciales
Ordinarias (EDO). Por ejemplo, el movimiento de un péndulo, la descarga de un
condensador, el enfriamiento de un objeto, o la velocidad de una reacción química.
Una EDO relaciona una función con sus derivadas.

Una EDO de primer orden simple tiene la forma: dy/dx = f(x, y).
Esto significa que la tasa de cambio de 'y' con respecto a 'x' depende de 'x' y de 'y'.

El Método de Euler es el método numérico más básico para aproximar la solución
de una EDO. Es un método de "paso a paso": si conocemos un punto (x0, y0),
podemos usar la pendiente en ese punto (dada por f(x0, y0)) para estimar el
siguiente punto (x1, y1).

Imagina que estás caminando por un terreno montañoso y tienes un mapa que te
dice la pendiente en cada punto. Si quieres saber dónde estarás después de dar
un pequeño paso, puedes usar la pendiente actual para estimar tu nueva posición.
El Método de Euler hace esto repetidamente para "trazar" la solución de la EDO.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 1: Método de Euler ---")

# --- Parte 1: Definición de la EDO y la Condición Inicial ---
# Resolveremos la EDO: dy/dx = -2y + x
# Con la condición inicial: y(0) = 1
# La solución analítica de esta EDO es: y(x) = (3/4)e^(-2x) + (1/2)x - (1/4)

def f_edo(x, y):
    """
    Define la función f(x, y) = dy/dx para la EDO.
    """
    return -2*y + x

def solucion_analitica(x):
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

# --- Parte 2: Implementación del Método de Euler ---
# La fórmula de Euler es:
# y_{i+1} = y_i + f(x_i, y_i) * h
# Donde h es el tamaño del paso (step size).

def metodo_euler(func_edo, x0, y0, x_final, h):
    """
    Resuelve una EDO de primer orden usando el Método de Euler.

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

    print(f"\n--- Parte 2: Ejecución del Método de Euler con paso h = {h} ---")

    # Bucle para avanzar paso a paso hasta x_final
    while x_actual < x_final:
        # Aseguramos que el último paso no exceda x_final
        if x_actual + h > x_final:
            h = x_final - x_actual

        # Calculamos la pendiente en el punto actual
        pendiente = func_edo(x_actual, y_actual)

        # Calculamos el nuevo valor de y
        y_siguiente = y_actual + pendiente * h

        # Actualizamos x para el siguiente paso
        x_siguiente = x_actual + h

        x_valores.append(x_siguiente)
        y_valores.append(y_siguiente)

        print(f"  x={x_actual:.4f}, y={y_actual:.4f}, Pendiente={pendiente:.4f} -> x_siguiente={x_siguiente:.4f}, y_siguiente={y_siguiente:.4f}")

        x_actual = x_siguiente
        y_actual = y_siguiente

    return np.array(x_valores), np.array(y_valores)

# --- Parte 3: Aplicación y Visualización ---

print("\n--- Parte 3: Aplicación y Visualización ---")

x_final_integracion = 2.0 # Integrar hasta x = 2.0
h_paso = 0.2 # Tamaño del paso. Experimenta con valores más pequeños (ej. 0.1, 0.05)

x_euler, y_euler = metodo_euler(f_edo, x0, y0, x_final_integracion, h_paso)

# Calculamos la solución analítica para comparar
x_analitica = np.linspace(x0, x_final_integracion, 100) # Muchos puntos para una curva suave
y_analitica = solucion_analitica(x_analitica)

plt.figure(figsize=(10, 7))
plt.plot(x_analitica, y_analitica, color='blue', linestyle='-', label='Solución Analítica')
plt.plot(x_euler, y_euler, color='red', linestyle='--', marker='o', label=f'Método de Euler (h={h_paso})')

plt.title('Solución de EDO con el Método de Euler')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

print("\nObserva cómo la solución de Euler se desvía de la solución analítica a medida que avanzamos.")
print("Un tamaño de paso (h) más pequeño generalmente produce una mejor aproximación.")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El Método de Euler, aunque simple, es la base para entender cómo se simulan")
print("sistemas dinámicos. Por ejemplo, para modelar el enfriamiento de un objeto")
print("según la Ley de Enfriamiento de Newton (dT/dt = -k(T - Ta)), donde T es la")
print("temperatura del objeto y Ta es la temperatura ambiente. También se puede usar")
print("para simular el movimiento de un objeto bajo la influencia de la gravedad y")
print("la resistencia del aire, o la descarga de un tanque de agua con un orificio.")
print("Aunque no es el método más preciso, su simplicidad lo hace ideal para entender")
print("el concepto de integración numérica de EDOs.")

print("\n¡Has completado el primer ejercicio del Capítulo 6!")
print("Ahora entiendes cómo el Método de Euler nos permite aproximar la solución")
print("de ecuaciones diferenciales ordinarias paso a paso.")
