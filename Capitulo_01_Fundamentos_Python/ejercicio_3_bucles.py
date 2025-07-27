# -*- coding: utf-8 -*-
"""
Capítulo 1: Fundamentos de Python para Métodos Numéricos
Ejercicio 3: Estructuras de Control de Flujo - Bucles (for y while)

En ingeniería, a menudo necesitamos repetir una tarea muchas veces. Por ejemplo,
calcular la deformación en cada punto de una viga, simular el comportamiento
de un fluido en diferentes instantes de tiempo, o realizar iteraciones hasta
que un cálculo converja a una solución.

Los bucles (o "loops") son la forma en que Python nos permite automatizar
estas tareas repetitivas, evitando que tengamos que escribir el mismo código
una y otra vez.
"""

print("--- Ejercicio 3: Bucles ---")

# --- Parte 1: Bucle 'for' - Repetir un número conocido de veces o sobre una colección ---
# El bucle 'for' es ideal cuando sabemos cuántas veces queremos repetir algo,
# o cuando queremos recorrer cada elemento de una lista, una cadena de texto, etc.

print("\n--- Parte 1: Bucle 'for' ---")

# Ejemplo 1.1: Repetir un número fijo de veces (usando range())
# La función 'range(n)' genera una secuencia de números desde 0 hasta n-1.
# Esto es útil para simular pasos de tiempo o iteraciones.
print("\nSimulación de 5 pasos de tiempo:")
for paso in range(5): # 'paso' tomará los valores 0, 1, 2, 3, 4
    print(f"Realizando cálculo para el paso de tiempo: {paso + 1}")
    # Aquí irían los cálculos de la simulación para cada paso.

# Ejemplo 1.2: Iterar sobre una lista de elementos
# Podemos tener una lista de materiales y procesar cada uno.
materiales = ["Acero", "Aluminio", "Cobre", "Titanio"]
print("\nProcesando propiedades de materiales:")
for mat in materiales:
    print(f"Analizando propiedades del material: {mat}")
    # Aquí podríamos, por ejemplo, buscar en una base de datos las propiedades de 'mat'.

# Ejemplo 1.3: Calcular la suma de una serie de números
# Imagina que tienes una serie de mediciones de temperatura y quieres el promedio.
temperaturas = [20.5, 21.0, 19.8, 22.1, 20.0]
suma_temperaturas = 0
print("\nCalculando suma de temperaturas:")
for temp in temperaturas:
    suma_temperaturas = suma_temperaturas + temp # Acumulamos la suma
    print(f"Temperatura actual: {temp}°C, Suma acumulada: {suma_temperaturas}°C")

print(f"Suma total de temperaturas: {suma_temperaturas}°C")
print(f"Temperatura promedio: {suma_temperaturas / len(temperaturas):.2f}°C")
# 'len(temperaturas)' nos da el número de elementos en la lista.

print("\n")

# --- Parte 2: Bucle 'while' - Repetir mientras una condición sea Verdadera ---
# El bucle 'while' es útil cuando no sabemos de antemano cuántas veces se repetirá
# el código. Se repite MIENTRAS una condición específica sea Verdadera.
# ¡Cuidado! Si la condición nunca se vuelve Falsa, el bucle se ejecutará infinitamente.

print("--- Parte 2: Bucle 'while' ---")

# Ejemplo 2.1: Iteración hasta alcanzar una tolerancia (común en métodos numéricos)
# Imagina que estamos refinando un cálculo hasta que el error sea muy pequeño.
error_actual = 10.0 # Un error inicial grande
tolerancia = 0.01 # Queremos que el error sea menor que esto
iteracion = 0

print("\nRefinando cálculo hasta alcanzar tolerancia:")
while error_actual > tolerancia:
    iteracion += 1 # Esto es lo mismo que iteracion = iteracion + 1
    print(f"Iteración {iteracion}: Error actual = {error_actual:.4f}")
    # Aquí irían los cálculos que reducen el error.
    # Para este ejemplo, simplemente reducimos el error a la mitad en cada paso.
    error_actual /= 2 # Esto es lo mismo que error_actual = error_actual / 2

print(f"Cálculo convergido en {iteracion} iteraciones. Error final: {error_actual:.4f}")

# Ejemplo 2.2: Simulación de descarga de un tanque
volumen_tanque = 100 # litros
flujo_salida = 10 # litros/minuto
tiempo = 0 # minutos

print("\nSimulando descarga de tanque:")
while volumen_tanque > 0:
    print(f"Tiempo: {tiempo} min, Volumen restante: {volumen_tanque} L")
    volumen_tanque -= flujo_salida # Restamos el flujo de salida
    tiempo += 1 # Avanzamos un minuto
    # Para evitar un bucle infinito si el volumen nunca llega a 0 exacto (por flotantes)
    if volumen_tanque < 0:
        volumen_tanque = 0 # Aseguramos que no sea negativo

print(f"Tanque vacío en {tiempo - 1} minutos.") # Restamos 1 porque el último incremento de tiempo fue cuando ya estaba vacío.

print("\n")

# --- Parte 3: Control de Bucles - 'break' y 'continue' ---
# 'break': Sale completamente del bucle.
# 'continue': Salta el resto del código en la iteración actual y pasa a la siguiente.

print("--- Parte 3: Control de Bucles ---")

# Ejemplo 3.1: Usando 'break' para detener una búsqueda
componentes = ["Resistor", "Capacitor", "Inductor", "Diodo", "Transistor"]
buscar_componente = "Diodo"

print(f"\nBuscando '{buscar_componente}' en la lista de componentes:")
for comp in componentes:
    print(f"Revisando: {comp}")
    if comp == buscar_componente:
        print(f"¡Encontrado! {buscar_componente} está en la lista.")
        break # Salimos del bucle una vez que lo encontramos

# Ejemplo 3.2: Usando 'continue' para saltar elementos
mediciones_presion = [10.2, 11.5, -99.0, 12.1, 10.8, -99.0, 11.0]
# Asumimos que -99.0 es una lectura errónea o un sensor defectuoso.

print("\nProcesando mediciones de presión (ignorando errores):")
for medicion in mediciones_presion:
    if medicion == -99.0:
        print("¡Dato erróneo detectado! Saltando esta medición.")
        continue # Ignoramos este valor y pasamos a la siguiente medición
    print(f"Procesando medición válida: {medicion} bar")
    # Aquí irían los cálculos con la medición válida.

print("\n¡Felicidades! Has dominado los bucles en Python.")
print("Esta habilidad es crucial para implementar algoritmos iterativos y procesar datos en ingeniería.")
print("¡Estás progresando muy bien!")
