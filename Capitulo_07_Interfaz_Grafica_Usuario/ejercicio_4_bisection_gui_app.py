# ----------------------------------------------------------------------------
# Capítulo 6: Aplicación GUI del Método de Bisección
#
# Propósito:
# Este script construye una aplicación GUI completa que permite al usuario
# encontrar la raíz de una función usando el método de bisección.
# Demuestra el concepto crucial de separar la lógica de la presentación
# al importar la función `bisection_method` desde otro archivo.
# ----------------------------------------------------------------------------

# Importamos las bibliotecas necesarias.
import tkinter as tk
# ttk es un módulo de Tkinter que nos da acceso a widgets con un aspecto más moderno.
from tkinter import ttk

# --- Paso 1: Importar la lógica del backend ---
# Esta es la parte más importante: en lugar de escribir el código del método
# numérico aquí, lo importamos desde un archivo separado.
# Esto se llama "separación de conceptos" y es una práctica de programación excelente
# porque mantiene nuestro código organizado, reutilizable y fácil de mantener.
from bisection_method_logic import bisection_method, example_function

class BisectionApp:
    """
    Esta clase encapsula toda la GUI para el solucionador del método de bisección.
    """
    def __init__(self, root):
        # Guardamos la ventana principal (root) y la configuramos.
        self.root = root
        self.root.title("Solucionador por Método de Bisección")
        self.root.geometry("450x400")

        # Usamos un estilo moderno para que la aplicación se vea mejor.
        style = ttk.Style()
        style.theme_use('clam')  # Puedes probar otros temas como 'alt', 'default', 'classic'.

        # --- Creamos y organizamos los widgets usando frames ---
        # Los "Frames" son como cajas o contenedores que nos ayudan a agrupar y organizar otros widgets.
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True) # fill y expand hacen que el frame ocupe todo el espacio disponible.

        # Creamos un frame dedicado para los campos de entrada.
        # "LabelFrame" es un frame que además tiene un título visible.
        input_frame = ttk.LabelFrame(main_frame, text="Parámetros de Entrada", padding="15")
        input_frame.pack(fill=tk.X, pady=10)

        # Creamos los widgets para que el usuario introduzca los datos.
        # Usamos un método auxiliar `_create_labeled_entry` para no repetir código.
        self.a_entry = self._create_labeled_entry(input_frame, "Inicio del Intervalo (a):")
        self.b_entry = self._create_labeled_entry(input_frame, "Fin del Intervalo (b):")
        self.tol_entry = self._create_labeled_entry(input_frame, "Tolerancia:", "1e-7") # 1e-7 es notación científica para 0.0000001

        # --- Botón de Cálculo ---
        calculate_button = ttk.Button(main_frame, text="Calcular Raíz", command=self.calculate_root)
        calculate_button.pack(pady=15)

        # --- Área de Resultados ---
        result_frame = ttk.LabelFrame(main_frame, text="Resultado", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_label = ttk.Label(result_frame, text="Por favor, introduce los parámetros y haz clic en calcular.", font=("Helvetica", 12, "italic"))
        self.result_label.pack(pady=10)

    def _create_labeled_entry(self, parent, label_text, default_value=""):
        """Método auxiliar para crear una etiqueta y un campo de entrada de forma ordenada."""
        # Este es un truco para mantener el código limpio. Esta función crea un pequeño
        # frame, le pone una etiqueta a la izquierda y un campo de entrada a la derecha.
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        label = ttk.Label(frame, text=label_text, width=18)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry.insert(0, default_value) # Inserta un valor por defecto en el campo.
        return entry

    def calculate_root(self):
        """
        Este método se llama cuando se presiona el botón. Recoge los datos,
        llama al método de bisección y muestra el resultado.
        """
        try:
            # 1. Obtener y validar la entrada del usuario.
            #    Usamos float() para convertir el texto de los campos de entrada a números.
            #    Si el usuario escribe algo que no es un número, esto lanzará un error.
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tolerance = float(self.tol_entry.get())

            # 2. Llamar a la función importada del método de bisección.
            #    Le pasamos la función a resolver, los intervalos y la tolerancia.
            root = bisection_method(example_function, a, b, tolerance)

            # 3. Mostrar el resultado en la etiqueta de resultado.
            if root is not None:
                # Si se encontró una raíz, la mostramos formateada y en color verde.
                result_text = f"Raíz Aproximada: {root:.7f}" # Formatea el número a 7 decimales.
                self.result_label.config(text=result_text, foreground="green", font=("Helvetica", 12, "bold"))
            else:
                # Si el método no encontró una raíz, mostramos un mensaje de advertencia.
                result_text = "No se pudo converger. Intenta aumentar las iteraciones o cambiar el intervalo."
                self.result_label.config(text=result_text, foreground="orange", font=("Helvetica", 12, "italic"))

        except ValueError as e:
            # Este bloque se ejecuta si ocurre un error al convertir los datos a número
            # o si la propia función de bisección lanza un error de valor.
            self.result_label.config(text=f"Error: {e}", foreground="red", font=("Helvetica", 12, "italic"))
        except Exception as e:
            # Este bloque atrapa cualquier otro error inesperado para que la app no se cierre.
            self.result_label.config(text=f"Ocurrió un error inesperado: {e}", foreground="red", font=("Helvetica", 12, "italic"))

def main():
    # La función principal que prepara y ejecuta la aplicación.
    root = tk.Tk()
    app = BisectionApp(root)
    root.mainloop()

# El punto de entrada estándar para un script de Python.
if __name__ == "__main__":
    main()
