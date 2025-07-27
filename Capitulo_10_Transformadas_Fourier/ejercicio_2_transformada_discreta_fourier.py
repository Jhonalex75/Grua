# -*- coding: utf-8 -*-
"""
Capítulo 10: Transformadas de Fourier
Ejercicio 2: Transformada Discreta de Fourier (DFT) desde Cero

La Transformada Discreta de Fourier (DFT) es la herramienta matemática que nos
permite pasar una señal del dominio del tiempo al dominio de la frecuencia.
Es decir, nos ayuda a descubrir qué frecuencias están presentes en una señal
muestreada (discreta).

Aunque en la práctica usaremos algoritmos más rápidos (como la FFT), entender
cómo funciona la DFT "a mano" es crucial para comprender los principios
fundamentales. La DFT convierte una secuencia finita de muestras de tiempo
en una secuencia finita de componentes de frecuencia.

Imagina que tienes una grabación de audio (una señal en el tiempo) y quieres
saber qué notas musicales (frecuencias) se están tocando. La DFT es como un
analizador de espectro que te dice la intensidad de cada nota.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 2: Transformada Discreta de Fourier (DFT) desde Cero ---")

# --- Parte 1: Definición de una Señal de Ejemplo ---
# Usaremos una señal simple compuesta por dos senos para ver cómo la DFT los detecta.

print("\n--- Parte 1: Señal de Ejemplo ---")

# Parámetros de la señal
fs = 100 # Frecuencia de muestreo (muestras por segundo)
T = 1.0 # Duración de la señal (segundos)
n_muestras = int(fs * T) # Número total de muestras

t = np.linspace(0, T, n_muestras, endpoint=False) # Vector de tiempo

frecuencia1 = 5.0 # Hz
frecuencia2 = 15.0 # Hz
amplitud1 = 1.0
amplitud2 = 0.5

signal = amplitud1 * np.sin(2 * np.pi * frecuencia1 * t) + \
         amplitud2 * np.sin(2 * np.pi * frecuencia2 * t)

plt.figure(figsize=(10, 5))
plt.plot(t, signal, label='Señal Original', color='blue')
plt.title('Señal Compuesta en el Dominio del Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()

print("Esta señal tiene dos componentes de frecuencia ocultas.")

# --- Parte 2: Implementación de la Transformada Discreta de Fourier (DFT) ---
# La fórmula de la DFT es:
# X_k = sumatoria de (x_n * e^(-j * 2 * pi * k * n / N)) para n desde 0 hasta N-1
# Donde:
# - x_n: la n-ésima muestra de la señal en el tiempo.
# - N: el número total de muestras.
# - X_k: la k-ésima componente de frecuencia en el dominio de la frecuencia.
# - j: la unidad imaginaria (sqrt(-1)).

def dft(x):
    """
    Calcula la Transformada Discreta de Fourier (DFT) de una señal x.
    """
    N = len(x)
    X = np.zeros(N, dtype=complex) # El resultado de la DFT es un número complejo

    print(f"\n--- Parte 2: Calculando la DFT para {N} muestras ---")

    for k in range(N): # Iteramos sobre cada componente de frecuencia (k)
        suma_terminos = 0.0
        for n in range(N): # Iteramos sobre cada muestra de tiempo (n)
            angulo = 2 * np.pi * k * n / N
            # e^(-j*theta) = cos(theta) - j*sin(theta)
            suma_terminos += x[n] * (np.cos(angulo) - 1j * np.sin(angulo))
        X[k] = suma_terminos
        # print(f"  X[{k}] = {X[k]:.2f}") # Descomentar para ver cada componente

    return X

# --- Parte 3: Aplicación de la DFT y Análisis del Espectro ---

print("\n--- Parte 3: Aplicación de la DFT y Análisis del Espectro ---")

signal_dft = dft(signal)

# Calculamos las frecuencias correspondientes a cada componente de la DFT.
# Las frecuencias van desde 0 hasta fs/2 (frecuencia de Nyquist).
# Solo la primera mitad de la DFT es única y contiene información útil.

frecuencias = np.fft.fftfreq(n_muestras, 1/fs) # Genera las frecuencias para la DFT

# Nos interesan solo las frecuencias positivas (la primera mitad del espectro)
# y la magnitud de las componentes de frecuencia.

# La magnitud es el valor absoluto del número complejo.
# La potencia (o energía) de cada frecuencia es proporcional a la magnitud al cuadrado.

# Tomamos solo la primera mitad del espectro (hasta n_muestras // 2)
# Multiplicamos por 2 porque la energía se distribuye en ambas mitades (positiva y negativa).
# Dividimos por N para normalizar.

# Para una señal real, el espectro es simétrico. Solo necesitamos la primera mitad.
# La componente DC (frecuencia 0) y la frecuencia de Nyquist (si N es par) no se duplican.

# Calculamos la magnitud del espectro
magnitud_espectro = np.abs(signal_dft) / n_muestras
magnitud_espectro = magnitud_espectro[0:n_muestras // 2]
magnitud_espectro[1:] = 2 * magnitud_espectro[1:] # Duplicamos excepto la componente DC

# Obtenemos las frecuencias correspondientes
frecuencias_positivas = frecuencias[0:n_muestras // 2]

plt.figure(figsize=(10, 5))
plt.stem(frecuencias_positivas, magnitud_espectro, linefmt='-', markerfmt='o', basefmt=' ', use_line_collection=True)
plt.title('Espectro de Frecuencia (DFT)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid(True)
plt.xlim(0, fs / 2) # Mostramos hasta la frecuencia de Nyquist
plt.show()

print("\nObserva los picos en las frecuencias 5 Hz y 15 Hz, que corresponden a las frecuencias de nuestra señal original.")

print("\n¡Has implementado la Transformada Discreta de Fourier desde cero!")
print("Esto te da una comprensión profunda de cómo se analizan las frecuencias en una señal.")
