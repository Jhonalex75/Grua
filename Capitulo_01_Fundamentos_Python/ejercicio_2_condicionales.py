# -*- coding: utf-8 -*-
"""
Capítulo 1: Fundamentos de Python para Métodos Numéricos
Ejercicio 2: Estructuras de Control de Flujo - Condicionales (if, elif, else)

En ingeniería, a menudo necesitamos que nuestros sistemas o cálculos tomen
decisiones. Por ejemplo, si la presión es muy alta, activar una válvula;
si la temperatura es baja, encender un calentador. En programación, esto
se logra con las sentencias condicionales.

Imagina que las sentencias condicionales son como un "flujograma" o un
"diagrama de decisión" que le dice a Python qué camino seguir.
"""

print("--- Ejercicio 2: Sentencias Condicionales ---")

# --- Parte 1: La sentencia 'if' (Si...) ---
# La sentencia 'if' ejecuta un bloque de código SOLO SI una condición es Verdadera.
# La condición es una expresión que resulta en True o False (Booleano).

print("\n--- Parte 1: Sentencia 'if' ---")

temperatura_actual = 25 # grados Celsius
temperatura_limite = 30 # grados Celsius

print(f"Temperatura actual: {temperatura_actual}°C")
print(f"Temperatura límite: {temperatura_limite}°C")

# Si la temperatura actual es mayor que la límite, se ejecuta el código indentado.
# La indentación (espacios al inicio de la línea) es MUY importante en Python.
if temperatura_actual > temperatura_limite:
    print("¡Advertencia! La temperatura está por encima del límite.")
    print("Se recomienda revisar el sistema de enfriamiento.")

print("El programa continúa después del 'if'.")

# Ejemplo con una condición que es Verdadera
temperatura_actual = 35 # grados Celsius
print(f"\nTemperatura actual: {temperatura_actual}°C (cambiada para este ejemplo)")
if temperatura_actual > temperatura_limite:
    print("¡Alerta! Temperatura crítica alcanzada. Apagando sistema.")
    # Aquí podríamos llamar a una función para apagar el sistema, por ejemplo.

print("\n")

# --- Parte 2: La sentencia 'if-else' (Si... Sino...) ---
# 'if-else' nos permite ejecutar un bloque de código si la condición es Verdadera,
# y otro bloque de código diferente si la condición es Falsa.

print("--- Parte 2: Sentencia 'if-else' ---")

presion_actual = 80 # psi
presion_minima = 70 # psi

print(f"Presión actual: {presion_actual} psi")
print(f"Presión mínima requerida: {presion_minima} psi")

if presion_actual >= presion_minima:
    print("La presión es adecuada. Operación normal.")
else:
    print("¡Advertencia! La presión está por debajo del mínimo.")
    print("Verificar bomba o fugas.")

# Otro ejemplo de if-else
velocidad_motor = 1500 # RPM
velocidad_optima = 1200 # RPM

print(f"\nVelocidad del motor: {velocidad_motor} RPM")
print(f"Velocidad óptima: {velocidad_optima} RPM")

if velocidad_motor == velocidad_optima:
    print("El motor está operando a la velocidad óptima.")
else:
    print("El motor no está a la velocidad óptima. Ajustar.")

print("\n")

# --- Parte 3: La sentencia 'if-elif-else' (Si... Sino Si... Sino...) ---
# 'elif' (abreviatura de "else if") nos permite verificar múltiples condiciones
# en secuencia. Python evalúa las condiciones de arriba hacia abajo y ejecuta
# el primer bloque cuyo 'if' o 'elif' sea Verdadero. Si ninguna es Verdadera,
# se ejecuta el 'else' (si existe).

print("--- Parte 3: Sentencia 'if-elif-else' ---")

nivel_combustible = 65 # Porcentaje

print(f"Nivel de combustible: {nivel_combustible}%")

if nivel_combustible > 75:
    print("Nivel de combustible: Alto. Todo bien.")
elif nivel_combustible > 50: # Se evalúa solo si la primera condición fue Falsa
    print("Nivel de combustible: Medio. Monitorear.")
elif nivel_combustible > 25: # Se evalúa solo si las dos primeras fueron Falsas
    print("Nivel de combustible: Bajo. Considerar reabastecer.")
else: # Se ejecuta si ninguna de las condiciones anteriores fue Verdadera
    print("¡Alerta! Nivel de combustible crítico. Reabastecer inmediatamente.")

# Otro ejemplo con clasificación de materiales por dureza (escala de Mohs)
dureza_material = 7.5 # Escala de Mohs

print(f"\nDureza del material (escala de Mohs): {dureza_material}")

if dureza_material >= 9:
    print("Material muy duro (ej. Corindón, Diamante).")
elif dureza_material >= 7:
    print("Material duro (ej. Cuarzo, Topacio).")
elif dureza_material >= 5:
    print("Material de dureza media (ej. Apatito, Ortosa).")
else:
    print("Material blando (ej. Talco, Yeso).")

print("\n¡Excelente! Ahora sabes cómo hacer que tus programas tomen decisiones.")
print("Esto es un paso gigante para crear lógica de control en tus simulaciones y análisis.")
