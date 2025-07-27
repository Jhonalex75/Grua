# -*- coding: utf-8 -*-
"""
Capítulo 5: Diferenciación e Integración Numérica
Ejercicio 1: Diferenciación Numérica

En ingeniería, la derivada de una función representa la tasa de cambio de una
cantidad con respecto a otra. Por ejemplo, la velocidad es la derivada de la
posición con respecto al tiempo, y la aceleración es la derivada de la velocidad.
La pendiente de una curva de esfuerzo-deformación es el módulo de elasticidad.

A veces, no tenemos una función matemática explícita para derivar (por ejemplo,
si tenemos datos de sensores o resultados de experimentos). En estos casos,
necesitamos la Diferenciación Numérica, que nos permite aproximar la derivada
usando los valores de la función en puntos cercanos.

Imagina que tienes una serie de mediciones de la posición de un vehículo en
diferentes momentos. No tienes una ecuación de movimiento, pero quieres saber
su velocidad (derivada de la posición) en un instante dado. La diferenciación
numérica te permite estimar esa velocidad.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 1: Diferenciación Numérica ---")

# --- Parte 1: Definición de la Función y Datos de Ejemplo ---
# Usaremos una función conocida para poder comparar la derivada numérica con la analítica.
# Función: f(x) = x^2
# Derivada analítica: f'(x) = 2x

def funcion_diferenciacion(x):
    """
    Función de ejemplo: f(x) = x^2
    """
    return x**2

def derivada_analitica(x):
    """
    Derivada analítica de f(x) = x^2, que es f'(x) = 2x
    """
    return 2*x

# Puntos de datos para la diferenciación numérica
x_data = np.array([1.0, 1.1, 1.2, 1.3, 1.4, 1.5])
y_data = funcion_diferenciacion(x_data)

print("\n--- Parte 1: Función y Datos de Ejemplo ---")
print("Datos x:", x_data)
print("Datos y (f(x)):", y_data)

# --- Parte 2: Fórmulas de Diferenciación Numérica ---
# Hay varias formas de aproximar la derivada. Las más comunes son:
# 1. Diferencia hacia adelante (Forward Difference)
# 2. Diferencia hacia atrás (Backward Difference)
# 3. Diferencia central (Central Difference)

# Sea h el tamaño del paso (la distancia entre los puntos x).

# 2.1. Diferencia hacia adelante: f'(x) ≈ (f(x + h) - f(x)) / h
#    Usa el punto actual y el siguiente.

# 2.2. Diferencia hacia atrás: f'(x) ≈ (f(x) - f(x - h)) / h
#    Usa el punto actual y el anterior.

# 2.3. Diferencia central: f'(x) ≈ (f(x + h) - f(x - h)) / (2h)
#    Usa un punto antes y un punto después. Generalmente más precisa.

def diferencia_hacia_adelante(func, x, h):
    """
    Aproxima la derivada de func en x usando la diferencia hacia adelante.
    """
    return (func(x + h) - func(x)) / h

def diferencia_hacia_atras(func, x, h):
    """
    Aproxima la derivada de func en x usando la diferencia hacia atrás.
    """
    return (func(x) - func(x - h)) / h

def diferencia_central(func, x, h):
    """
    Aproxima la derivada de func en x usando la diferencia central.
    """
    return (func(x + h) - func(x - h)) / (2 * h)

# --- Parte 3: Aplicación y Comparación ---

print("\n--- Parte 3: Aplicación y Comparación ---")

# Elegimos un punto para calcular la derivada y un tamaño de paso h.
# En datos discretos, h es la diferencia entre puntos adyacentes.
x_punto = 1.2 # Queremos la derivada en x = 1.2
h_paso = x_data[1] - x_data[0] # h = 1.1 - 1.0 = 0.1

print(f"Punto de interés (x): {x_punto}")
print(f"Tamaño de paso (h): {h_paso}")

derivada_analitica_val = derivada_analitica(x_punto)
print(f"\nDerivada Analítica en x={x_punto}: {derivada_analitica_val:.4f}")

# Diferencia hacia adelante
# Para x=1.2, necesitamos f(1.2) y f(1.3)
derivada_adelante = diferencia_hacia_adelante(funcion_diferenciacion, x_punto, h_paso)
print(f"Derivada Hacia Adelante: {derivada_adelante:.4f} (Error: {abs(derivada_adelante - derivada_analitica_val):.4e})")

# Diferencia hacia atrás
# Para x=1.2, necesitamos f(1.2) y f(1.1)
derivada_atras = diferencia_hacia_atras(funcion_diferenciacion, x_punto, h_paso)
print(f"Derivada Hacia Atrás:    {derivada_atras:.4f} (Error: {abs(derivada_atras - derivada_analitica_val):.4e})")

# Diferencia central
# Para x=1.2, necesitamos f(1.1) y f(1.3)
derivada_central = diferencia_central(funcion_diferenciacion, x_punto, h_paso)
print(f"Derivada Central:        {derivada_central:.4f} (Error: {abs(derivada_central - derivada_analitica_val):.4e})")

print("\nObserva que la diferencia central suele ser la más precisa.")

# --- Parte 4: Visualización de las Pendientes ---

plt.figure(figsize=(10, 7))
plt.plot(x_data, y_data, 'o-', label='f(x) = x^2 (Datos)', color='blue')

# Punto de interés
plt.scatter(x_punto, funcion_diferenciacion(x_punto), color='red', s=100, zorder=5, label='Punto de Interés')

# Dibujar las líneas de las pendientes
# Hacia adelante
x_adelante = np.array([x_punto, x_punto + h_paso])
y_adelante = funcion_diferenciacion(x_adelante)
plt.plot(x_adelante, y_adelante, '--', color='green', label='Pendiente Hacia Adelante')

# Hacia atrás
x_atras = np.array([x_punto - h_paso, x_punto])
y_atras = funcion_diferenciacion(x_atras)
plt.plot(x_atras, y_atras, '--', color='purple', label='Pendiente Hacia Atrás')

# Central
x_central = np.array([x_punto - h_paso, x_punto + h_paso])
y_central = funcion_diferenciacion(x_central)
plt.plot(x_central, y_central, '--', color='orange', label='Pendiente Central')

plt.title('Diferenciación Numérica: Aproximación de la Pendiente')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La diferenciación numérica es esencial cuando se analizan datos de sensores")
print("en tiempo real. Por ejemplo, si un acelerómetro mide la posición de un")
print("componente, la diferenciación numérica se usa para estimar su velocidad y")
print("aceleración. También es crucial en el análisis de vibraciones, donde se")
print("derivan señales de desplazamiento para obtener velocidades y aceleraciones.")
print("En termodinámica, si tenemos datos de entalpía en función de la temperatura,")
print("podemos usar diferenciación numérica para estimar el calor específico.")

print("\n¡Has completado el primer ejercicio del Capítulo 5!")
print("Ahora entiendes cómo aproximar la derivada de una función usando datos discretos.")
