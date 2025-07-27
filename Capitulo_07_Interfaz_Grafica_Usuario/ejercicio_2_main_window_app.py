# ----------------------------------------------------------------------------
# Capítulo 3: Aplicación de la Ventana Principal
#
# Propósito:
# Este script demuestra los pasos fundamentales para crear la ventana
# principal de una aplicación de escritorio utilizando la biblioteca Tkinter.
# ----------------------------------------------------------------------------

# 1. Importar la biblioteca Tkinter
#    La importamos y le damos el alias 'tk' por convención.
#    Esto hace que el código sea más limpio y fácil de escribir.
import tkinter as tk

def main():
    """
    Esta función contiene la lógica principal para crear y ejecutar
    nuestra sencilla aplicación con ventana.
    """
    # 2. Crear la instancia de la ventana principal de la aplicación.
    #    La clase `tk.Tk()` crea la ventana de nivel superior. Solo deberías
    #    tener una de estas en tu aplicación. La asignamos a una variable,
    #    convencionalmente llamada 'root', 'window', o 'app'.
    window = tk.Tk()

    # 3. Configurar las propiedades de la ventana. 
    #    - .title(): Establece el texto que aparece en la barra de título de la ventana.
    #    - .geometry(): Establece el tamaño inicial de la ventana en píxeles ("ancho x alto").
    window.title("Herramienta de Ingeniería Mecánica")
    window.geometry("600x400") # Ancho=600px, Alto=400px

    # 4. Iniciar el bucle de eventos de Tkinter.
    #    Este es el paso más importante. El método .mainloop() le dice a Python
    #    que muestre la ventana y escuche los eventos (como clics del ratón o
    #    pulsaciones de teclas). El programa permanecerá en este bucle hasta
    #    que se cierre la ventana. Sin esta línea, la ventana aparecería
    #    y desaparecería instantáneamente.
    window.mainloop()

# Esta es una convención estándar de Python.
# El código dentro de este bloque 'if' solo se ejecutará cuando el script
# se ejecute directamente (por ejemplo, `python main_window_app.py`).
# No se ejecutará si el script se importa como un módulo en otro archivo.
if __name__ == "__main__":
    main()