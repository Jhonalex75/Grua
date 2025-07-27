# Capítulo 11: Lectura y Escritura de Datos

En la práctica de la ingeniería, rara vez trabajamos con datos que generamos directamente en nuestro código. La mayoría de las veces, los datos provienen de fuentes externas: sensores, bases de datos, resultados de simulaciones de software especializado, o incluso tablas de propiedades de materiales. De manera similar, los resultados de nuestros análisis y simulaciones a menudo necesitan ser guardados para su posterior uso, análisis o para ser compartidos.

Este capítulo te enseñará cómo leer y escribir datos en diferentes formatos de archivo comunes, lo que es una habilidad esencial para cualquier ingeniero que trabaje con Python.

## Contenido Teórico

*   **Archivos de Texto Plano (.txt):** El formato más básico, útil para datos simples o logs.
*   **Archivos CSV (Comma Separated Values):** Un formato muy común para datos tabulares, fácil de leer y escribir por humanos y máquinas.
*   **Archivos Excel (.xlsx):** Ampliamente utilizados en la industria para organizar y analizar datos. Python puede interactuar con ellos para leer y escribir hojas de cálculo.
*   **Archivos JSON (JavaScript Object Notation):** Un formato ligero para el intercambio de datos, muy utilizado en aplicaciones web y APIs, pero también útil para guardar configuraciones o datos estructurados.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_lectura_escritura_txt.py`

*   **Descripción:** Demuestra cómo leer y escribir datos en archivos de texto plano (`.txt`). Se cubren operaciones básicas como abrir, leer línea por línea y escribir contenido.
*   **Conceptos Clave:** `open()`, `read()`, `readline()`, `readlines()`, `write()`, `writelines()`, `with` statement, manejo de archivos.

### `ejercicio_2_lectura_escritura_csv.py`

*   **Descripción:** Explora la lectura y escritura de archivos CSV utilizando el módulo `csv` de Python y la biblioteca `pandas`, que es la herramienta preferida para manejar datos tabulares en Python.
*   **Conceptos Clave:** `csv` module, `pandas.read_csv()`, `DataFrame.to_csv()`, datos tabulares, delimitadores.

### `ejercicio_3_lectura_escritura_excel.py`

*   **Descripción:** Muestra cómo leer datos de hojas de cálculo Excel (`.xlsx`) y cómo escribir resultados en nuevas hojas o archivos Excel utilizando la biblioteca `pandas`.
*   **Conceptos Clave:** `pandas.read_excel()`, `DataFrame.to_excel()`, hojas de cálculo, múltiples hojas.

### `ejercicio_4_lectura_escritura_json.py`

*   **Descripción:** Demuestra cómo trabajar con archivos JSON para guardar y cargar datos estructurados (diccionarios y listas de Python). Útil para configuraciones o datos jerárquicos.
*   **Conceptos Clave:** `json` module, `json.load()`, `json.dump()`, serialización, deserialización, datos estructurados.
