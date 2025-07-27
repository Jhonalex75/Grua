# -*- coding: utf-8 -*-
"""
Capítulo 4: Ajuste de Curvas e Interpolación
Ejercicio 3: Interpolación Polinomial de Lagrange

La Interpolación Lineal es sencilla, pero a veces necesitamos una curva más
suave o una estimación más precisa que pase por todos nuestros puntos de datos
conocidos. Aquí es donde entra la Interpolación Polinomial.

La Interpolación Polinomial de Lagrange es un método para construir un único
polinomio que pasa *exactamente* por cada uno de los puntos de datos que tenemos.
Si tenemos 'n' puntos de datos, el polinomio resultante tendrá un grado máximo de 'n-1'.

Imagina que tienes varios puntos en un plano y quieres dibujar una curva suave
que pase por todos ellos sin "dobleces" bruscos entre los puntos. El polinomio
de Lagrange nos da la ecuación de esa curva.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 3: Interpolación Polinomial de Lagrange ---")

# --- Parte 1: Datos de Ejemplo ---
# Usaremos un conjunto de datos que no es perfectamente lineal para ver cómo
# un polinomio se ajusta mejor.
# Por ejemplo, la relación entre la velocidad de un ventilador y el caudal de aire.

print("\n--- Parte 1: Datos de Ejemplo ---")

velocidad_ventilador = np.array([0, 10, 20, 30, 40, 50]) # Unidades: % de velocidad máxima
caudal_aire = np.array([0, 15, 60, 135, 240, 375]) # Unidades: m^3/min

print("Velocidad Ventilador (x):", velocidad_ventilador)
print("Caudal de Aire (y):", caudal_aire)

# Visualizamos los datos.
plt.figure(figsize=(8, 6))
plt.scatter(velocidad_ventilador, caudal_aire, color='blue', label='Datos Conocidos')
plt.title('Caudal de Aire vs. Velocidad del Ventilador')
plt.xlabel('Velocidad del Ventilador (%)')
plt.ylabel('Caudal de Aire (m^3/min)')
plt.grid(True)
plt.legend()
plt.show()

print("Los puntos no parecen seguir una línea recta, sino una curva.")

# --- Parte 2: Implementación del Polinomio de Lagrange ---
# El polinomio de Lagrange se construye como una suma de términos, donde cada
# término es un producto de factores. Cada factor es un cociente de (x - x_j) / (x_k - x_j).
# La fórmula general es:
# P(x) = sumatoria de (y_k * L_k(x))
# Donde L_k(x) es el "polinomio base de Lagrange" para el punto k, definido como:
# L_k(x) = producto de (x - x_j) / (x_k - x_j) para todo j != k

def interpolacion_lagrange(x_conocidos, y_conocidos, x_a_interpolar):
    """
    Realiza interpolación polinomial de Lagrange para estimar un valor y en un punto x_a_interpolar.

    Parámetros:
        x_conocidos (numpy.array): Array de los valores x conocidos.
        y_conocidos (numpy.array): Array de los valores y conocidos correspondientes a x_conocidos.
        x_a_interpolar (float): El valor de x para el cual queremos estimar y.

    Retorna:
        float: El valor y interpolado.
    """

    n = len(x_conocidos) # Número de puntos de datos
    y_interpolado = 0.0

    print(f"\n--- Parte 2: Calculando Interpolación de Lagrange para x = {x_a_interpolar} ---")

    for k in range(n): # Iteramos sobre cada punto de dato conocido (x_k, y_k)
        # Calculamos el polinomio base de Lagrange L_k(x)
        L_k_x = 1.0
        for j in range(n): # Iteramos sobre todos los otros puntos (x_j)
            if k != j:
                # Multiplicamos los factores (x - x_j) / (x_k - x_j)
                # Aseguramos que el denominador no sea cero (puntos x_k deben ser distintos)
                if (x_conocidos[k] - x_conocidos[j]) == 0:
                    print("Error: Los valores de x conocidos deben ser distintos para la interpolación de Lagrange.")
                    return None
                L_k_x *= (x_a_interpolar - x_conocidos[j]) / (x_conocidos[k] - x_conocidos[j])
        
        # Sumamos el término y_k * L_k(x) al polinomio total
        y_interpolado += y_conocidos[k] * L_k_x
        print(f"  Término {k+1}: y_{k_val}={y_conocidos[k]:.2f}, L_{k}({x_a_interpolar})={L_k_x:.4f}, Contribución={y_conocidos[k] * L_k_x:.4f}")

    return y_interpolado

# --- Parte 3: Aplicación y Visualización del Polinomio ---

print("\n--- Parte 3: Aplicación y Visualización ---")

x_estimar = 25 # Queremos estimar el caudal a 25% de velocidad

caudal_estimado = interpolacion_lagrange(velocidad_ventilador, caudal_aire, x_estimar)

if caudal_estimado is not None:
    print(f"\nEl caudal de aire estimado a {x_estimar}% de velocidad es: {caudal_estimado:.2f} m^3/min")

    # Para visualizar el polinomio, generamos muchos puntos en el rango de los datos.
    x_rango = np.linspace(np.min(velocidad_ventilador), np.max(velocidad_ventilador), 200)
    y_polinomio = np.array([interpolacion_lagrange(velocidad_ventilador, caudal_aire, x_val) for x_val in x_rango])

    plt.figure(figsize=(8, 6))
    plt.scatter(velocidad_ventilador, caudal_aire, color='blue', label='Datos Conocidos', zorder=5)
    plt.plot(x_rango, y_polinomio, color='red', linestyle='-', label='Polinomio de Lagrange')
    plt.scatter(x_estimar, caudal_estimado, color='green', marker='X', s=100, zorder=6, label=f'Punto Interpolado ({x_estimar}%, {caudal_estimado:.2f})')
    
    plt.title('Interpolación Polinomial de Lagrange')
    plt.xlabel('Velocidad del Ventilador (%)')
    plt.ylabel('Caudal de Aire (m^3/min)')
    plt.grid(True)
    plt.legend()
    plt.show()

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La interpolación polinomial de Lagrange es útil cuando se necesita una")
print("función continua y suave que pase exactamente por un conjunto de puntos")
print("de datos. Por ejemplo, para generar trayectorias para robots o máquinas")
print("CNC a partir de puntos de control discretos, o para modelar curvas de")
print("diseño de superficies aerodinámicas o de cascos de barcos a partir de")
print("puntos de diseño clave. También se usa en la aproximación de funciones")
print("complejas a partir de un número limitado de evaluaciones.")

print("\n¡Has completado el tercer ejercicio del Capítulo 4!")
print("Ahora entiendes cómo la Interpolación Polinomial de Lagrange nos permite")
print("crear una curva suave que pasa por todos los puntos de datos.")
