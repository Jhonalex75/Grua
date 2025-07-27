# -*- coding: utf-8 -*-
"""
Capítulo 2: Raíces de Ecuaciones
Ejercicio 1: Método de Bisección

En ingeniería, a menudo nos encontramos con ecuaciones complejas que no se
pueden resolver fácilmente de forma analítica (con lápiz y papel). Por ejemplo,
calcular el punto de equilibrio de un sistema, determinar la altura de un fluido
en un tanque con una geometría irregular, o encontrar la frecuencia natural de
vibración de una estructura.

Las "raíces" de una ecuación f(x) = 0 son los valores de 'x' donde la función
cruza el eje horizontal (donde f(x) es igual a cero).

El Método de Bisección es una técnica numérica para encontrar estas raíces.
Es como buscar algo en un libro: si sabes que la información está entre la
página 100 y la 200, abres por la mitad (página 150). Si no está ahí, pero sabes
que está en la primera mitad, repites el proceso en el rango 100-150, y así
sucesivamente, hasta que encuentras lo que buscas.
"""

import numpy as np # Importamos NumPy para operaciones numéricas, aunque no es crítico aquí.
import matplotlib.pyplot as plt # Importamos Matplotlib para visualizar la función.

print("--- Ejercicio 1: Método de Bisección ---")

# --- Parte 1: Definición de la Función ---
# Primero, necesitamos definir la función f(x) de la cual queremos encontrar la raíz.
# En Python, esto se hace con una función 'def'.

def funcion_ejemplo(x):
    """
    Define la función f(x) = x^3 - 2x - 5.
    Queremos encontrar el valor de x para el cual f(x) = 0.
    """
    return x**3 - 2*x - 5

# --- Parte 2: Visualización de la Función (Opcional pero Recomendado) ---
# Graficar la función nos ayuda a tener una idea de dónde podría estar la raíz.
# Buscamos los puntos donde la gráfica cruza el eje X.

print("\n--- Parte 2: Visualización de la Función ---")

x_valores = np.linspace(-3, 3, 400) # Genera 400 puntos entre -3 y 3
y_valores = funcion_ejemplo(x_valores) # Calcula f(x) para cada punto

plt.figure(figsize=(8, 6))
plt.plot(x_valores, y_valores, label='f(x) = x^3 - 2x - 5', color='blue')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--', label='Eje X (f(x)=0)')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--', label='Eje Y')
plt.title('Gráfico de la Función para Encontrar la Raíz')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()

print("Observando el gráfico, la raíz parece estar cerca de x = 2.")

# --- Parte 3: Implementación del Método de Bisección ---
# El método de bisección requiere un intervalo [a, b] donde f(a) y f(b) tienen
# signos opuestos. Esto garantiza que hay al menos una raíz dentro de ese intervalo.

def metodo_biseccion(func, a, b, tolerancia, max_iteraciones):
    """
    Implementa el Método de Bisección para encontrar la raíz de una función.

    Parámetros:
        func (function): La función f(x) de la cual se busca la raíz.
        a (float): Límite inferior del intervalo inicial.
        b (float): Límite superior del intervalo inicial.
        tolerancia (float): Criterio de parada: cuando el ancho del intervalo
                            sea menor que este valor, se considera que hemos
                            encontrado la raíz con suficiente precisión.
        max_iteraciones (int): Número máximo de iteraciones para evitar bucles
                               infinitos si la convergencia es lenta o no hay raíz.

    Retorna:
        float: La raíz aproximada de la función.
        None: Si no se encuentra una raíz dentro del número máximo de iteraciones
              o si los signos de f(a) y f(b) no son opuestos.
    """

    # Verificamos que los signos de f(a) y f(b) sean opuestos.
    # Si no lo son, el método no puede garantizar una raíz en el intervalo.
    if func(a) * func(b) >= 0:
        print("\nError: f(a) y f(b) deben tener signos opuestos para el Método de Bisección.")
        print(f"f({a}) = {func(a):.4f}, f({b}) = {func(b):.4f}")
        return None

    print("\n--- Parte 3: Ejecución del Método de Bisección ---")
    print(f"Intervalo inicial: [{a}, {b}]")
    print(f"Tolerancia deseada: {tolerancia}")

    # Bucle principal del método de bisección
    for i in range(max_iteraciones):
        # Calculamos el punto medio del intervalo
        c = (a + b) / 2

        # Evaluamos la función en el punto medio
        f_c = func(c)

        print(f"Iteración {i+1}: a={a:.4f}, b={b:.4f}, c={c:.4f}, f(c)={f_c:.4f}")

        # Verificamos si hemos encontrado la raíz con suficiente precisión
        # Si el valor de la función en 'c' es muy cercano a cero, o el intervalo es muy pequeño.
        if abs(f_c) < tolerancia or (b - a) / 2 < tolerancia:
            print(f"\nConvergencia alcanzada en {i+1} iteraciones.")
            return c

        # Decidimos en qué mitad del intervalo está la raíz
        if func(a) * f_c < 0: # Si f(a) y f(c) tienen signos opuestos, la raíz está en [a, c]
            b = c
        else: # Si f(b) y f(c) tienen signos opuestos, la raíz está en [c, b]
            a = c

    print("\nAdvertencia: Se alcanzó el número máximo de iteraciones sin cumplir la tolerancia.")
    return (a + b) / 2 # Devolvemos la mejor aproximación encontrada

# --- Parte 4: Aplicación del Método ---

