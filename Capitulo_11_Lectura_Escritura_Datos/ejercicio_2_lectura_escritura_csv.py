# -*- coding: utf-8 -*-
"""
Capítulo 11: Lectura y Escritura de Datos
Ejercicio 2: Lectura y Escritura de Archivos CSV

Los archivos CSV (Comma Separated Values) son uno de los formatos más comunes
y versátiles para almacenar datos tabulares (datos organizados en filas y
columnas). Son ampliamente utilizados en ingeniería para intercambiar datos
entre diferentes programas, bases de datos o para almacenar resultados de
experimentos y simulaciones.

Python tiene un módulo `csv` incorporado para manejar estos archivos, pero
la biblioteca `pandas` es la herramienta *estándar de facto* para trabajar
con datos tabulares en Python. `pandas` proporciona una estructura de datos
llamada `DataFrame`, que es como una hoja de cálculo o una tabla de base de
datos, y facilita enormemente la lectura, escritura y manipulación de datos.

Imagina que tienes un archivo CSV con mediciones de presión, temperatura y
caudal de un proceso industrial. Necesitas leer esos datos para analizarlos
y luego guardar tus resultados (por ejemplo, un cálculo de eficiencia) en
otro archivo CSV.
"""

import pandas as pd # Importamos pandas, la convención es 'pd'
import numpy as np # Para generar datos de ejemplo

print("--- Ejercicio 2: Lectura y Escritura de Archivos CSV ---")

# --- Parte 1: Creación y Escritura de un Archivo CSV con Pandas ---
# Pandas facilita la creación de DataFrames y su exportación a CSV.

print("\n--- Parte 1: Escritura de CSV ---")

# Creamos un DataFrame de ejemplo con datos de un ensayo de tracción
datos_ensayo = {
    'Deformacion_mm': np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5]),
    'Fuerza_N': np.array([0, 100, 210, 305, 390, 450]),
    'Temperatura_C': np.array([20, 20, 21, 21, 22, 22])
}

df_ensayo = pd.DataFrame(datos_ensayo)

nombre_archivo_csv = "ensayo_traccion.csv"

# Guardamos el DataFrame en un archivo CSV
# `index=False` evita que pandas escriba el índice del DataFrame como una columna en el CSV.
df_ensayo.to_csv(nombre_archivo_csv, index=False)

print(f"Datos de ensayo guardados en '{nombre_archivo_csv}'.")
print("Contenido del DataFrame original:")
print(df_ensayo)

# --- Parte 2: Lectura de un Archivo CSV con Pandas ---
# Leer un CSV es tan simple como usar `pd.read_csv()`.

print("\n--- Parte 2: Lectura de CSV ---")

df_leido = pd.read_csv(nombre_archivo_csv)

print(f"Datos leídos de '{nombre_archivo_csv}':")
print(df_leido)

# Podemos acceder a columnas como si fueran atributos o elementos de diccionario
print("\nColumna 'Fuerza_N':")
print(df_leido['Fuerza_N'])

# Podemos realizar operaciones directamente sobre las columnas
print(f"\nFuerza promedio: {df_leido['Fuerza_N'].mean():.2f} N")
print(f"Deformación máxima: {df_leido['Deformacion_mm'].max():.2f} mm")

# --- Parte 3: Escritura de un CSV con el Módulo `csv` (Alternativa Básica) ---
# Para casos muy simples o cuando no se quiere usar pandas.

print("\n--- Parte 3: Escritura con módulo `csv` ---")

import csv

nombre_archivo_csv_basico = "mediciones_sensor.csv"

# Datos de ejemplo: tiempo, voltaje, corriente
mediciones = [
    ['Tiempo (s)', 'Voltaje (V)', 'Corriente (A)'], # Cabecera
    [0.1, 12.1, 0.5],
    [0.2, 12.0, 0.52],
    [0.3, 11.9, 0.51]
]

with open(nombre_archivo_csv_basico, 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(mediciones)

print(f"Datos de mediciones guardados en '{nombre_archivo_csv_basico}'.")

# --- Parte 4: Lectura de un CSV con el Módulo `csv` ---

print("\n--- Parte 4: Lectura con módulo `csv` ---")

mediciones_leidas = []
with open(nombre_archivo_csv_basico, 'r', newline='') as archivo_csv:
    lector_csv = csv.reader(archivo_csv)
    for fila in lector_csv:
        mediciones_leidas.append(fila)

print(f"Datos leídos de '{nombre_archivo_csv_basico}':")
for fila in mediciones_leidas:
    print(fila)

print("\n¡Has aprendido a manejar archivos CSV en Python, tanto con pandas como con el módulo csv!")
print("Esta es una habilidad esencial para el manejo de datos en ingeniería.")
