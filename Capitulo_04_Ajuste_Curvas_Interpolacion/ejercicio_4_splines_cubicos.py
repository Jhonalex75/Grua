# -*- coding: utf-8 -*-
"""
Capítulo 4: Ajuste de Curvas e Interpolación
Ejercicio 4: Splines Cúbicos

La Interpolación Polinomial de Lagrange es excelente para pasar por todos los
puntos de datos, pero a veces, especialmente con muchos puntos, el polinomio
resultante puede tener oscilaciones extrañas entre los puntos (fenómeno de Runge).
Esto puede llevar a estimaciones poco realistas.

Los Splines Cúbicos son una solución a este problema. En lugar de ajustar un
solo polinomio de alto grado a todos los puntos, los splines cúbicos ajustan
múltiples polinomios de tercer grado (cúbicos) entre cada par de puntos de datos
adyacentes. La clave es que estos polinomios se unen de forma muy suave en los
puntos de datos, asegurando que la curva resultante sea continua y tenga
derivadas continuas (sin "picos" o "cambios bruscos de dirección").

Imagina que estás doblando una regla flexible (un spline) para que pase por
varios puntos. La forma que toma la regla es muy similar a la curva que genera
un spline cúbico: es suave y no tiene oscilaciones innecesarias.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline # SciPy tiene una implementación robusta

print("--- Ejercicio 4: Splines Cúbicos ---")

# --- Parte 1: Datos de Ejemplo ---
# Usaremos un conjunto de datos que podría mostrar el fenómeno de Runge con un
# polinomio de alto grado, para apreciar la suavidad del spline.
# Por ejemplo, la trayectoria de un brazo robótico o la forma de un perfil alar.

print("\n--- Parte 1: Datos de Ejemplo ---")

x_puntos = np.array([0, 1, 2, 3, 4, 5, 6])
y_puntos = np.array([0, 0.5, 2.0, 1.5, 3.0, 2.5, 1.0])

print("Puntos x:", x_puntos)
print("Puntos y:", y_puntos)

# Visualizamos los datos.
plt.figure(figsize=(8, 6))
plt.scatter(x_puntos, y_puntos, color='blue', label='Datos Conocidos')
plt.title('Puntos para Interpolación con Splines')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

print("Queremos una curva suave que pase por todos estos puntos.")

# --- Parte 2: Implementación y Uso de Splines Cúbicos con SciPy ---
# Implementar un spline cúbico desde cero es complejo porque implica resolver
# un sistema de ecuaciones para asegurar la continuidad de las derivadas.
# Afortunadamente, la biblioteca SciPy (Scientific Python) ya tiene una
# implementación robusta y optimizada que podemos usar directamente.

print("\n--- Parte 2: Uso de Splines Cúbicos con SciPy ---")

# Creamos el objeto spline cúbico. Esto "ajusta" los polinomios a los datos.
# El parámetro 'bc_type' define las condiciones de contorno en los extremos.
# 'natural' significa que la segunda derivada en los extremos es cero, lo que
# resulta en una curva más "natural" o relajada.
cs = CubicSpline(x_puntos, y_puntos, bc_type='natural')

# Ahora podemos usar este objeto 'cs' para evaluar el spline en cualquier punto.
# Generamos muchos puntos en el rango para dibujar la curva suave.
x_interp = np.linspace(np.min(x_puntos), np.max(x_puntos), 200) # 200 puntos para una curva suave
y_interp = cs(x_interp) # Evaluamos el spline en estos nuevos puntos

# --- Parte 3: Aplicación y Visualización del Spline ---

print("\n--- Parte 3: Aplicación y Visualización ---")

# Estimamos un valor en un punto específico, por ejemplo, en x = 2.5
x_estimar = 2.5
y_estimado = cs(x_estimar)
print(f"El valor estimado en x = {x_estimar} es: {y_estimado:.4f}")

plt.figure(figsize=(8, 6))
plt.scatter(x_puntos, y_puntos, color='blue', label='Datos Conocidos', zorder=5)
plt.plot(x_interp, y_interp, color='red', linestyle='-', label='Spline Cúbico')
plt.scatter(x_estimar, y_estimado, color='green', marker='X', s=100, zorder=6, label=f'Punto Interpolado ({x_estimar}, {y_estimado:.2f})')

plt.title('Interpolación con Spline Cúbico')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

# --- Comparación con Interpolación Lineal (Opcional) ---
# Para mostrar la diferencia en suavidad.

print("\n--- Comparación con Interpolación Lineal ---")
plt.figure(figsize=(8, 6))
plt.scatter(x_puntos, y_puntos, color='blue', label='Datos Conocidos', zorder=5)
plt.plot(x_puntos, y_puntos, color='purple', linestyle='--', label='Interpolación Lineal')
plt.plot(x_interp, y_interp, color='red', linestyle='-', label='Spline Cúbico')
plt.title('Comparación: Spline Cúbico vs. Interpolación Lineal')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

print("Observa cómo el spline cúbico (rojo) es mucho más suave que la interpolación lineal (púrpura).")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("Los splines cúbicos son ampliamente utilizados en el diseño asistido por")
print("computadora (CAD) para modelar formas complejas y suaves, como las superficies")
print("de carrocerías de automóviles, alas de aviones, o hélices de barcos. También")
print("son esenciales en la generación de trayectorias suaves para robots industriales")
print("y en la reconstrucción de datos de sensores donde se requiere una curva continua")
print("y sin oscilaciones. Por ejemplo, al procesar datos de vibración o de deformación")
print("de un componente, los splines pueden ayudar a obtener una representación suave")
print("del comportamiento.")

print("\n¡Has completado el cuarto y último ejercicio del Capítulo 4!")
print("Ahora entiendes la potencia de los Splines Cúbicos para crear curvas suaves")
print("y precisas que pasan por puntos de datos, evitando problemas de oscilación.")
print("¡Felicidades por completar el Capítulo 4: Ajuste de Curvas e Interpolación!")
