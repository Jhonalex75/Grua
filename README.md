# Proyecto: Métodos Numéricos con Python para Ingenieros

Este proyecto tiene como objetivo enseñar métodos numéricos utilizando el lenguaje de programación Python, con un enfoque didáctico e intuitivo para personas sin experiencia previa en programación, especialmente ingenieros mecánicos.

## Configuración del Entorno de Desarrollo

Antes de ejecutar los scripts, asegúrate de tener el entorno de desarrollo configurado correctamente.

### 1. Instalar Python

Si aún no tienes Python, descárgalo desde el [sitio web oficial de Python](https://www.python.org/downloads/).

**Importante:** Durante la instalación, asegúrate de marcar la casilla que dice **"Add Python to PATH"** o **"Agregar Python al PATH"**. Esto te permitirá ejecutar Python desde cualquier terminal o símbolo del sistema.

Para verificar que Python está instalado correctamente, abre una terminal y escribe:
```bash
python --version
```
Deberías ver la versión de Python que acabas de instalar.

### 2. Instalar Bibliotecas Científicas

Para la ingeniería mecánica, no solo necesitamos Python, sino también bibliotecas especializadas que nos faciliten los cálculos y la visualización. Las instalaremos usando `pip`, el gestor de paquetes de Python.

Abre una terminal y ejecuta los siguientes comandos:

*   **NumPy:** La biblioteca fundamental para la computación numérica en Python. Proporciona estructuras de datos como los arrays (vectores y matrices) y funciones matemáticas para operar con ellos.
    ```bash
    pip install numpy
    ```

*   **Matplotlib:** La biblioteca más popular para crear gráficos y visualizaciones en Python. La usaremos para graficar los resultados de nuestras simulaciones.
    ```bash
    pip install matplotlib
    ```

*   **SciPy:** Una biblioteca de código abierto utilizada para computación científica y técnica. Contiene módulos para optimización, álgebra lineal, integración, interpolación, y más.
    ```bash
    pip install scipy
    ```

### 3. Verificar la Instalación de Tkinter

**Tkinter** es la biblioteca que usaremos para crear nuestras interfaces gráficas (GUI). Por lo general, viene incluida con la instalación estándar de Python, por lo que no se necesita una instalación por separado.

Para asegurarte de que todo está funcionando correctamente, hemos preparado un script de verificación.

### 4. Ejecutar el Script de Verificación de Tkinter

El archivo `verify_tkinter_setup.py` se encuentra en el directorio `Capitulo_07_Interfaz_Grafica_Usuario`. Contiene un pequeño programa que intenta importar las bibliotecas necesarias y crear una ventana de prueba.

Para ejecutarlo, navega a la raíz de este proyecto en tu terminal y luego ejecuta:
```bash
python Capitulo_07_Interfaz_Grafica_Usuario/verify_tkinter_setup.py
```

Si todo está configurado correctamente, verás un mensaje de éxito en la terminal y aparecerá una pequeña ventana con el título "Tkinter Verification". ¡Si ves esa ventana, estás listo para empezar!

## Estructura del Proyecto

El proyecto está organizado en capítulos, cada uno enfocado en un tema específico de métodos numéricos, con ejercicios prácticos en Python. Además, se incluye un capítulo dedicado a la interfaz gráfica de usuario.

*   `Capitulo_01_Fundamentos_Python/`: Conceptos básicos de Python, NumPy y Matplotlib.
*   `Capitulo_02_Raices_Ecuaciones/`: Métodos para encontrar raíces de ecuaciones (Bisección, Newton-Raphson, Secante, Falsa Posición).
*   `Capitulo_03_Sistemas_Ecuaciones_Lineales/`: Métodos para resolver sistemas de ecuaciones lineales (Eliminación Gaussiana, Descomposición LU, Jacobi, Gauss-Seidel).
*   `Capitulo_04_Ajuste_Curvas_Interpolacion/`: Técnicas para ajustar curvas e interpolar datos (Regresión Lineal, Interpolación Lineal, Lagrange, Splines Cúbicos).
*   `Capitulo_05_Diferenciacion_Integracion_Numerica/`: Métodos para diferenciación e integración numérica (Diferenciación, Regla del Trapecio, Simpson, SciPy Integrate).
*   `Capitulo_06_Ecuaciones_Diferenciales_Ordinarias/`: Métodos para resolver Ecuaciones Diferenciales Ordinarias (Euler, Runge-Kutta, Sistemas de EDOs, SciPy solve_ivp).
*   `Capitulo_07_Interfaz_Grafica_Usuario/`: Ejemplos y scripts relacionados con la creación de interfaces gráficas de usuario con Tkinter.
*   `Capitulo_08_Valores_Vectores_Propios/`: Conceptos y aplicaciones de valores y vectores propios en ingeniería.
*   `Capitulo_09_Problemas_Valor_Frontera/`: Métodos para resolver problemas de valor en la frontera (Método de Disparo, Diferencias Finitas).
*   `Capitulo_10_Transformadas_Fourier/`: Análisis de señales en el dominio de la frecuencia (DFT, FFT, aplicaciones).
*   `Capitulo_11_Lectura_Escritura_Datos/`: Manejo de datos en diferentes formatos de archivo (TXT, CSV, Excel, JSON).

Cada subdirectorio de capítulo contiene scripts de Python (`.py`) con explicaciones detalladas y comentarios para facilitar el aprendizaje.
