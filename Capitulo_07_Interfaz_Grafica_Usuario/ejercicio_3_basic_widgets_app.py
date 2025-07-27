# ----------------------------------------------------------------------------
# Capítulo 4: Aplicación con Widgets Básicos
#
# Propósito:
# Este script introduce cómo construir una aplicación GUI usando una clase de Python.
# Usar una clase es un enfoque más organizado y escalable que manejar cada
# widget (elemento gráfico) como una variable separada.
# ----------------------------------------------------------------------------

# Primero, importamos la biblioteca Tkinter. La renombramos a 'tk' por convención,
# para que sea más corto y fácil de escribir.
import tkinter as tk

# --- Estructura Profesional de GUI: Usando una Clase ---
# Cuando las aplicaciones crecen, manejar todos los widgets (botones, etiquetas, etc.)
# como variables separadas se vuelve desordenado. Una clase funciona como una plantilla
# o un contenedor para nuestra aplicación, manteniendo todos los widgets y funciones
# relacionados, ordenados y en un solo lugar.

class BasicApp:
    """
    Esta clase encapsula (contiene) toda nuestra aplicación de interfaz gráfica.
    """
    # El método __init__ es el "constructor" de nuestra clase. Se ejecuta
    # automáticamente cuando creamos un nuevo objeto de la clase BasicApp.
    # 'root' es la ventana principal que le pasamos para construir nuestra app dentro de ella.
    def __init__(self, root):
        """
        El constructor de la clase de nuestra aplicación.
        'root' es la ventana principal en la que se construirá esta aplicación.
        """
        # Guardamos una referencia a la ventana principal (root) para poder usarla
        # en otros métodos de la clase. 'self' se refiere al objeto actual.
        self.root = root
        
        # Configuramos las propiedades de la ventana principal.
        self.root.title("App con Widgets Básicos")  # Título de la ventana.
        self.root.geometry("400x250")  # Tamaño inicial: 400 píxeles de ancho x 250 de alto.

        # --- Creación de los Widgets ---
        # Ahora, creamos los elementos gráficos (widgets) que irán dentro de la ventana.
        # Los guardamos como atributos del objeto (usando 'self.') para poder
        # acceder a ellos fácilmente desde otras partes de la clase.

        # 1. Creamos una Etiqueta (Label) para mostrar instrucciones al usuario.
        #    - El primer argumento (self.root) indica que esta etiqueta pertenece a la ventana principal.
        #    - 'text' es el texto que mostrará.
        #    - 'font' nos permite personalizar la fuente y su tamaño.
        self.instruction_label = tk.Label(self.root, text="Por favor, introduce tu nombre:", font=("Helvetica", 12))
        # '.pack()' es un método para colocar el widget en la ventana.
        # 'pady' añade un pequeño espacio vertical (padding) arriba y abajo de la etiqueta.
        self.instruction_label.pack(pady=10)

        # 2. Creamos un Campo de Entrada (Entry) para que el usuario pueda escribir texto.
        #    - 'width' controla el ancho del campo de entrada.
        self.name_entry = tk.Entry(self.root, width=30, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        # 3. Creamos un Botón (Button) que el usuario puede presionar.
        #    - 'command' es muy importante: especifica la función que se ejecutará
        #      cuando se haga clic en el botón. Aquí, llamará al método 'self.show_greeting'.
        self.greet_button = tk.Button(self.root, text="Mostrar Saludo", command=self.show_greeting)
        self.greet_button.pack(pady=15)

        # 4. Creamos otra Etiqueta para mostrar el resultado.
        #    - Inicialmente, no tiene texto ('text=""'). Lo actualizaremos más tarde.
        #    - 'bold' hace que el texto aparezca en negrita.
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14, "bold"))
        self.result_label.pack(pady=10)

    # Este es un método de nuestra clase. Los métodos son funciones que pertenecen a una clase.
    def show_greeting(self):
        """
        Este método se llama cuando se hace clic en el botón 'greet_button'.
        """
        # Obtenemos el texto que el usuario escribió en el campo de entrada (Entry).
        # El método '.get()' recupera el contenido del widget.
        user_name = self.name_entry.get()

        # Verificamos si el usuario realmente escribió algo.
        if user_name:
            # Si hay un nombre, creamos un saludo personalizado.
            # La 'f' antes de la cadena (f-string) nos permite incrustar variables fácilmente.
            greeting = f"¡Hola, {user_name}!"
        else:
            # Si el campo está vacío, le pedimos al usuario que escriba un nombre.
            greeting = "Por favor, introduce un nombre primero."

        # Actualizamos el texto de la etiqueta de resultado.
        # El método '.config()' nos permite cambiar las propiedades de un widget después de crearlo.
        self.result_label.config(text=greeting)

def main():
    """
    La función principal que prepara y ejecuta la aplicación.
    """
    # 1. Creamos la instancia de la ventana principal. Esta es la base de nuestra GUI.
    root = tk.Tk()
    
    # 2. Creamos una instancia de nuestra clase de aplicación.
    #    Le pasamos la ventana 'root' para que la clase pueda construir los widgets dentro de ella.
    app = BasicApp(root)
    
    # 3. Iniciamos el bucle de eventos de Tkinter.
    #    Esta línea es fundamental: muestra la ventana y la mantiene abierta,
    #    esperando a que el usuario interactúe con ella (haga clic, escriba, etc.).
    #    El programa se detiene aquí hasta que se cierra la ventana.
    root.mainloop()

# Esta es una construcción estándar en Python.
# El código dentro de este 'if' solo se ejecutará si este script es el archivo
# principal que se está ejecutando (y no si es importado por otro script).
if __name__ == "__main__":
    main()
