# -*- coding: utf-8 -*-
"""
Capítulo 6: Ecuaciones Diferenciales Ordinarias (EDO)
Ejercicio 4: Problemas de Valor Inicial con SciPy (solve_ivp)

En los ejercicios anteriores, implementamos los métodos de Euler y Runge-Kutta
desde cero para entender su funcionamiento interno. Sin embargo, en la práctica
de la ingeniería, cuando necesitamos resolver EDOs de manera eficiente y robusta,
recurrimos a bibliotecas especializadas como SciPy.

La función `solve_ivp` (solve initial value problem) del módulo `scipy.integrate`
es la herramienta estándar en Python para resolver problemas de valor inicial
para sistemas de EDOs. Ofrece varios métodos numéricos (como RK45, BDF, LSODA)
y maneja automáticamente el tamaño del paso para asegurar la precisión y la
estabilidad, lo que la hace muy confiable.

Imagina que tienes un simulador de vuelo y quieres predecir la trayectoria de
un avión. No querrías escribir el código para cada cálculo de paso; en su lugar,
usarías una herramienta ya probada y optimizada que se encarga de los detalles
matemáticos complejos, permitiéndote concentrarte en el modelo físico del avión.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp # Importamos la función clave

print("--- Ejercicio 4: Problemas de Valor Inicial con SciPy (solve_ivp) ---")

# --- Parte 1: Definición del Sistema de EDOs y Condiciones Iniciales ---
# Usaremos el mismo sistema del ejercicio anterior para comparar:
# dy1/dx = y2
# dy2/dx = -y1
# Con condiciones iniciales: y1(0) = 0, y2(0) = 1
# La solución analítica es: y1(x) = sin(x), y2(x) = cos(x)

def sistema_edos_scipy(x, y_vector):
    """
    Define el sistema de EDOs para `solve_ivp`.
    `solve_ivp` espera que la función retorne un array con las derivadas.
    """
    y1 = y_vector[0]
    y2 = y_vector[1]

    dy1_dx = y2
    dy2_dx = -y1

    return np.array([dy1_dx, dy2_dx])

def solucion_analitica_scipy(x):
    """
    Solución analítica del sistema de EDOs.
    """
    y1_sol = np.sin(x)
    y2_sol = np.cos(x)
    # Retornar un array 2D donde cada fila es una variable dependiente
    return np.vstack([y1_sol, y2_sol])

# Condiciones iniciales
x0 = 0.0
y_inicial_vector = np.array([0.0, 1.0]) # [y1(0), y2(0)]

# Intervalo de integración [x_inicio, x_fin]
x_final_integracion = 4 * np.pi # Integrar por dos ciclos completos
intervalo_x = [x0, x_final_integracion]

print("\n--- Parte 1: Sistema de EDOs y Condiciones Iniciales ---")
print(f"Sistema de EDOs: dy1/dx = y2, dy2/dx = -y1")
print(f"Condiciones iniciales: y1({x0}) = {y_inicial_vector[0]}, y2({x0}) = {y_inicial_vector[1]}")
print(f"Intervalo de integración: [{intervalo_x[0]:.2f}, {intervalo_x[1]:.2f}]")

# --- Parte 2: Uso de `scipy.integrate.solve_ivp` ---
# `solve_ivp` es muy flexible. Los parámetros clave son:
# - `fun`: La función que define el sistema de EDOs (f(x, y_vector)).
# - `t_span`: El intervalo de integración [t_inicio, t_fin].
# - `y0`: El vector de condiciones iniciales.
# - `method`: El método numérico a usar (ej. 'RK45', 'LSODA', 'BDF'). 'RK45' es el predeterminado y suele ser una buena opción.
# - `t_eval`: Puntos específicos de x donde queremos la solución. Si no se da, `solve_ivp` elige sus propios puntos.

print("\n--- Parte 2: Ejecución con `scipy.integrate.solve_ivp` ---")

# Generamos puntos donde queremos evaluar la solución para graficarla suavemente
x_eval_points = np.linspace(x0, x_final_integracion, 200)

solucion_scipy = solve_ivp(sistema_edos_scipy, intervalo_x, y_inicial_vector, method='RK45', t_eval=x_eval_points)

# El objeto `solucion_scipy` contiene los resultados:
# - `solucion_scipy.t`: Los valores de x donde se calculó la solución.
# - `solucion_scipy.y`: Una matriz donde cada fila es una variable dependiente (y1, y2, etc.).

print("Estado de la solución (success):", solucion_scipy.success)
print("Mensaje de la solución:", solucion_scipy.message)

# Extraemos las soluciones
x_sol_scipy = solucion_scipy.t
y1_sol_scipy = solucion_scipy.y[0, :]
y2_sol_scipy = solucion_scipy.y[1, :]

# --- Parte 3: Visualización y Comparación ---

print("\n--- Parte 3: Visualización y Comparación ---")

# Calculamos la solución analítica para comparar
x_analitica = np.linspace(x0, x_final_integracion, 200) # Muchos puntos para una curva suave
y_analitica_matriz = solucion_analitica_scipy(x_analitica)
y1_sol_analitica = y_analitica_matriz[0, :]
y2_sol_analitica = y_analitica_matriz[1, :]

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1) # Gráfico 1 de 2
plt.plot(x_analitica, y1_sol_analitica, color='blue', linestyle='-', label='y1 Analítica')
plt.plot(x_sol_scipy, y1_sol_scipy, color='red', linestyle='--', label='y1 SciPy')
plt.title('Solución de y1(x)')
plt.xlabel('x')
plt.ylabel('y1')
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2) # Gráfico 2 de 2
plt.plot(x_analitica, y2_sol_analitica, color='blue', linestyle='-', label='y2 Analítica')
plt.plot(x_sol_scipy, y2_sol_scipy, color='red', linestyle='--', label='y2 SciPy')
plt.title('Solución de y2(x)')
plt.xlabel('x')
plt.ylabel('y2')
plt.grid(True)
plt.legend()

plt.tight_layout() # Ajusta el diseño para evitar superposiciones
plt.show()

# También podemos graficar la trayectoria en el espacio de fase (y1 vs y2)
plt.figure(figsize=(7, 7))
plt.plot(y1_sol_analitica, y2_sol_analitica, color='blue', linestyle='-', label='Trayectoria Analítica')
plt.plot(y1_sol_scipy, y2_sol_scipy, color='red', linestyle='--', label='Trayectoria SciPy')
plt.scatter(y_inicial_vector[0], y_inicial_vector[1], color='green', s=100, zorder=5, label='Punto Inicial')
plt.title('Espacio de Fase (y2 vs y1)')
plt.xlabel('y1')
plt.ylabel('y2')
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.legend()
plt.show()

print("\nObserva cómo `solve_ivp` produce una solución muy precisa y suave, incluso")
print("sin que nosotros tengamos que preocuparnos por los detalles del algoritmo.")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("`scipy.integrate.solve_ivp` es la herramienta de elección para la simulación")
print("de sistemas dinámicos complejos en ingeniería mecánica. Se utiliza en:")
print("- **Dinámica de vehículos:** Modelado de la suspensión, frenado, o aceleración.")
print("- **Sistemas de control:** Simulación de la respuesta de controladores PID o de estado.")
print("- **Termofluidos:** Simulación de la evolución de la temperatura en un sistema")
print("  con transferencia de calor y reacciones químicas.")
print("- **Robótica:** Predicción del movimiento de robots manipuladores o móviles.")
print("Su robustez y eficiencia permiten a los ingenieros concentrarse en el modelo")
print("físico del sistema, en lugar de en la implementación numérica del solucionador.")

print("\n¡Has completado el cuarto y último ejercicio del Capítulo 6!")
print("Ahora sabes cómo usar la potente función `solve_ivp` de SciPy para resolver")
print("problemas de valor inicial de EDOs, lo que es esencial para la simulación")
print("de sistemas dinámicos complejos en ingeniería.")
print("¡Felicidades por completar el Capítulo 6: Ecuaciones Diferenciales Ordinarias!")
print("¡Y felicidades por completar todo el proyecto de Métodos Numéricos!")
