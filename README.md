
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

El repositorio está organizado para que cualquier usuario, incluso sin experiencia en programación, pueda navegarlo fácilmente y aprovechar todos los recursos educativos. La estructura principal es la siguiente:

- **`main_gui_app.py`**: Es la aplicación principal con interfaz gráfica (GUI). Se recomienda iniciar el estudio desde aquí, ya que permite navegar los capítulos y ejemplos de manera intuitiva.

- **Capítulos de Métodos Numéricos**
    - `Capitulo_01_Fundamentos_Python/` a `Capitulo_11_Lectura_Escritura_Datos/`: Cada carpeta corresponde a un tema fundamental de métodos numéricos, con ejercicios prácticos y explicaciones paso a paso.

- **`Ejemplos_y_Scripts/`**: Contiene notebooks, scripts, gráficos y hojas de cálculo adicionales, independientes de los capítulos principales. Aquí encontrarás ejemplos prácticos, materiales de apoyo y recursos para experimentar.

- **`Recursos_Graficos/`**: Imágenes, diagramas y gráficos utilizados en los capítulos y ejemplos. Útil para visualizar conceptos y resultados.

- **`Datos_y_Documentos/`**: Archivos de datos (Excel, CSV, bases de datos) y documentos PDF de referencia. Estos recursos pueden ser utilizados por los scripts y notebooks, o consultados como material de apoyo.

- **`Documentacion_Adicional/`**: Manuales, guías, informes, carpetas de proyectos anteriores y cualquier documentación complementaria relevante para el aprendizaje o referencia.

Cada carpeta contiene un archivo `README.md` explicando su contenido y propósito. Si tienes dudas sobre dónde encontrar o guardar un archivo, consulta el README correspondiente o inicia desde la aplicación GUI.

---

> **Recomendación:** Si eres nuevo, comienza por ejecutar `main_gui_app.py` para navegar el contenido de forma guiada y sencilla.
# Grua
Modelacion plan de izaje par grúa y parámetros fundamentales para considerar en un izaje critico

