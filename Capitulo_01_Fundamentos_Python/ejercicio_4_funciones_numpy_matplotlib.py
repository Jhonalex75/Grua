# -*- coding: utf-8 -*-
"""
Capítulo 1: Fundamentos de Python para Métodos Numéricos
Ejercicio 4: Funciones, Introducción a NumPy y Matplotlib

Este ejercicio cubre tres conceptos esenciales para la programación en ingeniería:
1.  **Funciones:** Cómo agrupar código para reutilizarlo y organizar mejor nuestros programas.
2.  **NumPy:** La biblioteca fundamental para trabajar con números de forma eficiente,
especialmente con arreglos (vectores y matrices), que son la base de muchos
métodos numéricos.
3.  **Matplotlib:** La biblioteca estándar para crear gráficos y visualizar nuestros
datos y resultados, algo crucial para entender el comportamiento de sistemas.
"""

print("--- Ejercicio 4: Funciones, NumPy y Matplotlib ---")

# --- Parte 1: Funciones - Organizando y Reutilizando Código ---
# Una función es como una "mini-programa" o una "receta" que realiza una tarea
# específica. Le damos unos "ingredientes" (parámetros de entrada), y nos devuelve
# un "resultado" (valor de retorno).

print("\n--- Parte 1: Funciones ---")

# Ejemplo 1.1: Función simple para calcular el área de un círculo
# 'def' se usa para definir una función. 'radio' es el parámetro de entrada.
# 'return' es lo que la función devuelve como resultado.
import math # Necesitamos math para usar math.pi

def calcular_area_circulo(radio):
    """
    Calcula el área de un círculo dado su radio.
    Parámetros:
        radio (float): El radio del círculo.
    Retorna:
        float: El área calculada.
    """
    area = math.pi * (radio ** 2)
    return area

# Usamos la función llamándola por su nombre y pasándole el valor del radio.
radio1 = 5.0
area1 = calcular_area_circulo(radio1)
print(f"El área de un círculo con radio {radio1} es: {area1:.2f} m^2")

radio2 = 10.0
area2 = calcular_area_circulo(radio2)
print(f"El área de un círculo con radio {radio2} es: {area2:.2f} m^2")

# Ejemplo 1.2: Función para convertir de Celsius a Fahrenheit
def celsius_a_fahrenheit(temp_celsius):
    """
    Convierte una temperatura de grados Celsius a Fahrenheit.
    Parámetros:
        temp_celsius (float): Temperatura en grados Celsius.
    Retorna:
        float: Temperatura en grados Fahrenheit.
    """
    temp_fahrenheit = (temp_celsius * 9/5) + 32
    return temp_fahrenheit

temperatura_c = 25.0
temperatura_f = celsius_a_fahrenheit(temperatura_c)
print(f"\n{temperatura_c}°C son {temperatura_f:.2f}°F")

print("\n")

# --- Parte 2: Introducción a NumPy - Trabajar con Arreglos (Arrays) ---
# NumPy (Numerical Python) es la biblioteca más importante para cálculos numéricos.
# Su principal característica son los 'arrays' (arreglos), que son como vectores
# o matrices, pero mucho más eficientes que las listas de Python para operaciones
# matemáticas.

print("--- Parte 2: Introducción a NumPy ---")

import numpy as np # Es una convención importar NumPy como 'np'

# Ejemplo 2.1: Creando un array de NumPy
# Un array es una colección de elementos del mismo tipo.

# Array de una dimensión (vector)
vector_fuerzas = np.array([100, 150, 200, 120]) # unidades: Newtons
print(f"\nVector de fuerzas: {vector_fuerzas}")
print(f"Tipo de dato del array: {vector_fuerzas.dtype}") # Muestra el tipo de los elementos
print(f"Dimensiones del array: {vector_fuerzas.shape}") # Muestra la forma (4,) significa 4 elementos

# Array de dos dimensiones (matriz)
matriz_rigidez = np.array([
    [1000, -500],
    [-500, 2000]
]) # unidades: N/m
print(f"\nMatriz de rigidez:\n{matriz_rigidez}")
print(f"Dimensiones de la matriz: {matriz_rigidez.shape}") # (2, 2) significa 2 filas, 2 columnas