# Definimos el intervalo inicial (observado del gráfico)
intervalo_a = 1.0
intervalo_b = 3.0

# Definimos la tolerancia y el número máximo de iteraciones
tol = 0.0001 # Queremos una precisión de 0.0001
max_iter = 100 # No más de 100 intentos

# Llamamos a nuestra función del método de bisección
raiz_encontrada = metodo_biseccion(funcion_ejemplo, intervalo_a, intervalo_b, tol, max_iter)

if raiz_encontrada is not None:
    print(f"\nLa raíz aproximada de la función es: {raiz_encontrada:.6f}")
    print(f"Verificación: f({raiz_encontrada:.6f}) = {funcion_ejemplo(raiz_encontrada):.6e}")
    # El ':.6e' muestra el número en notación científica con 6 decimales, útil para números muy pequeños.

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
# Imagina que tienes la ecuación para el factor de fricción de Darcy-Weisbach
# para flujo turbulento en tuberías (ecuación de Colebrook-White, implícita):
# 1/sqrt(f) = -2.0 * log10( (epsilon/D)/3.7 + 2.51/(Re*sqrt(f)) )
# Donde f es el factor de fricción, epsilon es la rugosidad, D el diámetro, Re el número de Reynolds.
# Esta ecuación no se puede despejar para 'f' directamente. Se define una función
# g(f) = 1/sqrt(f) + 2.0 * log10( (epsilon/D)/3.7 + 2.51/(Re*sqrt(f)) ) = 0
# Y se usa un método como bisección para encontrar la 'f' que hace g(f)=0.

print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("El método de bisección es útil para resolver ecuaciones implícitas, como la")
print("ecuación de Colebrook-White para el factor de fricción en tuberías, donde")
print("la variable que buscamos (el factor de fricción) no se puede despejar directamente.")
print("Se define una nueva función donde la ecuación es igual a cero, y se busca su raíz.")

print("\n¡Has completado el primer ejercicio del Capítulo 2!")
print("Ahora entiendes cómo el Método de Bisección puede encontrar soluciones a ecuaciones complejas.")

# --- Parte 5: Implementación Reutilizable del Método de Bisección (desde bisection_method_logic.py) ---
# Esta es una versión más limpia y reutilizable del método de bisección,
# ideal para ser importada y usada en otros scripts o aplicaciones (como una GUI).
# No imprime cada iteración, solo devuelve el resultado.

def funcion_ejemplo_adicional(x):
    """
    Esta es una función de ejemplo adicional para la cual queremos encontrar la raíz.
    La ecuación es: f(x) = x^3 - x - 2
    Esta función tiene una raíz entre x=1 y x=2.
    """
    return x**3 - x - 2

def metodo_biseccion_reutilizable(func, a, b, tolerancia=1e-7, max_iterations=100):
    """
    Implements the bisection method to find a root of a function.

    Args:
        func (function): The function for which to find a root. It must take one float argument.
        a (float): The start of the interval.
        b (float): The end of the interval.
        tolerance (float, optional): The desired precision of the root.
                                     The algorithm stops when the interval size |b-a| is smaller than this.
                                     Defaults to 1e-7.
        max_iterations (int, optional): The maximum number of iterations to prevent infinite loops.
                                        Defaults to 100.

    Raises:
        ValueError: If the initial interval [a, b] does not bracket a root
                    (i.e., f(a) and f(b) have the same sign).

    Returns:
        float: The approximate value of the root.
        None: If the method fails to converge within max_iterations.
    """
    fa = func(a)
    fb = func(b)
    if fa * fb >= 0:
        raise ValueError("The function must have opposite signs at the interval endpoints a and b.")

    for i in range(max_iterations):
        c = (a + b) / 2.0
        fc = func(c)

        if (b - a) / 2.0 < tolerance:
            # print(f"Converged after {i+1} iterations.") # Comentado para ser reutilizable
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    # print(f"Failed to converge within {max_iterations} iterations.") # Comentado para ser reutilizable
    return None

# --- Parte 6: Aplicación de la Versión Reutilizable del Método de Bisección ---

print("\n--- Parte 6: Aplicación de la Versión Reutilizable del Método de Bisección ---")

intervalo_a_reutilizable = 1.0
intervalo_b_reutilizable = 2.0 # Para la funcion_ejemplo_adicional
tolerancia_reutilizable = 1e-6
max_iter_reutilizable = 100

print(f"Función: f(x) = x^3 - x - 2")
print(f"Buscando una raíz en el intervalo [{intervalo_a_reutilizable}, {intervalo_b_reutilizable}]...")

try:
    raiz_reutilizable = metodo_biseccion_reutilizable(
        funcion_ejemplo_adicional,
        intervalo_a_reutilizable,
        intervalo_b_reutilizable,
        tolerancia=tolerancia_reutilizable,
        max_iterations=max_iter_reutilizable
    )

    if raiz_reutilizable is not None:
        print(f"\nRaíz aproximada encontrada (reutilizable): {raiz_reutilizable:.7f}")
        print(f"Verificación: f({raiz_reutilizable:.7f}) = {funcion_ejemplo_adicional(raiz_reutilizable):.7f}")
    else:
        print("\nNo se pudo encontrar una raíz con la versión reutilizable del método.")

except ValueError as e:
    print(f"\nError en la versión reutilizable: {e}")

print("\n¡Has complementado el ejercicio de Bisección con una versión más modular!")