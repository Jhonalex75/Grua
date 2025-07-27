# -*- coding: utf-8 -*-
"""
Capítulo 5: Diferenciación e Integración Numérica
Ejercicio 3: Integración Numérica - Regla de Simpson 1/3

La Regla del Trapecio es un buen comienzo para la integración numérica, pero
a veces necesitamos mayor precisión sin usar una cantidad excesiva de subintervalos.
Aquí es donde la Regla de Simpson 1/3 se vuelve muy útil.

En lugar de aproximar el área bajo la curva con trapecios (líneas rectas),
la Regla de Simpson 1/3 lo hace usando parábolas. Esto significa que, para
intervalos curvos, la aproximación es mucho más cercana a la forma real de la
función, lo que resulta en una mayor precisión.

Para aplicar la Regla de Simpson 1/3, necesitamos dividir el intervalo de
integración en un número *par* de subintervalos. Cada par de subintervalos
(es decir, tres puntos) se ajusta con una parábola.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 3: Integración Numérica - Regla de Simpson 1/3 ---")

# --- Parte 1: Definición de la Función y el Intervalo ---
# Usaremos la misma función de los ejercicios anteriores para comparar.
# Función: f(x) = x^2
# Integral analítica de x^2 entre a y b: (b^3 / 3) - (a^3 / 3)

def funcion_integracion_simpson(x):
    """
    Función de ejemplo: f(x) = x^2
    """
    return x**2

def integral_analitica_simpson(a, b):
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

# --- Parte 2: Implementación de la Regla de Simpson 1/3 ---
# La fórmula para la Regla de Simpson 1/3 para un par de subintervalos (tres puntos)
# es: (h/3) * [f(x_i) + 4*f(x_{i+1}) + f(x_{i+2})]
# Donde h es el ancho de cada subintervalo.
# La integral total es la suma de estas aproximaciones para todos los pares de subintervalos.

def regla_simpson_1_3(func, a, b, n_subintervalos):
    """
    Aproxima la integral de func de a a b usando la Regla de Simpson 1/3.

    Parámetros:
        func (function): La función a integrar.
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        n_subintervalos (int): Número de subintervalos a usar. DEBE SER UN NÚMERO PAR.

    Retorna:
        float: El valor aproximado de la integral.
        None: Si el número de subintervalos no es par o es <= 0.
    """

    if n_subintervalos <= 0 or n_subintervalos % 2 != 0:
        print("Error: El número de subintervalos para Simpson 1/3 debe ser un número par y mayor que cero.")
        return None

    h = (b - a) / n_subintervalos # Ancho de cada subintervalo
    integral = 0.0

    print(f"\n--- Parte 2: Ejecución de la Regla de Simpson 1/3 con {n_subintervalos} subintervalos ---")
    print(f"Ancho de cada subintervalo (h): {h:.4f}")

    # Sumamos los términos según la fórmula de Simpson
    # El primer y último término se multiplican por 1.
    # Los términos con índice impar se multiplican por 4.
    # Los términos con índice par (excepto el primero y el último) se multiplican por 2.

    # Primer término
    integral += func(a)

    for i in range(1, n_subintervalos):
        x_i = a + i * h
        if i % 2 == 1: # Si el índice es impar (1, 3, 5, ...)
            integral += 4 * func(x_i)
        else: # Si el índice es par (2, 4, 6, ...)
            integral += 2 * func(x_i)
    
    # Último término
    integral += func(b)

    integral *= (h / 3)

    return integral

# --- Parte 3: Aplicación y Comparación ---

print("\n--- Parte 3: Aplicación y Comparación ---")

num_subintervalos_simpson = 4 # Debe ser par. Probemos con 4.

integral_numerica_simpson = regla_simpson_1_3(funcion_integracion_simpson, a, b, num_subintervalos_simpson)
integral_exacta_simpson = integral_analitica_simpson(a, b)

if integral_numerica_simpson is not None:
    print(f"\nValor de la integral numérica (Regla de Simpson 1/3): {integral_numerica_simpson:.6f}")
    print(f"Valor de la integral exacta (analítica): {integral_exacta_simpson:.6f}")
    print(f"Error absoluto: {abs(integral_numerica_simpson - integral_exacta_simpson):.6e}")

    # Visualización de la aproximación con parábolas (conceptual)
    x_plot = np.linspace(a, b, 400) # Muchos puntos para dibujar la curva suave
    y_plot = funcion_integracion_simpson(x_plot)

    plt.figure(figsize=(10, 7))
    plt.plot(x_plot, y_plot, color='blue', label='f(x) = x^2')
    plt.fill_between(x_plot, y_plot, color='lightblue', alpha=0.3, label='Área Exacta')

    # Para visualizar la aproximación parabólica, necesitamos más puntos
    # y dibujar los segmentos de parábola. Esto es más complejo de graficar
    # directamente con líneas simples, pero podemos mostrar los puntos usados.
    x_simpson_points = np.linspace(a, b, num_subintervalos_simpson + 1)
    y_simpson_points = funcion_integracion_simpson(x_simpson_points)
    plt.scatter(x_simpson_points, y_simpson_points, color='red', zorder=5, label='Puntos de Evaluación')

    plt.title(f'Integración Numérica: Regla de Simpson 1/3 (n={num_subintervalos_simpson})')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

    print("\nObserva que para f(x)=x^2, Simpson 1/3 da un resultado exacto incluso con pocos subintervalos.")
    print("Esto se debe a que Simpson 1/3 es exacto para polinomios de grado hasta 3.")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La Regla de Simpson 1/3 es muy utilizada en el cálculo de volúmenes de")
print("sólidos de revolución o de cuerpos irregulares, donde se tienen secciones")
print("transversales a intervalos regulares. Por ejemplo, para estimar el volumen")
print("de un tanque de combustible con una forma compleja, o el volumen de un")
print("fuselaje de avión a partir de sus secciones transversales. También se usa")
print("en el análisis de datos experimentales para calcular la energía total")
print("disipada en un ciclo de histéresis, o la carga total aplicada en un ensayo")
print("de impacto a partir de la curva fuerza-tiempo.")

print("\n¡Has completado el tercer ejercicio del Capítulo 5!")
print("Ahora entiendes cómo la Regla de Simpson 1/3 nos permite obtener")
print("aproximaciones más precisas de integrales, especialmente para funciones curvas.")
