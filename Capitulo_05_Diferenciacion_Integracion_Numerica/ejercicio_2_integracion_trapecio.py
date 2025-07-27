# -*- coding: utf-8 -*-
"""
Capítulo 5: Diferenciación e Integración Numérica
Ejercicio 2: Integración Numérica - Regla del Trapecio

En ingeniería, la integral de una función representa la acumulación de una
cantidad. Por ejemplo, la integral de la velocidad con respecto al tiempo es
el desplazamiento; la integral de la fuerza con respecto a la distancia es el
trabajo. A menudo, necesitamos calcular estas integrales, pero la función
puede ser muy compleja, o solo tenemos datos discretos (como mediciones
experimentales).

La Integración Numérica nos permite aproximar el valor de una integral definida
cuando no podemos resolverla analíticamente. La Regla del Trapecio es uno de
los métodos más sencillos y visualmente intuitivos.

Imagina que quieres calcular el área de un terreno irregular. En lugar de
intentar una fórmula compleja, puedes dividir el terreno en muchas pequeñas
franjas con forma de trapecio. Si sumas el área de todos esos trapecios,
obtendrás una buena aproximación del área total del terreno.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 2: Integración Numérica - Regla del Trapecio ---")

# --- Parte 1: Definición de la Función y el Intervalo ---
# Usaremos una función conocida para poder comparar la integral numérica con la analítica.
# Función: f(x) = x^2
# Integral analítica de x^2 entre a y b: (b^3 / 3) - (a^3 / 3)

def funcion_integracion(x):
    """
    Función de ejemplo: f(x) = x^2
    """
    return x**2

def integral_analitica(a, b):
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

# --- Parte 2: Implementación de la Regla del Trapecio ---
# La Regla del Trapecio aproxima el área bajo la curva dividiendo el intervalo
# en 'n' subintervalos y aproximando el área de cada subintervalo con un trapecio.
# El área de un trapecio es: (base1 + base2) * altura / 2
# En nuestro caso, las bases son los valores de la función f(x) en los extremos
# del subintervalo, y la altura es el ancho del subintervalo (h).
# Área_trapecio = (f(x_i) + f(x_{i+1})) * h / 2
# La integral total es la suma de las áreas de todos los trapecios.

def regla_trapecio(func, a, b, n_subintervalos):
    """
    Aproxima la integral de func de a a b usando la Regla del Trapecio.

    Parámetros:
        func (function): La función a integrar.
        a (float): Límite inferior de integración.
        b (float): Límite superior de integración.
        n_subintervalos (int): Número de subintervalos (trapecios) a usar.

    Retorna:
        float: El valor aproximado de la integral.
    """

    if n_subintervalos <= 0:
        print("Error: El número de subintervalos debe ser mayor que cero.")
        return None

    h = (b - a) / n_subintervalos # Ancho de cada subintervalo
    integral = 0.0

    print(f"\n--- Parte 2: Ejecución de la Regla del Trapecio con {n_subintervalos} subintervalos ---")
    print(f"Ancho de cada subintervalo (h): {h:.4f}")

    # Sumamos el área de cada trapecio
    for i in range(n_subintervalos):
        x_i = a + i * h       # Punto inicial del subintervalo
        x_i_mas_1 = a + (i + 1) * h # Punto final del subintervalo

        f_x_i = func(x_i)
        f_x_i_mas_1 = func(x_i_mas_1)

        area_trapecio = (f_x_i + f_x_i_mas_1) * h / 2
        integral += area_trapecio

        print(f"  Subintervalo [{x_i:.2f}, {x_i_mas_1:.2f}]: f({x_i:.2f})={f_x_i:.2f}, f({x_i_mas_1:.2f})={f_x_i_mas_1:.2f}, Área={area_trapecio:.4f}")

    return integral

# --- Parte 3: Aplicación y Comparación ---

print("\n--- Parte 3: Aplicación y Comparación ---")

num_subintervalos = 4 # Podemos probar con más para ver cómo mejora la precisión

integral_numerica = regla_trapecio(funcion_integracion, a, b, num_subintervalos)
integral_exacta = integral_analitica(a, b)

if integral_numerica is not None:
    print(f"\nValor de la integral numérica (Regla del Trapecio): {integral_numerica:.6f}")
    print(f"Valor de la integral exacta (analítica): {integral_exacta:.6f}")
    print(f"Error absoluto: {abs(integral_numerica - integral_exacta):.6e}")

    # Visualización de la aproximación con trapecios
    x_plot = np.linspace(a, b, 400) # Muchos puntos para dibujar la curva suave
    y_plot = funcion_integracion(x_plot)

    plt.figure(figsize=(10, 7))
    plt.plot(x_plot, y_plot, color='blue', label='f(x) = x^2')
    plt.fill_between(x_plot, y_plot, color='lightblue', alpha=0.3, label='Área Exacta')

    # Dibujar los trapecios
    x_trapecios = np.linspace(a, b, num_subintervalos + 1)
    y_trapecios = funcion_integracion(x_trapecios)
    for i in range(num_subintervalos):
        x_segmento = [x_trapecios[i], x_trapecios[i], x_trapecios[i+1], x_trapecios[i+1]]
        y_segmento = [0, y_trapecios[i], y_trapecios[i+1], 0]
        plt.fill(x_segmento, y_segmento, color='red', alpha=0.5, edgecolor='red')
        plt.plot([x_trapecios[i], x_trapecios[i+1]], [y_trapecios[i], y_trapecios[i+1]], color='red', linestyle='--')

    plt.title(f'Integración Numérica: Regla del Trapecio (n={num_subintervalos})')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

    print("\nObserva cómo al aumentar el número de subintervalos, la aproximación mejora.")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La integración numérica es fundamental para calcular el trabajo realizado")
print("por una fuerza variable (integral de F dx), o el impulso de una fuerza")
print("variable en el tiempo (integral de F dt). También se usa para determinar")
print("el centroide o el momento de inercia de áreas o volúmenes con formas")
print("irregulares, donde la integración analítica es difícil. En termodinámica,")
print("se puede usar para calcular el trabajo de expansión o compresión de un gas")
print("cuando la relación presión-volumen no es simple.")

print("\n¡Has completado el segundo ejercicio del Capítulo 5!")
print("Ahora entiendes cómo la Regla del Trapecio nos permite aproximar el área")
print("bajo una curva, una herramienta esencial en muchos cálculos de ingeniería.")
