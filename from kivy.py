from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
import os
import shutil
from datetime import datetime
import pandas as pd

class MantenimientoApp(App):
    def build(self):
        self.conn = sqlite3.connect("mantenimiento.db")
        self.crear_tabla()

        self.sistemas = [
            "1. Trituración",
            "2. Tolva de Finos",
            "3. Sistema de Bandas",
            "4. Molino de bolas 7x7",
            "5. Hidrociclones",
            "6. Celda Unitaria",
            "7. Celdas WS 240",
            "8. Celdas D21",
        ]

        self.equipos = {
            "1. Trituración": ["Grizzly", "Trituradora de Mandíbula", "Trituradora Cónica"],
            "2. Tolva de Finos": ["Criba", "Compuerta de Finos", "Alimentación de Banda 2"],
            "3. Sistema de Bandas": ["Banda 1", "Banda 2", "Banda 3"],
            "4. Molino de bolas 7x7": ["Molino de bolas 7x7"],
            "5. Hidrociclones": ["Hidrociclones"],
            "6. Celda Unitaria": ["Celda Unitaria"],
            "7. Celdas WS 240": ["Celdas WS 240"],
            "8. Celdas D21": ["Celdas D21"],
        }

        self.tab_panel = TabbedPanel()
        for sistema in self.sistemas:
            tab_item = TabbedPanelItem(text=sistema)
            tab_item.add_widget(self.crear_contenido_sistema(sistema))
            self.tab_panel.add_widget(tab_item)

        return self.tab_panel

    def crear_tabla(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS archivos (
                    id INTEGER PRIMARY KEY,
                    sistema TEXT,
                    equipo TEXT,
                    tipo TEXT,
                    ruta TEXT,
                    fecha TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS repuestos (
                    id INTEGER PRIMARY KEY,
                    sistema TEXT,
                    equipo TEXT,
                    nombre_repuesto TEXT,
                    codigo TEXT,
                    descripcion TEXT,
                    unidad TEXT,
                    cantidad INTEGER,
                    precio REAL,
                    proveedor TEXT,
                    fecha TEXT
                )
                """
            )
            self.conn.commit()
        except sqlite3.Error as e:
            self.mostrar_popup("Error", f"No se pudo crear la tabla: {e}")

    def crear_contenido_sistema(self, sistema):
        layout = BoxLayout(orientation='vertical')
        for equipo in self.equipos[sistema]:
            equipo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            equipo_layout.add_widget(Label(text=equipo))
            equipo_layout.add_widget(Button(text="Subir Manual", on_press=lambda x, s=sistema, e=equipo: self.subir_archivo(s, e, "Manual")))
            equipo_layout.add_widget(Button(text="Subir Registro Fotográfico", on_press=lambda x, s=sistema, e=equipo: self.subir_archivo(s, e, "Registro")))
            equipo_layout.add_widget(Button(text="Subir PDF", on_press=lambda x, s=sistema, e=equipo: self.subir_archivo(s, e, "PDF")))
            equipo_layout.add_widget(Button(text="Subir Repuestos", on_press=lambda x, s=sistema, e=equipo: self.subir_repuestos(s, e)))
            equipo_layout.add_widget(Button(text="Ver Archivos", on_press=lambda x, s=sistema, e=equipo: self.ver_archivos(s, e)))
            equipo_layout.add_widget(Button(text="Ver Repuestos", on_press=lambda x, s=sistema, e=equipo: self.ver_repuestos(s, e)))
            layout.add_widget(equipo_layout)
        return layout

    def subir_archivo(self, sistema, equipo, tipo):
        filechooser = FileChooserListView()
        popup = Popup(title=f"Seleccionar {tipo} para {equipo}", content=filechooser, size_hint=(0.9, 0.9))
        filechooser.bind(on_submit=lambda x, y, s=sistema, e=equipo, t=tipo: self.procesar_archivo(x, y, s, e, t))
        popup.open()

    def procesar_archivo(self, filechooser, selection, sistema, equipo, tipo):
        if selection:
            file_path = selection[0]
            destino = os.path.join("Archivos", sistema, equipo)
            os.makedirs(destino, exist_ok=True)
            nuevo_path = os.path.join(destino, os.path.basename(file_path))
            shutil.copy2(file_path, nuevo_path)

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO archivos (sistema, equipo, tipo, ruta, fecha) VALUES (?, ?, ?, ?, ?)",
                (sistema, equipo, tipo, nuevo_path, fecha),
            )
            self.conn.commit()
            self.mostrar_popup("Éxito", f"{tipo} subido correctamente para {equipo}")
        else:
            self.mostrar_popup("Advertencia", f"No se seleccionó ningún archivo para {equipo}")

    def subir_repuestos(self, sistema, equipo):
        filechooser = FileChooserListView(filters=["*.xlsx", "*.xls"])
        popup = Popup(title=f"Seleccionar listado de repuestos para {equipo}", content=filechooser, size_hint=(0.9, 0.9))
        filechooser.bind(on_submit=lambda x, y, s=sistema, e=equipo: self.procesar_repuestos(x, y, s, e))
        popup.open()

    def procesar_repuestos(self, filechooser, selection, sistema, equipo):
        if selection:
            file_path = selection[0]
            try:
                df = pd.read_excel(file_path)
                cursor = self.conn.cursor()
                for _, row in df.iterrows():
                    cursor.execute(
                        """
                        INSERT INTO repuestos (sistema, equipo, nombre_repuesto, codigo, descripcion, unidad, cantidad, precio, proveedor, fecha)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            sistema,
                            equipo,
                            row.get("Nombre", ""),
                            row.get("Código", ""),
                            row.get("Descripción", ""),
                            row.get("Unidad", ""),
                            int(row.get("Cantidad", 0)),
                            float(row.get("Precio", 0.0)),
                            row.get("Proveedor", ""),
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        ),
                    )
                self.conn.commit()
                self.mostrar_popup("Éxito", f"Repuestos subidos correctamente para {equipo}")
            except Exception as e:
                self.mostrar_popup("Error", f"Ocurrió un error al subir los repuestos: {e}")

    def ver_archivos(self, sistema, equipo):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT tipo, ruta, fecha
            FROM archivos 
            WHERE sistema = ? AND equipo = ?
            ORDER BY fecha
            """,
            (sistema, equipo),
        )
        archivos = cursor.fetchall()

        layout = GridLayout(cols=3, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for archivo in archivos:
            layout.add_widget(Label(text=archivo[0]))
            layout.add_widget(Label(text=archivo[1]))
            layout.add_widget(Label(text=archivo[2]))

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(layout)
        popup = Popup(title=f"Archivos - {equipo}", content=scroll_view, size_hint=(0.9, 0.9))
        popup.open()

    def ver_repuestos(self, sistema, equipo):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT nombre_repuesto, codigo, descripcion, unidad, cantidad, precio, proveedor, fecha
            FROM repuestos 
            WHERE sistema = ? AND equipo = ?
            ORDER BY nombre_repuesto
            """,
            (sistema, equipo),
        )
        repuestos = cursor.fetchall()

        layout = GridLayout(cols=8, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for repuesto in repuestos:
            layout.add_widget(Label(text=repuesto[0]))
            layout.add_widget(Label(text=repuesto[1]))
            layout.add_widget(Label(text=repuesto[2]))
            layout.add_widget(Label(text=repuesto[3]))
            layout.add_widget(Label(text=str(repuesto[4])))
            layout.add_widget(Label(text=str(repuesto[5])))
            layout.add_widget(Label(text=repuesto[6]))
            layout.add_widget(Label(text=repuesto[7]))

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(layout)
        popup = Popup(title=f"Repuestos - {equipo}", content=scroll_view, size_hint=(0.9, 0.9))
        popup.open()

    def mostrar_popup(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=mensaje))
        btn = Button(text="Cerrar", size_hint=(1, 0.25))
        content.add_widget(btn)
        popup = Popup(title=titulo, content=content, size_hint=(0.7, 0.7))
        btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    MantenimientoApp().run()