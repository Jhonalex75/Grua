# -*- coding: utf-8 -*-
"""
Capítulo 4: Ajuste de Curvas e Interpolación
Ejercicio 2: Interpolación Lineal

En ingeniería, a menudo tenemos datos en puntos discretos, pero necesitamos
estimar un valor en un punto intermedio donde no tenemos una medición directa.
Por ejemplo, si tenemos la temperatura de un motor cada 10 minutos, pero
necesitamos saber la temperatura exacta a los 7 minutos.

La Interpolación es el proceso de estimar valores entre puntos de datos conocidos.
La Interpolación Lineal es la forma más sencilla de hacerlo: asumimos que los
puntos de datos adyacentes están conectados por una línea recta.

Imagina que tienes un mapa con la elevación de dos puntos cercanos y quieres
estimar la elevación de un punto que está justo entre ellos, asumiendo que el
terreno es una pendiente constante entre esos dos puntos. Eso es interpolación lineal.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 2: Interpolación Lineal ---")

# --- Parte 1: Datos de Ejemplo ---
# Vamos a usar un conjunto de datos simple para ilustrar la interpolación lineal.
# Por ejemplo, la relación entre el tiempo y la temperatura de un proceso.

print("\n--- Parte 1: Datos de Ejemplo ---")

tiempo = np.array([0, 5, 10, 15, 20]) # Unidades: minutos
temperatura = np.array([20, 25, 32, 30, 28]) # Unidades: grados Celsius

print("Tiempo (x):", tiempo)
print("Temperatura (y):", temperatura)

# Visualizamos los datos para ver la tendencia.
plt.figure(figsize=(8, 6))
plt.plot(tiempo, temperatura, marker='o', linestyle='-', color='blue', label='Datos Conocidos')
plt.title('Temperatura vs. Tiempo')
plt.xlabel('Tiempo (min)')
plt.ylabel('Temperatura (°C)')
plt.grid(True)
plt.legend()
plt.show()

print("Queremos estimar la temperatura en un tiempo intermedio, por ejemplo, a los 7 minutos.")

# --- Parte 2: Implementación de la Interpolación Lineal ---
# La fórmula para la interpolación lineal entre dos puntos (x0, y0) y (x1, y1) para un punto x es:
# y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)

def interpolacion_lineal(x_conocidos, y_conocidos, x_a_interpolar):
    """
    Realiza interpolación lineal para estimar un valor y en un punto x_a_interpolar.

    Parámetros:
        x_conocidos (numpy.array): Array de los valores x conocidos.
        y_conocidos (numpy.array): Array de los valores y conocidos correspondientes a x_conocidos.
        x_a_interpolar (float): El valor de x para el cual queremos estimar y.

    Retorna:
        float: El valor y interpolado.
        None: Si x_a_interpolar está fuera del rango de x_conocidos.
    """

    # Asegurarse de que x_a_interpolar esté dentro del rango de los datos conocidos.
    if not (np.min(x_conocidos) <= x_a_interpolar <= np.max(x_conocidos)):
        print(f"Error: El valor {x_a_interpolar} está fuera del rango de los datos conocidos.")
        return None

    # Encontrar el intervalo [x0, x1] que contiene x_a_interpolar.
    # np.searchsorted encuentra los índices donde se insertaría x_a_interpolar para mantener el orden.
    idx = np.searchsorted(x_conocidos, x_a_interpolar)

    # Si x_a_interpolar es exactamente uno de los puntos conocidos, devolver su valor.
    if x_a_interpolar == x_conocidos[idx-1]: # Si es el límite inferior del intervalo
        return y_conocidos[idx-1]
    if x_a_interpolar == x_conocidos[idx]: # Si es el límite superior del intervalo
        return y_conocidos[idx]

    # Los puntos (x0, y0) y (x1, y1) son los que rodean a x_a_interpolar.
    x0 = x_conocidos[idx-1]
    y0 = y_conocidos[idx-1]
    x1 = x_conocidos[idx]
    y1 = y_conocidos[idx]

    print(f"\nInterpolando entre ({x0}, {y0}) y ({x1}, {y1})")

    # Aplicar la fórmula de interpolación lineal
    y_interpolado = y0 + (y1 - y0) * (x_a_interpolar - x0) / (x1 - x0)

    return y_interpolado

# --- Parte 3: Aplicación y Visualización de la Interpolación ---

print("\n--- Parte 3: Aplicación y Visualización ---")

x_estimar = 7.0 # Queremos estimar la temperatura a los 7 minutos

temperatura_estimada = interpolacion_lineal(tiempo, temperatura, x_estimar)

if temperatura_estimada is not None:
    print(f"La temperatura estimada a los {x_estimar} minutos es: {temperatura_estimada:.2f}°C")

    # Volvemos a graficar los datos y añadimos el punto interpolado.
    plt.figure(figsize=(8, 6))
    plt.plot(tiempo, temperatura, marker='o', linestyle='-', color='blue', label='Datos Conocidos')
    plt.scatter(x_estimar, temperatura_estimada, color='red', marker='X', s=100, zorder=5, label=f'Punto Interpolado ({x_estimar} min, {temperatura_estimada:.2f}°C)')
    
    # Dibujar la línea de interpolación para el segmento relevante
    idx = np.searchsorted(tiempo, x_estimar)
    plt.plot([tiempo[idx-1], tiempo[idx]], [temperatura[idx-1], temperatura[idx]], color='green', linestyle='--', label='Segmento de Interpolación')

    plt.title('Interpolación Lineal de Temperatura')
    plt.xlabel('Tiempo (min)')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.legend()
    plt.show()

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La interpolación lineal es muy común en la lectura de tablas de propiedades")
print("termodinámicas (vapor, refrigerantes, etc.). Si la tabla no tiene el valor")
print("exacto que necesitamos para una presión o temperatura, usamos interpolación")
print("lineal entre los valores más cercanos. También se usa en el procesamiento")
print("de señales, donde se pueden rellenar huecos en datos de sensores, o en el")
print("diseño de levas, donde se necesita una trayectoria suave entre puntos discretos.")

print("\n¡Has completado el segundo ejercicio del Capítulo 4!")
print("Ahora entiendes cómo la Interpolación Lineal nos permite estimar valores")
print("entre puntos de datos conocidos.")
