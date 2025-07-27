# -*- coding: utf-8 -*-
"""
Capítulo 1: Fundamentos de Python para Métodos Numéricos
Ejercicio 1: Variables, Tipos de Datos y Operaciones Básicas

Este ejercicio está diseñado para ingenieros mecánicos que no tienen experiencia
previa en programación. Aquí aprenderemos los conceptos más fundamentales de
Python: cómo guardar información (variables), qué tipo de información podemos
guardar (tipos de datos) y cómo realizar cálculos simples (operaciones).

Imagina que Python es una calculadora muy potente y una libreta donde puedes
anotar y manipular números, textos y otras cosas.
"""

# --- Parte 1: Variables - Guardando Información ---
# Una variable es como una caja con una etiqueta donde guardamos un valor.
# La etiqueta (nombre de la variable) nos ayuda a recordar qué hay dentro de la caja.

print("--- Parte 1: Variables ---")

# Ejemplo 1.1: Guardando un número entero (sin decimales)
# Aquí, 'velocidad' es la etiqueta de nuestra caja, y dentro guardamos el número 100.
velocidad = 100 # unidades: km/h
print(f"La velocidad inicial es: {velocidad} km/h")

# Podemos cambiar el contenido de la caja en cualquier momento.
velocidad = 120 # La velocidad ha cambiado a 120 km/h
print(f"La nueva velocidad es: {velocidad} km/h")

# Ejemplo 1.2: Guardando un número con decimales (flotante)
# 'diametro_tuberia' es la variable, y 0.5 es el valor.
diametro_tuberia = 0.5 # unidades: metros
print(f"El diámetro de la tubería es: {diametro_tuberia} metros")

# Ejemplo 1.3: Guardando texto (cadena de caracteres o 'string')
# El texto siempre va entre comillas simples o dobles.
material = "Acero Inoxidable"
print(f"El material de la tubería es: {material}")

# Ejemplo 1.4: Guardando un valor lógico (Booleano)
# Solo puede ser Verdadero (True) o Falso (False). Útil para decisiones.
sistema_presurizado = True # ¿Está el sistema bajo presión? Sí (True)
print(f"¿El sistema está presurizado? {sistema_presurizado}")

print("\n") # Esto es para dejar una línea en blanco y mejorar la lectura.

# --- Parte 2: Tipos de Datos - ¿Qué tipo de información es? ---
# Python es "inteligente" y sabe qué tipo de información guardamos en cada variable.
# Podemos preguntarle a Python el tipo de dato usando la función 'type()'.

print("--- Parte 2: Tipos de Datos ---")

# 'int' (entero): Números sin decimales.
print(f"Tipo de 'velocidad': {type(velocidad)}")

# 'float' (flotante): Números con decimales.
print(f"Tipo de 'diametro_tuberia': {type(diametro_tuberia)}")

# 'str' (string): Cadenas de texto.
print(f"Tipo de 'material': {type(material)}")

# 'bool' (booleano): Valores lógicos True/False.
print(f"Tipo de 'sistema_presurizado': {type(sistema_presurizado)}")

print("\n")

# --- Parte 3: Operaciones Básicas - Haciendo Cálculos ---
# Podemos usar las variables en operaciones matemáticas, igual que en una calculadora.

print("--- Parte 3: Operaciones Básicas ---")

# Ejemplo 3.1: Suma (+)
temperatura_inicial = 20 # grados Celsius
aumento_temperatura = 5 # grados Celsius
temperatura_final = temperatura_inicial + aumento_temperatura
print(f"Temperatura final (suma): {temperatura_final} °C")

# Ejemplo 3.2: Resta (-)
presion_inicial = 100 # kPa
caida_presion = 15 # kPa
presion_final = presion_inicial - caida_presion
print(f"Presión final (resta): {presion_final} kPa")

# Ejemplo 3.3: Multiplicación (*)
fuerza = 50 # Newtons
distancia = 2 # metros
trabajo = fuerza * distancia # Trabajo = Fuerza x Distancia
print(f"Trabajo realizado (multiplicación): {trabajo} Joules")

# Ejemplo 3.4: División (/)
masa = 10 # kg
volumen = 0.005 # m^3
densidad = masa / volumen # Densidad = Masa / Volumen
print(f"Densidad del material (división): {densidad} kg/m^3")

# Ejemplo 3.5: Potencia (**) - Elevar un número a una potencia
lado_cuadrado = 4 # cm
area_cuadrado = lado_cuadrado ** 2 # Área = lado al cuadrado
print(f"Área del cuadrado (potencia): {area_cuadrado} cm^2")

# Ejemplo 3.6: División Entera (//) - Solo la parte entera del resultado
# Útil si solo nos interesa cuántas veces "cabe" un número en otro.
piezas_totales = 17
piezas_por_caja = 5
cajas_necesarias = piezas_totales // piezas_por_caja
print(f"Cajas completas necesarias (división entera): {cajas_necesarias}")

# Ejemplo 3.7: Módulo (%) - El "resto" de una división
# Útil para saber si un número es par/impar o para ciclos.
resto_piezas = piezas_totales % piezas_por_caja
print(f"Piezas restantes (módulo): {resto_piezas}")

# --- Parte 4: Combinando Operaciones y Variables ---
# Podemos hacer cálculos más complejos, siguiendo el orden de las operaciones (PEMDAS/PEMDSR).

print("\n--- Parte 4: Combinando Operaciones y Variables ---")

# Cálculo del área de un círculo: Pi * radio^2
import math # Importamos el módulo 'math' para usar el valor de Pi

radio = 3.0 # metros
area_circulo = math.pi * (radio ** 2)
print(f"El área de un círculo con radio {radio} m es: {area_circulo:.2f} m^2")
# El ':.2f' es para mostrar solo 2 decimales, útil para resultados de ingeniería.

# Cálculo de la energía cinética: 0.5 * masa * velocidad^2
masa_objeto = 5.0 # kg
velocidad_objeto = 10.0 # m/s
energia_cinetica = 0.5 * masa_objeto * (velocidad_objeto ** 2)
print(f"La energía cinética del objeto es: {energia_cinetica} Joules")

print("\n¡Felicidades! Has completado el primer ejercicio de Python.")
print("Has aprendido a guardar información, entender su tipo y realizar cálculos básicos.")
print("¡Sigue adelante!")
