# -*- coding: utf-8 -*-
"""
Capítulo 10: Transformadas de Fourier
Ejercicio 1: Introducción a las Señales y Frecuencias

Antes de sumergirnos en las Transformadas de Fourier, es fundamental entender
qué es una señal y cómo se compone de diferentes frecuencias. En ingeniería,
una señal puede ser cualquier cantidad que varía con el tiempo o el espacio:
la vibración de un motor, la presión en una tubería, la temperatura de un
componente, o una señal eléctrica.

Una señal simple puede ser una onda sinusoidal, caracterizada por su amplitud
(qué tan "grande" es), su frecuencia (qué tan rápido oscila) y su fase (dónde
comienza en el tiempo). Las señales más complejas son a menudo la suma de
muchas señales sinusoidales simples.

Imagina que estás escuchando una orquesta. Lo que oyes es una mezcla compleja
de sonidos. Pero si pudieras "descomponer" ese sonido, encontrarías que está
compuesto por las notas individuales de cada instrumento (diferentes frecuencias).
Este ejercicio te ayudará a visualizar cómo se construyen las señales.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 1: Introducción a las Señales y Frecuencias ---")

# --- Parte 1: Creación de Señales Sinusoidales Simples ---
# Una onda sinusoidal se define como: A * sin(2 * pi * f * t + phi)
# Donde: A = Amplitud, f = Frecuencia (Hz), t = Tiempo, phi = Fase (radianes)

print("\n--- Parte 1: Señales Simples ---")

# Parámetros de la señal
amplitud1 = 1.0
frecuencia1 = 1.0 # Hz
fase1 = 0.0 # radianes

amplitud2 = 0.5
frecuencia2 = 3.0 # Hz
fase2 = np.pi / 2 # 90 grados

# Vector de tiempo
t = np.linspace(0, 2, 500) # 500 puntos entre 0 y 2 segundos

# Señal 1
signal1 = amplitud1 * np.sin(2 * np.pi * frecuencia1 * t + fase1)

# Señal 2
signal2 = amplitud2 * np.sin(2 * np.pi * frecuencia2 * t + fase2)

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1) # 2 filas, 1 columna, primer gráfico
plt.plot(t, signal1, label=f'Señal 1: A={amplitud1}, f={frecuencia1} Hz', color='blue')
plt.title('Señal Sinusoidal Simple')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2) # 2 filas, 1 columna, segundo gráfico
plt.plot(t, signal2, label=f'Señal 2: A={amplitud2}, f={frecuencia2} Hz', color='green')
plt.title('Otra Señal Sinusoidal Simple')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print("Observa cómo la frecuencia afecta la rapidez de las oscilaciones.")

# --- Parte 2: Creación de una Señal Compuesta ---
# Una señal compleja es simplemente la suma de varias señales simples.

print("\n--- Parte 2: Señal Compuesta ---")

signal_compuesta = signal1 + signal2

plt.figure(figsize=(10, 5))
plt.plot(t, signal_compuesta, label='Señal Compuesta (Señal 1 + Señal 2)', color='purple')
plt.title('Señal Compuesta por la Suma de Dos Frecuencias')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()

print("La señal compuesta se ve más compleja, pero está hecha de componentes simples.")

# --- Parte 3: Señal con Ruido (Simulación de Datos Reales) ---
# En la realidad, las señales a menudo tienen ruido, que es información no deseada.

print("\n--- Parte 3: Señal con Ruido ---")

# Añadimos ruido aleatorio a la señal compuesta
ruido = 0.2 * np.random.randn(len(t)) # Ruido aleatorio con distribución normal
signal_con_ruido = signal_compuesta + ruido

plt.figure(figsize=(10, 5))
plt.plot(t, signal_con_ruido, label='Señal Compuesta con Ruido', color='orange', alpha=0.8)
plt.title('Señal Realista con Ruido')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()

print("El ruido hace que sea más difícil identificar las frecuencias originales a simple vista.")

print("\n¡Has explorado cómo se construyen las señales a partir de componentes de frecuencia!")
print("Esto es el primer paso para entender cómo las Transformadas de Fourier nos ayudan a analizarlas.")