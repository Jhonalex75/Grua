# -*- coding: utf-8 -*-
"""
Capítulo 10: Transformadas de Fourier
Ejercicio 4: Aplicación en Análisis de Vibraciones

El análisis de vibraciones es una aplicación crucial de las Transformadas de
Fourier en ingeniería mecánica. Las vibraciones excesivas en maquinaria o
estructuras pueden indicar fallas, desgaste o problemas de diseño. Al analizar
la señal de vibración en el dominio de la frecuencia, podemos identificar las
frecuencias dominantes y, a menudo, correlacionarlas con componentes específicos
del sistema (rodamientos, engranajes, desequilibrios, etc.).

Este ejercicio simulará una señal de vibración que podría provenir de un sensor
(como un acelerómetro) en una máquina. Luego, utilizaremos la FFT para analizar
esta señal y detectar las frecuencias de vibración más significativas.

Imagina que eres un ingeniero de mantenimiento y tienes un sensor en un motor.
Si el motor empieza a vibrar de forma extraña, la FFT te puede decir si la
vibración es causada por un desequilibrio (una frecuencia) o por un rodamiento
dañado (otra frecuencia), lo que te ayuda a diagnosticar el problema.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 4: Aplicación en Análisis de Vibraciones ---")

# --- Parte 1: Simulación de una Señal de Vibración ---
# Crearemos una señal que simula la vibración de una máquina con dos componentes
# de frecuencia principales y algo de ruido.

print("\n--- Parte 1: Señal de Vibración Simulada ---")

fs = 1000 # Frecuencia de muestreo (Hz) - Típica para vibraciones
T = 5.0 # Duración de la señal (segundos)
n_muestras = int(fs * T) # Número total de muestras

t = np.linspace(0, T, n_muestras, endpoint=False) # Vector de tiempo

# Componentes de frecuencia de la vibración
frecuencia_motor = 20.0 # Hz (ej. velocidad de rotación del motor)
frecuencia_rodamiento = 75.0 # Hz (ej. frecuencia de falla de un rodamiento)

amplitud_motor = 1.5
amplitud_rodamiento = 0.8

signal_vibracion = amplitud_motor * np.sin(2 * np.pi * frecuencia_motor * t) + \
                   amplitud_rodamiento * np.sin(2 * np.pi * frecuencia_rodamiento * t)

# Añadimos ruido aleatorio (siempre presente en mediciones reales)
ruido = 0.3 * np.random.randn(n_muestras)
signal_vibracion_con_ruido = signal_vibracion + ruido

plt.figure(figsize=(12, 6))
plt.plot(t, signal_vibracion_con_ruido, label='Señal de Vibración con Ruido', color='blue', alpha=0.7)
plt.title('Señal de Vibración Simulada en el Dominio del Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud de Vibración')
plt.grid(True)
plt.legend()
plt.show()

print("La señal de vibración en el tiempo es compleja debido a múltiples fuentes y ruido.")

# --- Parte 2: Análisis de Frecuencia con FFT ---
# Usaremos la FFT para transformar la señal al dominio de la frecuencia y
# revelar sus componentes principales.

print("\n--- Parte 2: Análisis de Frecuencia con FFT ---")

# Realizamos la FFT
fft_resultado = np.fft.fft(signal_vibracion_con_ruido)

# Obtenemos las frecuencias correspondientes
frecuencias = np.fft.fftfreq(n_muestras, 1/fs)

# Calculamos la magnitud del espectro y normalizamos para amplitudes reales
magnitud_espectro = np.abs(fft_resultado) / n_muestras

# Nos quedamos solo con las frecuencias positivas
indices_frecuencias_positivas = frecuencias >= 0
frecuencias_positivas = frecuencias[indices_frecuencias_positivas]
magnitud_espectro_positivas = magnitud_espectro[indices_frecuencias_positivas]

magnitud_espectro_positivas[1:] = 2 * magnitud_espectro_positivas[1:] # Duplicamos excepto DC

plt.figure(figsize=(12, 6))
plt.stem(frecuencias_positivas, magnitud_espectro_positivas, linefmt='-', markerfmt='o', basefmt=' ', use_line_collection=True)
plt.title('Espectro de Frecuencia de Vibración (FFT)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud de Vibración')
plt.grid(True)
plt.xlim(0, fs / 2) # Mostrar hasta la frecuencia de Nyquist
plt.ylim(0, 1.2 * np.max(magnitud_espectro_positivas)) # Ajustar límite Y
plt.show()

print("\nObserva los picos claros en las frecuencias de 20 Hz y 75 Hz.")
print("Estos picos nos indican las frecuencias dominantes de vibración en la máquina.")

# --- Parte 3: Identificación de Frecuencias Dominantes ---
# Podemos encontrar las frecuencias más altas en el espectro.

print("\n--- Parte 3: Identificación de Frecuencias Dominantes ---")

# Encontramos los índices de los picos más altos (excluyendo la componente DC)
# np.argsort devuelve los índices que ordenarían el array.
# [::-1] invierte el orden para obtener los más grandes primero.
# [1:6] para obtener los 5 picos más grandes (excluyendo el DC en el índice 0).

picos_indices = np.argsort(magnitud_espectro_positivas)[::-1][1:6] # Top 5 picos (excluyendo DC)

print("Las 5 frecuencias de vibración más dominantes son:")
for idx in picos_indices:
    frec = frecuencias_positivas[idx]
    magn = magnitud_espectro_positivas[idx]
    print(f"  - Frecuencia: {frec:.2f} Hz, Amplitud: {magn:.2f}")

print("\n¡Has aplicado la FFT para el análisis de vibraciones!")
print("Esta técnica es una herramienta poderosa para el diagnóstico de maquinaria,")
print("el monitoreo de la salud estructural y el diseño de sistemas dinámicos.")
