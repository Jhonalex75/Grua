# Curso de Python para Ingeniería: Proyecto Grúa

Bienvenido al curso práctico de Python aplicado a la ingeniería. Este repositorio contiene el material completo del curso, estructurado por capítulos, utilizando el análisis de una grúa como hilo conductor.

## 📚 Contenido del Curso

### Fundamentos y Cálculo Numérico
*   **[Capítulo 1: Fundamentos de Python](./Capitulo_01_Fundamentos_Python)** - Sintaxis básica, variables y control de flujo.
*   **[Capítulo 2: Raíces de Ecuaciones](./Capitulo_02_Raices_Ecuaciones)** - Métodos de bisección, Newton-Raphson.
*   **[Capítulo 3: Sistemas de Ecuaciones Lineales](./Capitulo_03_Sistemas_Ecuaciones_Lineales)** - Matrices y solución de sistemas.
*   **[Capítulo 4: Ajuste de Curvas e Interpolación](./Capitulo_04_Ajuste_Curvas_Interpolacion)** - Regresión lineal y polinómica.

### Cálculo Avanzado
*   **[Capítulo 5: Diferenciación e Integración Numérica](./Capitulo_05_Diferenciacion_Integracion_Numerica)**
*   **[Capítulo 6: Ecuaciones Diferenciales Ordinarias](./Capitulo_06_Ecuaciones_Diferenciales_Ordinarias)** - Modelado dinámico.
*   **[Capítulo 8: Valores y Vectores Propios](./Capitulo_08_Valores_Vectores_Propios)** - Análisis de estabilidad.
*   **[Capítulo 9: Problemas de Valor Frontera](./Capitulo_09_Problemas_Valor_Frontera)**
*   **[Capítulo 10: Transformadas de Fourier](./Capitulo_10_Transformadas_Fourier)** - Análisis de señales.

### Aplicaciones Prácticas
*   **[Capítulo 7: Interfaz Gráfica de Usuario (GUI)](./Capitulo_07_Interfaz_Grafica_Usuario)** - Creación de apps con Tkinter/Qt.
*   **[Capítulo 11: Lectura y Escritura de Datos](./Capitulo_11_Lectura_Escritura_Datos)** - Manejo de archivos CSV, JSON, Excel.

## 🏗️ Análisis de Estabilidad para Planes de Izaje Crítico

Este curso incluye un módulo especializado en la modelación de planes de izaje, fundamental para operaciones seguras en ingeniería civil y mecánica.

### Definición de Izaje Crítico
Un izaje se considera crítico cuando supera el **75% de la capacidad bruta** de la grúa, involucra cargas complejas, o se realiza en condiciones ambientales adversas.

### Variables Clave del Modelo
El módulo de análisis (ver Capítulos 2 y 6) permite calcular la estabilidad basándose en:
*   **Radio de Trabajo ($R$):** Distancia horizontal desde el centro de rotación hasta el centro de gravedad de la carga.
*   **Longitud de Pluma ($L$):** Extensión total de la pluma telescópica o reticulada.
*   **Ángulo de Pluma ($\theta$):** Ángulo respecto a la horizontal; determina la capacidad de carga.
*   **Contrapeso:** Masa necesaria para contrarrestar el momento de vuelco.

> **Nota:** Los scripts de este curso permiten verificar si un punto de operación $(R, \text{Carga})$ se encuentra dentro de la zona segura de la curva de capacidad.

## 🎓 Objetivos de Aprendizaje
Al finalizar este curso, serás capaz de:
1.  Dominar la sintaxis de Python para aplicaciones científicas.
2.  Implementar métodos numéricos para resolver problemas de ingeniería.
3.  Crear visualizaciones profesionales de datos y resultados.
4.  Desarrollar aplicaciones de escritorio con interfaz gráfica.

## 📝 Requisitos Previos
*   **Software:** Python 3.8+, VS Code (o IDE de preferencia).
*   **Conocimientos:** Conceptos básicos de álgebra lineal y cálculo.

## 🚀 Cómo usar este repositorio
1.  Clona el repositorio:
    ```bash
    git clone https://github.com/Jhonalex75/grua_python.git
    ```
2.  Instala las dependencias generales:
    ```bash
    pip install -r requirements.txt
    ```
3.  Navega a cada capítulo para ver los scripts y ejercicios específicos.

## 📄 Licencia
Este material educativo está bajo la Licencia MIT.
