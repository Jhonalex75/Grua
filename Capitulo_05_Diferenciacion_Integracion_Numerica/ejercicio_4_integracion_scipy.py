# -*- coding: utf-8 -*-
"""
Capítulo 5: Diferenciación e Integración Numérica
Ejercicio 4: Integración con SciPy

Aunque es fundamental entender cómo funcionan los métodos de integración
numérica (como la Regla del Trapecio o Simpson), en la práctica, para la
mayoría de las aplicaciones de ingeniería, no necesitamos implementar estos
algoritmos desde cero. Python, a través de la biblioteca SciPy (Scientific Python),
ofrece herramientas muy potentes, optimizadas y fáciles de usar para la
integración numérica.

SciPy es una colección de algoritmos y funciones matemáticas construidas
sobre NumPy. Su módulo `scipy.integrate` proporciona varias funciones para
integración, tanto para funciones definidas analíticamente como para datos discretos.

Este ejercicio te mostrará cómo usar las funciones más comunes de SciPy para
realizar integración numérica de manera eficiente y confiable.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, simpson, trapezoid # Importamos las funciones específicas

print("--- Ejercicio 4: Integración con SciPy ---")

# --- Parte 1: Definición de la Función y el Intervalo ---
# Usaremos la misma función de los ejercicios anteriores para comparar.
# Función: f(x) = x^2
# Integral analítica de x^2 entre a y b: (b^3 / 3) - (a^3 / 3)

def funcion_scipy(x):
    """
    Función de ejemplo: f(x) = x^2
    """
    return x**2

def integral_analitica_scipy(a, b):
    """
    Integral analítica de f(x) = x^2 entre a y b.
    """
    return (b**3 / 3) - (a**3 / 3)

# Definimos el intervalo de integración
a = 0.0 # Límite inferior
b = 2.0 # Límite superior

print("\n--- Parte 1: Función y Intervalo de Integración ---")
print(f"Función: f(x) = x^2")
print(f"Intervalo de integración: [{a}, {b}]")

integral_exacta = integral_analitica_scipy(a, b)
print(f"Valor de la integral exacta (analítica): {integral_exacta:.6f}")

# --- Parte 2: Integración de Funciones Definidas Analíticamente (quad) ---
# La función `quad` (de "quadrature") es la herramienta principal de SciPy
# para integrar funciones de una sola variable. Es muy precisa y adaptativa.

print("\n--- Parte 2: Integración de Funciones con `quad` ---")

# `quad` devuelve una tupla: (valor_de_la_integral, estimacion_del_error)
integral_quad, error_quad = quad(funcion_scipy, a, b)

print(f"Integral con `quad`: {integral_quad:.6f}")
print(f"Error estimado por `quad`: {error_quad:.2e}")
print(f"Error absoluto real: {abs(integral_quad - integral_exacta):.6e}")

# --- Parte 3: Integración de Datos Discretos (simpson, trapezoid) ---
# Cuando solo tenemos un conjunto de puntos (x, y) y no una función explícita.

print("\n--- Parte 3: Integración de Datos Discretos ---")

# Generamos algunos datos discretos de nuestra función
x_datos = np.linspace(a, b, 10) # 10 puntos entre a y b
y_datos = funcion_scipy(x_datos)

print("Datos x:", x_datos)
print("Datos y (f(x)):", y_datos)

# Usando `trapezoid` (equivalente a nuestra implementación de la Regla del Trapecio)
integral_trapezoid = trapezoid(y_datos, x_datos)
print(f"Integral con `trapezoid` (SciPy): {integral_trapezoid:.6f}")
print(f"Error absoluto real: {abs(integral_trapezoid - integral_exacta):.6e}")

# Usando `simpson` (equivalente a nuestra implementación de la Regla de Simpson 1/3)
# Requiere un número impar de puntos (o par de subintervalos).
# Si tenemos un número par de puntos, simpson puede usar la regla 3/8 para el último segmento.
integral_simpson = simpson(y_datos, x_datos)
print(f"Integral con `simpson` (SciPy): {integral_simpson:.6f}")
print(f"Error absoluto real: {abs(integral_simpson - integral_exacta):.6e}")

# --- Parte 4: Visualización ---

plt.figure(figsize=(10, 7))
plt.plot(x_datos, y_datos, 'o-', color='blue', label='Datos Discretos')

x_plot_cont = np.linspace(a, b, 400)
y_plot_cont = funcion_scipy(x_plot_cont)
plt.plot(x_plot_cont, y_plot_cont, color='gray', linestyle='--', alpha=0.5, label='Función Continua')

plt.fill_between(x_plot_cont, y_plot_cont, color='lightblue', alpha=0.3, label='Área bajo la curva')

plt.title('Integración Numérica con SciPy')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El uso de `scipy.integrate` es la forma más común y recomendada de realizar")
print("integración numérica en proyectos de ingeniería. Por ejemplo, para calcular")
print("la energía total consumida por un motor a lo largo de un ciclo de operación")
print("a partir de datos de potencia vs. tiempo, o para determinar el volumen de")
print("un depósito irregular a partir de mediciones de área de sección transversal")
print("a diferentes alturas. También es crucial en el análisis de vibraciones para")
print("obtener el desplazamiento a partir de la aceleración (integrando dos veces),")
print("o en el cálculo de la cantidad de calor transferido en un proceso no estacionario.")

print("\n¡Has completado el cuarto y último ejercicio del Capítulo 5!")
print("Ahora sabes cómo usar las potentes herramientas de SciPy para la integración")
print("numérica, lo que te ahorrará mucho tiempo y esfuerzo en tus proyectos.")
print("¡Felicidades por completar el Capítulo 5: Diferenciación e Integración Numérica!")
