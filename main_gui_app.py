import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import subprocess

class MainNumericalMethodsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto: Métodos Numéricos con Python")
        self.root.geometry("1200x800") # Ventana más grande para el contenido

        # Configurar la cuadrícula para la ventana principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0) # Panel izquierdo de ancho fijo
        self.root.grid_columnconfigure(1, weight=1) # Panel derecho se expande

        # --- Panel Izquierdo: Capítulos ---
        self.left_frame = ttk.Frame(self.root, padding="10", relief="raised", borderwidth=2)
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame.grid_rowconfigure(0, weight=0) # Título
        self.left_frame.grid_rowconfigure(1, weight=1) # Botones de capítulo con scroll
        self.left_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.left_frame, text="Capítulos", font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=5)

        self.chapter_buttons_frame = ttk.Frame(self.left_frame)
        self.chapter_buttons_frame.grid(row=1, column=0, sticky="nswe")
        # Usar un canvas y scrollbar para los botones de capítulo si hay muchos
        self.chapter_canvas = tk.Canvas(self.chapter_buttons_frame)
        self.chapter_scrollbar = ttk.Scrollbar(self.chapter_buttons_frame, orient="vertical", command=self.chapter_canvas.yview)
        self.chapter_scrollable_frame = ttk.Frame(self.chapter_canvas)

        self.chapter_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chapter_canvas.configure(
                scrollregion=self.chapter_canvas.bbox("all")
            )
        )

        self.chapter_canvas.create_window((0, 0), window=self.chapter_scrollable_frame, anchor="nw")
        self.chapter_canvas.configure(yscrollcommand=self.chapter_scrollbar.set)

        self.chapter_canvas.pack(side="left", fill="both", expand=True)
        self.chapter_scrollbar.pack(side="right", fill="y")

        # --- Panel Derecho: Contenido ---
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky="nswe")
        self.right_frame.grid_rowconfigure(0, weight=0) # README del capítulo
        self.right_frame.grid_rowconfigure(1, weight=0) # Botones de ejercicio
        self.right_frame.grid_rowconfigure(2, weight=1) # Mostrar código
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Mostrar README del capítulo
        self.chapter_readme_text = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, height=15, font=("Consolas", 10))
        self.chapter_readme_text.grid(row=0, column=0, sticky="nswe", pady=5)
        self.chapter_readme_text.insert(tk.END, "Selecciona un capítulo para ver su introducción aquí.")
        self.chapter_readme_text.config(state=tk.DISABLED) # Solo lectura

        # Frame para botones de ejercicio
        self.exercise_buttons_frame = ttk.Frame(self.right_frame, padding="5")
        self.exercise_buttons_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.exercise_buttons_frame.grid_columnconfigure(0, weight=1) # Para centrar botones

        # Mostrar código
        self.code_display_text = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.code_display_text.grid(row=2, column=0, sticky="nswe", pady=5)
        self.code_display_text.insert(tk.END, "Selecciona un ejercicio para ver su código aquí.")
        self.code_display_text.config(state=tk.DISABLED) # Solo lectura

        # Botón Ejecutar Ejercicio
        self.run_exercise_button = ttk.Button(self.right_frame, text="Ejecutar Ejercicio Seleccionado", command=self.run_selected_exercise, state=tk.DISABLED)
        self.run_exercise_button.grid(row=3, column=0, pady=10)

        self.load_chapters()
        self.current_chapter_path = None
        self.current_exercise_path = None

    def load_chapters(self):
        # Obtener el directorio raíz del proyecto (donde está este script)
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # Encontrar todos los directorios de capítulo (que empiezan con "Capitulo_")
        self.chapter_paths = {}
        for item in sorted(os.listdir(self.project_root)):
            full_path = os.path.join(self.project_root, item)
            if os.path.isdir(full_path) and item.startswith("Capitulo_"):
                chapter_name = item.replace("Capitulo_", "").replace("_", " ")
                self.chapter_paths[chapter_name] = full_path

        # Crear botones para cada capítulo
        for i, (name, path) in enumerate(self.chapter_paths.items()):
            btn = ttk.Button(self.chapter_scrollable_frame, text=name, command=lambda p=path, n=name: self.select_chapter(p, n))
            btn.grid(row=i, column=0, sticky="ew", pady=2, padx=5)
            self.chapter_scrollable_frame.grid_rowconfigure(i, weight=0) # No expandir filas
        self.chapter_scrollable_frame.grid_columnconfigure(0, weight=1) # Hacer que la columna se expanda

    def select_chapter(self, chapter_path, chapter_name):
        self.current_chapter_path = chapter_path
        self.current_exercise_path = None # Resetear ejercicio seleccionado

        # Limpiar botones de ejercicio anteriores
        for widget in self.exercise_buttons_frame.winfo_children():
            widget.destroy()

        # Limpiar mostrar código
        self.code_display_text.config(state=tk.NORMAL)
        self.code_display_text.delete(1.0, tk.END)
        self.code_display_text.insert(tk.END, "Selecciona un ejercicio para ver su código aquí.")
        self.code_display_text.config(state=tk.DISABLED)
        self.run_exercise_button.config(state=tk.DISABLED)

        # Cargar README del capítulo
        readme_path = os.path.join(chapter_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
            self.chapter_readme_text.config(state=tk.NORMAL)
            self.chapter_readme_text.delete(1.0, tk.END)
            self.chapter_readme_text.insert(tk.END, readme_content)
            self.chapter_readme_text.config(state=tk.DISABLED)
        else:
            self.chapter_readme_text.config(state=tk.NORMAL)
            self.chapter_readme_text.delete(1.0, tk.END)
            self.chapter_readme_text.insert(tk.END, f"No se encontró README.md para {chapter_name}.")
            self.chapter_readme_text.config(state=tk.DISABLED)

        # Cargar botones de ejercicio
        self.exercise_files = {}
        exercise_label = ttk.Label(self.exercise_buttons_frame, text="Ejercicios:", font=("Helvetica", 12, "bold"))
        exercise_label.grid(row=0, column=0, sticky="w", pady=5)
        
        for i, item in enumerate(sorted(os.listdir(chapter_path))):
            full_path = os.path.join(chapter_path, item)
            if os.path.isfile(full_path) and item.endswith(".py") and item.startswith("ejercicio_"):
                exercise_name = item.replace(".py", "").replace("ejercicio_", "").replace("_", " ")
                self.exercise_files[exercise_name] = full_path
                btn = ttk.Button(self.exercise_buttons_frame, text=exercise_name, command=lambda p=full_path: self.select_exercise(p))
                btn.grid(row=i+1, column=0, sticky="ew", pady=2)
        self.exercise_buttons_frame.grid_columnconfigure(0, weight=1)

    def select_exercise(self, exercise_path):
        self.current_exercise_path = exercise_path
        self.run_exercise_button.config(state=tk.NORMAL)

        # Mostrar código del ejercicio
        if os.path.exists(exercise_path):
            with open(exercise_path, "r", encoding="utf-8") as f:
                code_content = f.read()
            self.code_display_text.config(state=tk.NORMAL)
            self.code_display_text.delete(1.0, tk.END)
            self.code_display_text.insert(tk.END, code_content)
            self.code_display_text.config(state=tk.DISABLED)
        else:
            self.code_display_text.config(state=tk.NORMAL)
            self.code_display_text.delete(1.0, tk.END)
            self.code_display_text.insert(tk.END, "Error: Archivo de ejercicio no encontrado.")
            self.code_display_text.config(state=tk.DISABLED)
            self.run_exercise_button.config(state=tk.DISABLED)

    def run_selected_exercise(self):
        if self.current_exercise_path and os.path.exists(self.current_exercise_path):
            # Ejecutar el script en un nuevo proceso para evitar bloquear la GUI
            # y para permitir que imprima en la consola o abra sus propios gráficos.
            try:
                # Usar 'start' en Windows para abrir una nueva ventana de consola
                if os.name == 'nt': # Para Windows
                    subprocess.Popen(['start', 'cmd', '/k', 'python', self.current_exercise_path], shell=True)
                else: # Para Linux/macOS
                    subprocess.Popen(['python', self.current_exercise_path])
                print(f"Ejecutando: {self.current_exercise_path}")
            except Exception as e:
                print(f"Error al ejecutar el ejercicio: {e}")
                # Opcionalmente, mostrar error en la GUI
                self.code_display_text.config(state=tk.NORMAL)
                self.code_display_text.insert(tk.END, f"\n\nERROR AL EJECUTAR: {e}")
                self.code_display_text.config(state=tk.DISABLED)
        else:
            print("No hay ejercicio seleccionado para ejecutar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainNumericalMethodsGUI(root)
    root.mainloop()
