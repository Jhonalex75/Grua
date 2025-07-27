# -*- coding: utf-8 -*-
"""
Capítulo 11: Lectura y Escritura de Datos
Ejercicio 3: Lectura y Escritura de Archivos Excel (.xlsx)

Microsoft Excel es una herramienta omnipresente en la ingeniería para la
organización, análisis y presentación de datos. Poder interactuar con archivos
Excel directamente desde Python es una habilidad muy valiosa, ya que permite
automatizar tareas, integrar análisis complejos y generar informes.

La biblioteca `pandas` es, de nuevo, la herramienta más potente y conveniente
para leer y escribir archivos Excel en Python. Puede manejar múltiples hojas,
diferentes rangos de datos y formatos.

Imagina que recibes datos de pruebas de materiales en un archivo Excel, o que
necesitas generar un informe con los resultados de tu simulación en un formato
que otros ingenieros puedan abrir y manipular fácilmente en Excel.
"""

import pandas as pd
import numpy as np

print("--- Ejercicio 3: Lectura y Escritura de Archivos Excel (.xlsx) ---")

# --- Parte 1: Escritura de Datos en un Archivo Excel con Pandas ---
# Pandas puede exportar DataFrames directamente a archivos Excel.

print("\n--- Parte 1: Escritura de Excel ---")

# Datos de ejemplo: Rendimiento de una bomba
datos_bomba = {
    'Caudal (m3/h)': np.array([10, 20, 30, 40, 50]),
    'Altura (m)': np.array([35, 32, 28, 22, 15]),
    'Eficiencia (%)': np.array([60, 72, 78, 75, 65])
}

df_bomba = pd.DataFrame(datos_bomba)

nombre_archivo_excel = "rendimiento_bomba.xlsx"

# Guardamos el DataFrame en una hoja de Excel. Si el archivo no existe, lo crea.
# `sheet_name` especifica el nombre de la hoja.
# `index=False` evita escribir el índice del DataFrame en el Excel.
df_bomba.to_excel(nombre_archivo_excel, sheet_name='Curva de Bomba', index=False)

print(f"Datos de rendimiento de bomba guardados en '{nombre_archivo_excel}'.")
print("Contenido del DataFrame original:")
print(df_bomba)

# --- Parte 2: Escritura en Múltiples Hojas de un Archivo Excel ---
# Podemos escribir varios DataFrames en diferentes hojas del mismo archivo Excel.

print("\n--- Parte 2: Escritura en Múltiples Hojas ---")

# Datos de ejemplo: Propiedades de materiales
datos_materiales = {
    'Material': ['Acero', 'Aluminio', 'Cobre'],
    'Densidad (kg/m3)': [7850, 2700, 8960],
    'Modulo Young (GPa)': [200, 70, 110]
}

df_materiales = pd.DataFrame(datos_materiales)

# Creamos un objeto ExcelWriter para gestionar la escritura en múltiples hojas.
with pd.ExcelWriter(nombre_archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    # Escribimos el DataFrame de materiales en una nueva hoja
    df_materiales.to_excel(writer, sheet_name='Propiedades Materiales', index=False)

print(f"Datos de materiales añadidos a '{nombre_archivo_excel}' en una nueva hoja.")

# --- Parte 3: Lectura de Datos de un Archivo Excel ---
# Podemos leer hojas específicas o todas las hojas de un archivo Excel.

print("\n--- Parte 3: Lectura de Excel ---")

# Leer una hoja específica por su nombre
df_bomba_leido = pd.read_excel(nombre_archivo_excel, sheet_name='Curva de Bomba')
print(f"\nDatos leídos de la hoja 'Curva de Bomba':")
print(df_bomba_leido)

# Leer otra hoja específica
df_materiales_leido = pd.read_excel(nombre_archivo_excel, sheet_name='Propiedades Materiales')
print(f"\nDatos leídos de la hoja 'Propiedades Materiales':")
print(df_materiales_leido)

# Leer todas las hojas en un diccionario de DataFrames
# Cada clave del diccionario será el nombre de la hoja.
excel_dict = pd.read_excel(nombre_archivo_excel, sheet_name=None) # sheet_name=None lee todas las hojas
print("\nTodas las hojas leídas (diccionario de DataFrames):")
for sheet_name, df in excel_dict.items():
    print(f"\nHoja: {sheet_name}")
    print(df)

print("\n¡Has aprendido a manejar archivos Excel en Python con pandas!")
print("Esto te permite automatizar el procesamiento de datos y la generación de informes.")
