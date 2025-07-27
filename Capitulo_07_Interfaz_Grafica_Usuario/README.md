# Capítulo 7: Interfaz Gráfica de Usuario (GUI) con Tkinter

Este capítulo se enfoca en la creación de interfaces gráficas de usuario (GUI) utilizando la biblioteca Tkinter, que viene incluida con Python. Aprenderás los fundamentos para construir aplicaciones interactivas que faciliten la interacción con los métodos numéricos.

## Contenido Teórico

Las interfaces gráficas de usuario permiten a los usuarios interactuar con los programas de una manera más intuitiva que la línea de comandos. Tkinter es la biblioteca estándar de Python para crear GUIs, ofreciendo una forma sencilla de construir ventanas, botones, campos de entrada y otros elementos visuales.

*   **Ventana Principal:** El contenedor fundamental de cualquier aplicación GUI.
*   **Widgets:** Elementos interactivos como etiquetas, campos de entrada y botones.
*   **Separación de Responsabilidades:** La buena práctica de mantener la lógica del programa (los métodos numéricos) separada de la interfaz de usuario.
*   **Validación Frontend:** Verificar la entrada del usuario antes de procesarla para mejorar la robustez y la experiencia del usuario.
*   **Incrustación de Gráficos:** Integrar visualizaciones de Matplotlib directamente en la ventana de la aplicación.

## Ejercicios Prácticos

Cada ejercicio es un script de Python (`.py`) con comentarios detallados y ejemplos relevantes para la ingeniería.

### `ejercicio_1_verify_tkinter_setup.py`

*   **Descripción:** Un script simple para verificar que la biblioteca Tkinter está correctamente instalada y funcionando en tu entorno Python. Es el primer paso para asegurar que puedes desarrollar GUIs.
*   **Conceptos Clave:** Importación de `tkinter`, creación de una ventana básica, `mainloop()`.

### `ejercicio_2_main_window_app.py`

*   **Descripción:** Demuestra los pasos fundamentales para crear la ventana principal de una aplicación de escritorio con Tkinter. Aprenderás a configurar el título y el tamaño de la ventana.
*   **Conceptos Clave:** `tk.Tk()`, `title()`, `geometry()`, `mainloop()`.

### `ejercicio_3_basic_widgets_app.py`

*   **Descripción:** Introduce cómo construir una aplicación GUI utilizando una clase de Python para organizar el código. Muestra cómo usar widgets básicos como `Label` (etiquetas), `Entry` (campos de entrada) y `Button` (botones), y cómo hacer que interactúen.
*   **Conceptos Clave:** Clases en Python, `__init__`, `Label`, `Entry`, `Button`, `pack()`, `get()`, `config()`, manejo de eventos.

### `ejercicio_4_bisection_gui_app.py`

*   **Descripción:** Construye una aplicación GUI completa que permite al usuario encontrar la raíz de una función usando el método de bisección. Demuestra la separación de la lógica (importando el método de bisección) de la presentación.
*   **Conceptos Clave:** Importación de módulos propios, `ttk` (temas y widgets mejorados), `Frame`, `LabelFrame`, manejo de entrada numérica, visualización de resultados.

### `ejercicio_5_bisection_gui_app_final.py`

*   **Descripción:** Representa una versión pulida de la aplicación GUI del método de bisección, añadiendo validación frontend para proporcionar retroalimentación instantánea al usuario y prevenir errores antes de que lleguen al algoritmo principal.
*   **Conceptos Clave:** Validación de entrada, manejo de errores (`try-except`), mejora de la experiencia del usuario.

### `ejercicio_6_mass_spring_damper_app.py`

*   **Descripción:** Una aplicación GUI avanzada que simula el comportamiento de un sistema masa-resorte-amortiguador. Permite al usuario cambiar los parámetros físicos y ver la respuesta del sistema en tiempo real, incluyendo la incrustación de gráficos de Matplotlib en la ventana de Tkinter.
*   **Conceptos Clave:** Simulación de sistemas dinámicos, integración de Matplotlib en Tkinter, interactividad con parámetros físicos, aplicación completa de ingeniería.