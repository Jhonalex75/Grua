# -*- coding: utf-8 -*-
"""
Capítulo 2: Raíces de Ecuaciones
Ejercicio 4: Método de la Falsa Posición (Regula Falsi)

El Método de la Falsa Posición, también conocido como Regula Falsi, es una
combinación inteligente de los métodos de Bisección y Secante.

Al igual que el Método de Bisección, requiere un intervalo inicial [a, b]
donde la función f(x) cambia de signo (es decir, f(a) y f(b) tienen signos
opuestos). Esto garantiza que hay al menos una raíz dentro de ese intervalo.

Pero, en lugar de simplemente dividir el intervalo por la mitad (como Bisección),
el Método de la Falsa Posición traza una línea recta (una secante) entre los
puntos (a, f(a)) y (b, f(b)). La intersección de esta línea con el eje X
es la nueva estimación de la raíz. Luego, se ajusta el intervalo, manteniendo
siempre el cambio de signo.

Esto lo hace generalmente más rápido que Bisección, pero mantiene la robustez
de siempre converger a una raíz si el intervalo inicial es válido.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 4: Método de la Falsa Posición ---")

# --- Parte 1: Definición de la Función ---
# Usaremos la misma función de los ejercicios anteriores para comparar resultados.

def funcion_falsa_posicion(x):
    """
    Define la función f(x) = x^3 - 2x - 5.
    """
    return x**3 - 2*x - 5

# --- Parte 2: Visualización de la Función y la Secante (para entender el paso) ---
# Graficar nos ayuda a entender cómo la línea secante se usa para encontrar la nueva aproximación.

print("\n--- Parte 2: Visualización de la Función y la Secante ---")

x_valores = np.linspace(-3, 3, 400)
y_valores = funcion_falsa_posicion(x_valores)

plt.figure(figsize=(10, 7))
plt.plot(x_valores, y_valores, label='f(x) = x^3 - 2x - 5', color='blue')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--', label='Eje X (f(x)=0)')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--', label='Eje Y')

# Vamos a dibujar una secante entre dos puntos iniciales para ilustrar el método.
# Estos puntos deben tener signos opuestos en f(x).
a_plot = 1.0
b_plot = 3.0

f_a_plot = funcion_falsa_posicion(a_plot)
f_b_plot = funcion_falsa_posicion(b_plot)

# La fórmula para la intersección de la secante con el eje X es:
# x_interseccion = b - f(b) * (b - a) / (f(b) - f(a))

# Para dibujar la secante, necesitamos dos puntos: (a, f(a)) y (b, f(b))
plt.plot([a_plot, b_plot], [f_a_plot, f_b_plot], color='green', linestyle=':', label='Línea Secante')
plt.scatter([a_plot, b_plot], [f_a_plot, f_b_plot], color='red', zorder=5, label='Puntos del intervalo')

plt.title('Gráfico de la Función y una Línea Secante para Falsa Posición')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.ylim(-20, 20) # Ajustamos los límites del eje Y para mejor visualización
plt.show()

print("Observa cómo la línea verde (secante) cruza el eje X. Ese punto es la nueva estimación.")

# --- Parte 3: Implementación del Método de la Falsa Posición ---
# La fórmula para la nueva aproximación (c) es:
# c = b - f(b) * (b - a) / (f(b) - f(a))

def metodo_falsa_posicion(func, a, b, tolerancia, max_iteraciones):
    """
    Implementa el Método de la Falsa Posición para encontrar la raíz de una función.

    Parámetros:
        func (function): La función f(x).
        a (float): Límite inferior del intervalo inicial.
        b (float): Límite superior del intervalo inicial.
        tolerancia (float): Criterio de parada: cuando el valor absoluto de f(c)
                            sea menor que este valor, o el cambio en c sea muy pequeño.
        max_iteraciones (int): Número máximo de iteraciones.

    Retorna:
        float: La raíz aproximada de la función.
        None: Si no se encuentra una raíz o si los signos de f(a) y f(b) no son opuestos.
    """

    # Verificamos que los signos de f(a) y f(b) sean opuestos.
    if func(a) * func(b) >= 0:
        print("\nError: f(a) y f(b) deben tener signos opuestos para el Método de la Falsa Posición.")
        print(f"f({a}) = {func(a):.4f}, f({b}) = {func(b):.4f}")
        return None

    print("\n--- Parte 3: Ejecución del Método de la Falsa Posición ---")
    print(f"Intervalo inicial: [{a}, {b}]")
    print(f"Tolerancia deseada: {tolerancia}")

    c_anterior = a # Inicializamos con un valor para el criterio de parada

    for i in range(max_iteraciones):
        f_a = func(a)
        f_b = func(b)

        # Verificamos si el denominador es cero (f(b) - f(a)), lo que indicaría
        # que f(a) y f(b) son iguales, lo cual no debería pasar si los signos son opuestos
        # a menos que ambos sean cero (ya encontramos la raíz).
        if abs(f_b - f_a) < 1e-9: # Muy cercano a cero
            print("\nAdvertencia: f(b) - f(a) es muy cercano a cero. Posiblemente la raíz ya fue encontrada o hay un problema.")
            return b # O a, ya que f(a) y f(b) son casi iguales a cero.

        # Calculamos la nueva aproximación 'c' usando la fórmula de la falsa posición
        c = b - f_b * (b - a) / (f_b - f_a)
        f_c = func(c)

        print(f"Iteración {i+1}: a={a:.4f}, b={b:.4f}, c={c:.4f}, f(c)={f_c:.4f}")

        # Criterio de parada: si f(c) es muy cercano a cero
        if abs(f_c) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones (f(c) muy cercano a cero).")
            return c

        # Criterio de parada alternativo: si el cambio en c es muy pequeño
        if abs(c - c_anterior) < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones (cambio en c muy pequeño).")
            return c

        # Actualizamos el intervalo, manteniendo siempre el cambio de signo
        if f_a * f_c < 0: # Si f(a) y f(c) tienen signos opuestos, la raíz está en [a, c]
            b = c
        else: # Si f(b) y f(c) tienen signos opuestos, la raíz está en [c, b]
            a = c

        c_anterior = c # Guardamos c para la próxima comparación de cambio

    print("\nAdvertencia: Se alcanzó el número máximo de iteraciones sin cumplir la tolerancia.")
    return c # Devolvemos la mejor aproximación encontrada

# --- Parte 4: Aplicación del Método ---

# Definimos el intervalo inicial (observado del gráfico, donde f(a) y f(b) tienen signos opuestos)
intervalo_a = 1.0
intervalo_b = 3.0

# Definimos la tolerancia y el número máximo de iteraciones
tol = 0.0001
max_iter = 100

# Llamamos a nuestra función del método de la Falsa Posición
raiz_encontrada = metodo_falsa_posicion(funcion_falsa_posicion, intervalo_a, intervalo_b, tol, max_iter)

if raiz_encontrada is not None:
    print(f"\nLa raíz aproximada de la función es: {raiz_encontrada:.6f}")
    print(f"Verificación: f({raiz_encontrada:.6f}) = {funcion_falsa_posicion(raiz_encontrada):.6e}")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El Método de la Falsa Posición es muy útil en problemas donde se necesita")
print("garantizar la convergencia (como en Bisección) pero se desea una velocidad")
print("de convergencia mayor. Por ejemplo, en el diseño de sistemas de control, donde")
print("se busca el punto de operación óptimo de un componente, y la función que lo")
print("describe es compleja pero se puede acotar entre dos valores donde el comportamiento")
print("cambia de signo (ej. de estable a inestable, o de ganancia positiva a negativa).")
print("También en el cálculo de propiedades termodinámicas implícitas o en el análisis")
print("de esfuerzos en estructuras con comportamiento no lineal, donde se busca el punto")
print("donde el esfuerzo alcanza un valor crítico.")

print("\n¡Has completado el cuarto y último ejercicio del Capítulo 2!")
print("Ahora conoces el Método de la Falsa Posición, una técnica robusta y eficiente")
print("para encontrar raíces de ecuaciones.")
print("¡Felicidades por completar el Capítulo 2: Raíces de Ecuaciones!")