# Ejemplo 2.2: Operaciones con arrays de NumPy
# Las operaciones se aplican elemento a elemento, lo cual es muy potente.

# Sumar un escalar a todos los elementos
velocidades = np.array([10, 12, 15, 8]) # m/s
aumento_velocidad = 2 # m/s
nuevas_velocidades = velocidades + aumento_velocidad
print(f"\nVelocidades originales: {velocidades}")
print(f"Nuevas velocidades (sumando {aumento_velocidad}): {nuevas_velocidades}")

# Multiplicar dos arrays elemento a elemento
areas_seccion = np.array([0.1, 0.2, 0.15, 0.05]) # m^2
presiones = np.array([100, 120, 90, 150]) # kPa
# Fuerza = Presión * Área
fuerzas_calculadas = areas_seccion * presiones
print(f"\nÁreas de sección: {areas_seccion}")
print(f"Presiones: {presiones}")
print(f"Fuerzas calculadas (elemento a elemento): {fuerzas_calculadas}")

# Producto punto (multiplicación de matrices/vectores) - muy común en álgebra lineal
# Si tenemos un vector de desplazamientos y una matriz de rigidez, podemos calcular fuerzas.
desplazamientos = np.array([0.01, 0.02]) # metros
fuerzas_resultantes = np.dot(matriz_rigidez, desplazamientos)
print(f"\nDesplazamientos: {desplazamientos}")
print(f"Fuerzas resultantes (producto punto): {fuerzas_resultantes}")

print("\n")

# --- Parte 3: Visualización Básica con Matplotlib ---
# Matplotlib es la biblioteca más popular para crear gráficos en Python.
# Es fundamental para visualizar datos, resultados de simulaciones y entender
# el comportamiento de los sistemas.

print("--- Parte 3: Visualización Básica con Matplotlib ---")

import matplotlib.pyplot as plt # Es una convención importar pyplot como 'plt'

# Ejemplo 3.1: Gráfico simple de una función (ej. temperatura vs. tiempo)

tiempo = np.array([0, 1, 2, 3, 4, 5]) # segundos
temperatura = np.array([20, 22, 25, 23, 21, 19]) # grados Celsius

plt.figure(figsize=(8, 5)) # Crea una figura para el gráfico (tamaño en pulgadas)
plt.plot(tiempo, temperatura, marker='o', linestyle='-', color='blue')
# plt.plot(x, y, ...) dibuja la línea.
# marker='o' pone círculos en cada punto.
# linestyle='-' dibuja una línea continua.
# color='blue' establece el color de la línea.

plt.title('Variación de Temperatura con el Tiempo') # Título del gráfico
plt.xlabel('Tiempo (s)') # Etiqueta del eje X
plt.ylabel('Temperatura (°C)') # Etiqueta del eje Y
plt.grid(True) # Muestra una cuadrícula en el gráfico
plt.show() # Muestra el gráfico (¡importante para que aparezca!)

# Ejemplo 3.2: Gráfico de una función matemática (ej. seno)

x = np.linspace(0, 2 * np.pi, 100) # Crea 100 puntos igualmente espaciados entre 0 y 2*Pi
y = np.sin(x) # Calcula el seno de cada punto en x

plt.figure(figsize=(8, 5))
plt.plot(x, y, color='red', linestyle='--')
plt.title('Función Seno')
plt.xlabel('Ángulo (radianes)')
plt.ylabel('Seno(x)')
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5) # Línea horizontal en y=0
plt.axvline(0, color='black', linewidth=0.5) # Línea vertical en x=0
plt.show()

print("\n¡Felicidades! Has completado el Capítulo 1 de Fundamentos de Python.")
print("Ahora tienes las herramientas básicas para organizar tu código, manejar datos")
print("numéricos de forma eficiente y visualizar tus resultados. ¡Estás listo para")
print("sumergirte en los métodos numéricos!")
