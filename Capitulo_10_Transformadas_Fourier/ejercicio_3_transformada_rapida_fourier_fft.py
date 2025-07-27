# -*- coding: utf-8 -*-
"""
Capítulo 10: Transformadas de Fourier
Ejercicio 3: Transformada Rápida de Fourier (FFT) con NumPy

En el ejercicio anterior, implementamos la Transformada Discreta de Fourier (DFT)
desde cero. Aunque es excelente para entender el concepto, la DFT es computacionalmente
muy lenta para señales largas. Aquí es donde entra la Transformada Rápida de Fourier (FFT).

La FFT es un algoritmo *extremadamente eficiente* para calcular la DFT. No es una
transformada diferente, sino una forma mucho más rápida de calcular la misma DFT.
Gracias a la FFT, el análisis de frecuencia se ha vuelto práctico para una vasta
gama de aplicaciones en ingeniería, desde el procesamiento de audio y video hasta
el análisis de vibraciones y el diseño de filtros.

NumPy, a través de su módulo `numpy.fft`, proporciona una implementación optimizada
de la FFT. Este ejercicio te mostrará cómo usarla y cómo interpretar sus resultados,
incluyendo el manejo de señales con ruido.
"""

import numpy as np
import matplotlib.pyplot as plt

print("--- Ejercicio 3: Transformada Rápida de Fourier (FFT) con NumPy ---")

# --- Parte 1: Definición de una Señal de Ejemplo con Ruido ---
# Usaremos una señal similar a la del ejercicio 1, pero con más ruido, para
# demostrar la capacidad de la FFT para extraer las frecuencias subyacentes.

print("\n--- Parte 1: Señal de Ejemplo con Ruido ---")

fs = 200 # Frecuencia de muestreo (muestras por segundo)
T = 2.0 # Duración de la señal (segundos)
n_muestras = int(fs * T) # Número total de muestras

t = np.linspace(0, T, n_muestras, endpoint=False) # Vector de tiempo

frecuencia1 = 10.0 # Hz
frecuencia2 = 30.0 # Hz
amplitud1 = 1.0
amplitud2 = 0.7

signal_pura = amplitud1 * np.sin(2 * np.pi * frecuencia1 * t) + \
              amplitud2 * np.sin(2 * np.pi * frecuencia2 * t)

# Añadimos ruido significativo
ruido = 0.5 * np.random.randn(n_muestras) # Ruido aleatorio con distribución normal
signal_con_ruido = signal_pura + ruido

plt.figure(figsize=(10, 5))
plt.plot(t, signal_con_ruido, label='Señal con Ruido', color='orange', alpha=0.8)
plt.title('Señal Compuesta con Ruido en el Dominio del Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()

print("Esta señal es difícil de analizar a simple vista debido al ruido.")

# --- Parte 2: Aplicación de la Transformada Rápida de Fourier (FFT) ---
# Usaremos `np.fft.fft` para calcular la DFT de nuestra señal.
# Luego, `np.fft.fftfreq` para obtener las frecuencias correspondientes.

print("\n--- Parte 2: Aplicación de la FFT ---")

# Realizamos la FFT de la señal con ruido
fft_resultado = np.fft.fft(signal_con_ruido)

# Obtenemos las frecuencias correspondientes a cada componente de la FFT
frecuencias = np.fft.fftfreq(n_muestras, 1/fs)

# Calculamos la magnitud (amplitud) de cada componente de frecuencia
magnitud_espectro = np.abs(fft_resultado)

# --- Parte 3: Interpretación y Visualización del Espectro de Frecuencia ---
# Para una señal real, el espectro de frecuencia es simétrico. Solo necesitamos
# la primera mitad (frecuencias positivas) para el análisis.

print("\n--- Parte 3: Visualización del Espectro ---")

# Filtramos para mostrar solo las frecuencias positivas
indices_frecuencias_positivas = frecuencias >= 0
frecuencias_positivas = frecuencias[indices_frecuencias_positivas]
magnitud_espectro_positivas = magnitud_espectro[indices_frecuencias_positivas]

# Normalizamos la magnitud para que represente la amplitud real de las ondas sinusoidales.
# Dividimos por N y multiplicamos por 2 (excepto la componente DC, que no se duplica).
# La componente DC (frecuencia 0) es el primer elemento.

magnitud_espectro_normalizada = magnitud_espectro_positivas / n_muestras
magnitud_espectro_normalizada[1:] = 2 * magnitud_espectro_normalizada[1:]

plt.figure(figsize=(10, 5))
plt.stem(frecuencias_positivas, magnitud_espectro_normalizada, linefmt='-', markerfmt='o', basefmt=' ', use_line_collection=True)
plt.title('Espectro de Frecuencia (FFT) de la Señal con Ruido')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.xlim(0, fs / 2) # Mostrar hasta la frecuencia de Nyquist
plt.ylim(0, 1.2 * np.max(magnitud_espectro_normalizada)) # Ajustar límite Y
plt.show()

print("\n¡La FFT nos permite ver claramente los picos en 10 Hz y 30 Hz, a pesar del ruido!")
print("Esto demuestra el poder de la FFT para el análisis de señales.")

# --- Parte 4: Filtrado Conceptual (Opcional) ---
# Una vez que identificamos las frecuencias, podríamos "filtrar" el ruido.
# Esto es conceptual, no una implementación de filtro real.

print("\n--- Parte 4: Filtrado Conceptual ---")

# Creamos una copia del resultado de la FFT
fft_filtrado = fft_resultado.copy()

# Identificamos las frecuencias que queremos mantener (ej. entre 5 Hz y 35 Hz)
# y ponemos a cero las demás.

# En el espectro de la FFT, las frecuencias están ordenadas de 0 a fs/2, luego -fs/2 a 0.
# np.fft.fftfreq nos da el orden correcto.

# Encontramos los índices de las frecuencias que queremos mantener
# Por ejemplo, queremos mantener las frecuencias de 10 Hz y 30 Hz.
# Los índices de estas frecuencias y sus contrapartes negativas deben mantenerse.

# Para este ejemplo simple, vamos a poner a cero todas las componentes
# cuya magnitud sea muy pequeña (considerándolas ruido).

threshold = 0.1 # Umbral para considerar una componente como ruido
fft_filtrado[np.abs(fft_filtrado) < threshold * n_muestras] = 0 # Poner a cero las componentes pequeñas

# Invertimos la FFT para obtener la señal filtrada en el dominio del tiempo
signal_filtrada = np.fft.ifft(fft_filtrado)

plt.figure(figsize=(10, 5))
plt.plot(t, signal_con_ruido, label='Señal Original con Ruido', color='gray', alpha=0.5)
plt.plot(t, signal_filtrada.real, label='Señal Filtrada (Parte Real)', color='green')
plt.title('Señal Filtrada del Ruido (Conceptual)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()

print("\nObserva cómo la señal filtrada se parece mucho más a la señal pura original.")
print("Esto es el principio del filtrado de señales usando el dominio de la frecuencia.")

print("\n¡Has dominado la Transformada Rápida de Fourier con NumPy!")
print("Esta es una herramienta esencial para el análisis de señales en ingeniería.")
