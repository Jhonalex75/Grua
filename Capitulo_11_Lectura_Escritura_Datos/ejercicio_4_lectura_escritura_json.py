# -*- coding: utf-8 -*-
"""
Capítulo 11: Lectura y Escritura de Datos
Ejercicio 4: Lectura y Escritura de Archivos JSON

JSON (JavaScript Object Notation) es un formato de intercambio de datos ligero
y fácil de leer y escribir tanto para humanos como para máquinas. Aunque su
origen está en el desarrollo web, se ha vuelto muy popular para guardar datos
estructurados, configuraciones de programas y para la comunicación entre
diferentes sistemas.

En Python, los datos JSON se mapean directamente a estructuras de datos nativas
como diccionarios y listas, lo que facilita enormemente su manejo. El módulo
`json` de Python proporciona todas las herramientas necesarias para serializar
(convertir objetos Python a JSON) y deserializar (convertir JSON a objetos Python).

Imagina que tienes un programa de simulación que utiliza una serie de parámetros
de configuración (materiales, dimensiones, condiciones de contorno). Guardar
estos parámetros en un archivo JSON permite modificarlos fácilmente sin tener
que cambiar el código, y también facilita compartir configuraciones complejas.
"""

import json

print("--- Ejercicio 4: Lectura y Escritura de Archivos JSON ---")

# --- Parte 1: Escritura de Datos en un Archivo JSON ---
# Podemos guardar diccionarios y listas de Python directamente como JSON.

print("\n--- Parte 1: Escritura de JSON ---")

# Datos de ejemplo: Configuración de un motor
configuracion_motor = {
    "nombre": "Motor Diesel XYZ",
    "potencia_hp": 150.0,
    "cilindros": 4,
    "temperatura_operacion_c": {
        "min": 80,
        "max": 120
    },
    "sensores": [
        {"tipo": "temperatura", "ubicacion": "bloque", "id": "T001"},
        {"tipo": "presion", "ubicacion": "aceite", "id": "P001"}
    ],
    "activo": True
}

nombre_archivo_json = "configuracion_motor.json"

# Usamos `json.dump()` para escribir el diccionario en un archivo.
# `indent=4` hace que el archivo JSON sea más legible para humanos (con indentación).
with open(nombre_archivo_json, 'w') as archivo_json:
    json.dump(configuracion_motor, archivo_json, indent=4)

print(f"Configuración del motor guardada en '{nombre_archivo_json}'.")

# --- Parte 2: Lectura de Datos de un Archivo JSON ---
# Podemos cargar el contenido de un archivo JSON de vuelta a un objeto Python.

print("\n--- Parte 2: Lectura de JSON ---")

configuracion_leida = {}
with open(nombre_archivo_json, 'r') as archivo_json:
    configuracion_leida = json.load(archivo_json)

print(f"Configuración leída de '{nombre_archivo_json}':")
print(configuracion_leida)

# Podemos acceder a los datos como si fuera un diccionario de Python
print(f"\nNombre del motor: {configuracion_leida['nombre']}")
print(f"Potencia: {configuracion_leida['potencia_hp']} HP")
print(f"Temperatura máxima de operación: {configuracion_leida['temperatura_operacion_c']['max']} °C")
print(f"Tipo del primer sensor: {configuracion_leida['sensores'][0]['tipo']}")

# --- Parte 3: Manejo de Errores (JSON inválido) ---
# Es importante manejar casos donde el archivo JSON no es válido.

print("\n--- Parte 3: Manejo de Errores ---")

archivo_json_invalido = "invalido.json"
contenido_invalido = "{ 'clave': 'valor', " # JSON incompleto

with open(archivo_json_invalido, 'w') as f:
    f.write(contenido_invalido)

try:
    with open(archivo_json_invalido, 'r') as f:
        json.load(f)
except json.JSONDecodeError as e:
    print(f"Error al leer JSON inválido: {e}")

# --- Ejemplo de Aplicación en Ingeniería Mecánica (Concepto) ---
print("\n--- Concepto de Aplicación en Ingeniería Mecánica ---")
print("Los archivos JSON son excelentes para:")
print("- **Guardar configuraciones de simulaciones:** Definir parámetros de entrada para modelos complejos.")
print("- **Intercambio de datos entre servicios:** Si tu programa interactúa con APIs web que proporcionan datos de sensores o información meteorológica.")
print("- **Almacenar resultados estructurados:** Por ejemplo, los resultados de un análisis de elementos finitos que incluyen propiedades de nodos, elementos y condiciones de carga.")
print("- **Definir especificaciones de componentes:** Guardar las características técnicas de piezas o ensamblajes.")

print("\n¡Has aprendido a manejar archivos JSON en Python!")
print("Esto te abre las puertas a trabajar con datos estructurados y configuraciones complejas.")
