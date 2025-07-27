# -*- coding: utf-8 -*-
"""
Capítulo 11: Lectura y Escritura de Datos
Ejercicio 1: Lectura y Escritura de Archivos de Texto Plano (.txt)

Los archivos de texto plano (.txt) son el formato más básico y universal para
almacenar información. Aunque no son estructurados como las hojas de cálculo,
son extremadamente útiles para guardar datos simples, registros (logs) o
configuraciones. En ingeniería, a menudo nos encontramos con datos de sensores
o resultados de simulaciones en este formato.

Este ejercicio te enseñará las operaciones fundamentales para interactuar con
archivos .txt en Python: cómo abrirlos, leer su contenido (línea por línea o
completo) y escribir nueva información en ellos.

Imagina que tienes un sensor que registra la temperatura de un motor cada
cierto tiempo y guarda esos datos en un archivo de texto. Necesitas saber
cómo leer ese archivo para analizar las temperaturas, o cómo guardar los
resultados de tu análisis en otro archivo de texto.
"""

print("--- Ejercicio 1: Lectura y Escritura de Archivos de Texto Plano (.txt) ---")

# --- Parte 1: Escritura de Datos en un Archivo de Texto ---
# Para escribir en un archivo, primero debemos abrirlo. Usamos la función `open()`.
# El segundo argumento es el "modo":
# - 'w': write (escritura). Si el archivo existe, lo sobrescribe. Si no existe, lo crea.
# - 'a': append (añadir). Si el archivo existe, añade contenido al final. Si no existe, lo crea.
# - 'r': read (lectura). Para leer un archivo existente.

print("\n--- Parte 1: Escritura de Datos ---")

nombre_archivo_salida = "datos_temperatura.txt"

# Usar `with open(...)` es la forma recomendada. Asegura que el archivo se cierre
# automáticamente, incluso si ocurre un error.
with open(nombre_archivo_salida, 'w') as archivo:
    archivo.write("Temperatura del Motor (C)\n") # Escribimos una cabecera
    archivo.write("-----------------------\n")
    archivo.write("25.3\n")
    archivo.write("26.1\n")
    archivo.write("27.5\n")
    archivo.write("28.0\n")
    archivo.write("27.8\n")

print(f"Datos escritos en '{nombre_archivo_salida}'.")

# Ahora, añadamos más datos al mismo archivo sin borrar lo anterior.
with open(nombre_archivo_salida, 'a') as archivo:
    archivo.write("29.1\n")
    archivo.write("30.5\n")

print(f"Más datos añadidos a '{nombre_archivo_salida}'.")

# --- Parte 2: Lectura de Datos de un Archivo de Texto ---
# Para leer, abrimos el archivo en modo 'r' (read).

print("\n--- Parte 2: Lectura de Datos ---")

# 2.1: Leer el archivo completo de una vez (`read()`)
print(f"\nContenido completo de '{nombre_archivo_salida}':")
with open(nombre_archivo_salida, 'r') as archivo:
    contenido = archivo.read()
    print(contenido)

# 2.2: Leer el archivo línea por línea (`readline()` o iterando sobre el archivo)
print(f"\nLeyendo línea por línea de '{nombre_archivo_salida}':")
with open(nombre_archivo_salida, 'r') as archivo:
    for linea in archivo:
        print(f"  {linea.strip()}") # .strip() elimina espacios en blanco y saltos de línea al inicio/final

# 2.3: Leer todas las líneas en una lista (`readlines()`)
print(f"\nLeyendo todas las líneas en una lista de '{nombre_archivo_salida}':")
with open(nombre_archivo_salida, 'r') as archivo:
    lineas = archivo.readlines()
    for i, linea in enumerate(lineas):
        print(f"  Línea {i+1}: {linea.strip()}")

# --- Parte 3: Procesamiento Básico de Datos Leídos ---
# A menudo, queremos extraer números de las líneas de texto.

print("\n--- Parte 3: Procesamiento Básico ---")

temperaturas_leidas = []
with open(nombre_archivo_salida, 'r') as archivo:
    # Saltamos las dos primeras líneas (cabecera)
    next(archivo) # Salta la primera línea
    next(archivo) # Salta la segunda línea
    for linea in archivo:
        try:
            temp = float(linea.strip()) # Convertimos la línea a un número flotante
            temperaturas_leidas.append(temp)
        except ValueError:
            print(f"Advertencia: No se pudo convertir la línea '{linea.strip()}' a número. Ignorando.")

print("Temperaturas numéricas leídas:", temperaturas_leidas)
print(f"Temperatura promedio: {np.mean(temperaturas_leidas):.2f}°C")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("La lectura y escritura de archivos de texto es fundamental para:")
print("- **Procesar datos de sensores:** Leer archivos de datos generados por equipos de prueba.")
print("- **Guardar resultados de simulaciones:** Almacenar grandes volúmenes de datos de simulaciones numéricas.")
print("- **Archivos de configuración:** Leer parámetros de entrada para modelos o programas.")
print("- **Generación de informes simples:** Escribir resúmenes o tablas de resultados en un formato legible.")

print("\n¡Has aprendido a manejar archivos de texto plano en Python!")
print("Esta es una habilidad básica pero poderosa para la gestión de datos en ingeniería.")
