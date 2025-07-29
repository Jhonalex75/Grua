import sys
import os
import json
import uuid
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QStackedWidget, QDialog, QFormLayout, QDateEdit, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QScrollArea,
    QFrame
)
from PySide6.QtCore import Qt, QDate, Slot, Signal
from PySide6.QtGui import QIcon, QFont
from google.cloud import firestore
import requests # Para la API REST de Firebase Auth

# --- Configuración de Firebase ---
# Intenta cargar la configuración desde variables de entorno o un archivo local
# Para Firestore, necesitarás configurar las credenciales de Google Cloud.
# Esto usualmente se hace estableciendo la variable de entorno GOOGLE_APPLICATION_CREDENTIALS
# para que apunte a tu archivo JSON de clave de cuenta de servicio.
# Ejemplo: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ruta/a/tu/clave-servicio.json"
#
# Para la autenticación anónima, necesitaremos la Web API Key de tu proyecto Firebase.
try:
    FIREBASE_CONFIG_JSON = os.environ.get("__FIREBASE_CONFIG")
    if FIREBASE_CONFIG_JSON:
        FIREBASE_CONFIG = json.loads(FIREBASE_CONFIG_JSON)
        FIREBASE_WEB_API_KEY = FIREBASE_CONFIG.get("apiKey")
        PROJECT_ID = FIREBASE_CONFIG.get("projectId")
    else: # Fallback a valores de placeholder si no se encuentra la config
        print("ADVERTENCIA: Configuración de Firebase no encontrada en __FIREBASE_CONFIG. Usando placeholders.")
        print("             La autenticación y Firestore podrían no funcionar.")
        print("             Asegúrate de configurar GOOGLE_APPLICATION_CREDENTIALS y FIREBASE_WEB_API_KEY.")
        FIREBASE_WEB_API_KEY = "YOUR_WEB_API_KEY" # REEMPLAZA ESTO
        PROJECT_ID = "YOUR_PROJECT_ID" # REEMPLAZA ESTO
        # Configura tus credenciales de Google Cloud aquí si es necesario
        # Ejemplo: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/serviceAccountKey.json"

except KeyError:
    print("ADVERTENCIA: No se pudo cargar la configuración de Firebase. Funcionalidad limitada.")
    FIREBASE_WEB_API_KEY = "YOUR_WEB_API_KEY_FALLBACK" # REEMPLAZA ESTO
    PROJECT_ID = "YOUR_PROJECT_ID_FALLBACK" # REEMPLAZA ESTO

APP_ID = os.environ.get("__APP_ID", "p6-simulator-python-default")

# Inicializar cliente de Firestore
# Si GOOGLE_APPLICATION_CREDENTIALS está configurado correctamente, esto debería funcionar.
try:
    db = firestore.Client(project=PROJECT_ID)
except Exception as e:
    print(f"Error inicializando Firestore: {e}. Asegúrate que las credenciales estén bien configuradas.")
    db = None


USER_ID = None # Se establecerá después de la autenticación

# --- Autenticación Anónima con Firebase REST API ---
def firebase_anonymous_auth():
    global USER_ID
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    payload = json.dumps({"returnSecureToken": True})
    
    try:
        response = requests.post(rest_api_url, data=payload)
        response.raise_for_status() # Lanza un error para respuestas HTTP malas (4xx o 5xx)
        auth_data = response.json()
        USER_ID = auth_data.get("localId")
        # id_token = auth_data.get("idToken") # Podría usarse para llamadas autenticadas a otros servicios
        print(f"Autenticación anónima exitosa. User ID: {USER_ID}")
        return USER_ID
    except requests.exceptions.RequestException as e:
        print(f"Error en la autenticación anónima con Firebase: {e}")
        print("Detalles de la respuesta:", response.text if 'response' in locals() else "No response object")
        # Fallback a un UUID local si la autenticación falla, para permitir uso offline limitado
        USER_ID = str(uuid.uuid4())
        print(f"Fallback a User ID local: {USER_ID}")
        QMessageBox.warning(None, "Error de Autenticación", 
                            f"No se pudo autenticar anónimamente con Firebase: {e}.\n"
                            "Se usará un ID local. Algunas funcionalidades podrían no estar disponibles.")
        return USER_ID
    except json.JSONDecodeError:
        print(f"Error decodificando respuesta JSON de Firebase Auth.")
        QMessageBox.critical(None, "Error de Autenticación", "Respuesta inválida del servidor de autenticación.")
        return None


# --- Modelos de Datos (Simplificados) ---
class Project:
    def __init__(self, id, name, start_date, created_at=None, wbs=None, activities=None, data_date=None):
        self.id = id
        self.name = name
        self.start_date = start_date # String YYYY-MM-DD
        self.created_at = created_at or firestore.SERVER_TIMESTAMP
        self.wbs = wbs if wbs is not None else [{"id": f"wbs-root-{uuid.uuid4()}", "name": name, "parentId": None, "path": "0"}]
        self.activities = activities if activities is not None else []
        self.data_date = data_date or start_date

    def to_dict(self):
        return {
            "name": self.name,
            "startDate": self.start_date,
            "createdAt": self.created_at,
            "wbs": self.wbs,
            "activities": self.activities,
            "dataDate": self.data_date
        }

    @staticmethod
    def from_dict(source_dict, id_val):
        # Convertir Timestamps de Firestore a string si es necesario
        created_at_val = source_dict.get("createdAt")
        if isinstance(created_at_val, firestore.SERVER_TIMESTAMP.__class__): # Comparar con la clase de firestore.SERVER_TIMESTAMP
             created_at_val = None # Dejar que se actualice o manejarlo como string
        elif hasattr(created_at_val, 'isoformat'): # Es un datetime object
            created_at_val = created_at_val.isoformat()

        return Project(
            id=id_val,
            name=source_dict.get("name"),
            start_date=source_dict.get("startDate"),
            created_at=created_at_val,
            wbs=source_dict.get("wbs", []),
            activities=source_dict.get("activities", []),
            data_date=source_dict.get("dataDate")
        )

# --- Diálogos ---
class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Proyecto")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit()
        self.start_date_edit = QDateEdit(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")

        self.layout.addRow("Nombre del Proyecto:", self.name_edit)
        self.layout.addRow("Fecha de Inicio:", self.start_date_edit)

        self.buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("Crear")
        self.cancel_button = QPushButton("Cancelar")
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addRow(self.buttons_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "start_date": self.start_date_edit.date().toString("yyyy-MM-dd")
        }

# --- Vistas Principales (Widgets para el QStackedWidget) ---
class HomeView(QWidget):
    project_selected = Signal(str) # Emite el ID del proyecto seleccionado

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel("Mis Proyectos")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        self.new_project_button = QPushButton("Crear Nuevo Proyecto")
        self.new_project_button.setIcon(QIcon.fromTheme("document-new", QIcon("icons/document-new.png"))) # Placeholder icon
        self.layout.addWidget(self.new_project_button)
        
        self.project_list_widget = QListWidget()
        self.project_list_widget.itemDoubleClicked.connect(self._handle_project_selected)
        self.layout.addWidget(self.project_list_widget)
        
        self.loading_label = QLabel("Cargando proyectos...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()
        self.layout.addWidget(self.loading_label)

    def load_projects(self):
        if not db or not USER_ID:
            self.project_list_widget.addItem("Error: Firestore o User ID no configurado.")
            return

        self.loading_label.show()
        self.project_list_widget.clear()
        try:
            projects_ref = db.collection(f"artifacts/{APP_ID}/users/{USER_ID}/p6_projects")
            docs = projects_ref.order_by("createdAt", direction=firestore.Query.DESCENDING).stream()
            
            projects_found = False
            for doc_snap in docs:
                project = Project.from_dict(doc_snap.to_dict(), doc_snap.id)
                item = QListWidgetItem(f"{project.name} (Inicio: {project.start_date})")
                item.setData(Qt.ItemDataRole.UserRole, project.id) # Guardar ID del proyecto en el item
                self.project_list_widget.addItem(item)
                projects_found = True
            
            if not projects_found:
                self.project_list_widget.addItem("No hay proyectos. ¡Crea uno!")

        except Exception as e:
            print(f"Error cargando proyectos desde Firestore: {e}")
            self.project_list_widget.addItem(f"Error al cargar proyectos: {e}")
            QMessageBox.critical(self, "Error de Firestore", f"No se pudieron cargar los proyectos: {e}")
        finally:
            self.loading_label.hide()

    @Slot(QListWidgetItem)
    def _handle_project_selected(self, item):
        project_id = item.data(Qt.ItemDataRole.UserRole)
        if project_id:
            self.project_selected.emit(project_id)

class PlaceholderView(QWidget):
    def __init__(self, view_name, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel(f"Vista: {view_name}\n(Funcionalidad Próximamente)")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

# --- Ventana Principal ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Simulador P6 Básico (Python/PySide6) - App ID: {APP_ID}")
        self.setGeometry(100, 100, 1200, 800)
        
        self.current_project_id = None
        self.current_project_data = None

        # Autenticar primero
        if not USER_ID: # Si no se autenticó al inicio
            if not firebase_anonymous_auth():
                 QMessageBox.critical(self, "Fallo Crítico de Autenticación", 
                                     "La aplicación no puede continuar sin un User ID. Revisa la configuración de Firebase.")
                 # sys.exit(1) # O manejar de otra forma
                 # Por ahora, permitimos continuar con un USER_ID de fallback si la autenticación falló pero generó uno.
                 if not USER_ID: # Si sigue sin USER_ID después del fallback
                    sys.exit(1)


        # Layout principal con QSplitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        # Sidebar (panel izquierdo)
        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.nav_buttons = {}
        nav_items = [
            ("home", "Inicio"), ("projectSetup", "Proyecto"), ("wbs", "EDT (WBS)"),
            ("activities", "Actividades"), ("schedule", "Programación"), ("costs", "Costos"),
            ("resources", "Recursos (Pronto)"), ("baselines", "Líneas Base (Pronto)")
        ]

        for key, label in nav_items:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, k=key: self.switch_view(k))
            self.sidebar_layout.addWidget(btn)
            self.nav_buttons[key] = btn
        
        self.sidebar_layout.addStretch()
        self.splitter.addWidget(self.sidebar_widget)

        # Contenido Principal (panel derecho)
        self.main_content_stack = QStackedWidget()
        self.splitter.addWidget(self.main_content_stack)
        
        self.splitter.setSizes([200, 600]) # Tamaños iniciales para sidebar y contenido

        # Crear Vistas
        self.home_view = HomeView()
        self.home_view.new_project_button.clicked.connect(self.handle_new_project)
        self.home_view.project_selected.connect(self.handle_project_selected_from_home)

        self.views = {
            "home": self.home_view,
            "projectSetup": PlaceholderView("Configuración Proyecto"), # Placeholder por ahora
            "wbs": PlaceholderView("EDT / WBS"), # Placeholder por ahora
            "activities": PlaceholderView("Actividades"), # Placeholder por ahora
            "schedule": PlaceholderView("Programación"), # Placeholder por ahora
            "costs": PlaceholderView("Costos"), # Placeholder por ahora
            # ... añadir más vistas aquí
        }

        for key, widget in self.views.items():
            self.main_content_stack.addWidget(widget)

        self.switch_view("home") # Vista inicial
        self.home_view.load_projects() # Cargar proyectos al inicio

    def switch_view(self, view_key):
        if view_key in self.views:
            if view_key != "home" and not self.current_project_id:
                QMessageBox.information(self, "Información", "Por favor, selecciona o crea un proyecto primero.")
                return
            self.main_content_stack.setCurrentWidget(self.views[view_key])
            
            # Actualizar estilo de botón activo (opcional)
            for key, btn in self.nav_buttons.items():
                is_active = (key == view_key)
                btn.setStyleSheet("background-color: lightblue;" if is_active else "")
        else:
            print(f"Advertencia: Vista '{view_key}' no encontrada.")
            
    def handle_new_project(self):
        if not db or not USER_ID:
            QMessageBox.critical(self, "Error", "Firestore o User ID no está configurado. No se puede crear proyecto.")
            return

        dialog = NewProjectDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data["name"].strip():
                QMessageBox.warning(self, "Entrada Inválida", "El nombre del proyecto no puede estar vacío.")
                return

            new_project_data = Project(
                id=None, # Firestore generará el ID
                name=data["name"],
                start_date=data["start_date"]
            )
            
            try:
                # Añadir a Firestore
                projects_ref = db.collection(f"artifacts/{APP_ID}/users/{USER_ID}/p6_projects")
                # Firestore genera el ID automáticamente con .add()
                timestamp, doc_ref = projects_ref.add(new_project_data.to_dict()) 
                
                print(f"Proyecto '{data['name']}' creado con ID: {doc_ref.id}")
                QMessageBox.information(self, "Proyecto Creado", f"Proyecto '{data['name']}' creado exitosamente.")
                self.home_view.load_projects() # Recargar lista de proyectos
                self.handle_project_selected_from_home(doc_ref.id) # Seleccionar el nuevo proyecto
            except Exception as e:
                print(f"Error creando proyecto en Firestore: {e}")
                QMessageBox.critical(self, "Error de Firestore", f"No se pudo crear el proyecto: {e}")

    @Slot(str)
    def handle_project_selected_from_home(self, project_id):
        self.current_project_id = project_id
        print(f"Proyecto seleccionado: {project_id}")
        # Aquí cargarías los datos completos del proyecto si es necesario para otras vistas
        # self.load_project_details(project_id) 
        self.switch_view("projectSetup") # Ir a la vista de configuración del proyecto (actualmente placeholder)


if __name__ == "__main__":
    # Intento de autenticación al inicio de la app
    if not firebase_anonymous_auth():
        print("Fallo en la autenticación inicial. La aplicación podría no funcionar correctamente.")
        if not USER_ID:
            sys.exit("Saliendo debido a fallo de autenticación.")

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

'''
**Archivo `requirements.txt` (sugerido):**
```txt
PySide6
google-cloud-firestore
requests
'''


''''
1.  **Configuración de Firebase:**
    * **Autenticación:** Este código intenta realizar una autenticación anónima usando la API REST de Firebase. Necesitarás reemplazar `"YOUR_WEB_API_KEY"` con la clave API web real de tu proyecto Firebase.
    * **Firestore:** Para que Firestore funcione, debes:
        * Tener la biblioteca `google-cloud-firestore` instalada.
        * Configurar las credenciales de Google Cloud. La forma más común es descargar el archivo JSON de la clave de tu cuenta de servicio desde la consola de Google Cloud y luego establecer la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` para que apunte a la ruta de este archivo.
        * Reemplazar `"YOUR_PROJECT_ID"` con el ID de tu proyecto de Firebase/Google Cloud si no se carga desde `__FIREBASE_CONFIG`.
    * Las variables `__FIREBASE_CONFIG` y `__APP_ID` se intentan leer del entorno, similar a como podría funcionar en el Canvas. Si no están presentes, se usan valores de fallback.

2.  **Funcionalidad Implementada:**
    * Estructura básica de la ventana principal con una barra lateral para navegación y un área de contenido principal.
    * Autenticación anónima al iniciar la aplicación. Si falla, intenta usar un UUID local como `USER_ID` para permitir una funcionalidad muy limitada y muestra una advertencia.
    * **Vista de Inicio (`HomeView`):**
        * Muestra una lista de proyectos obtenidos de Firestore.
        * Botón para "Crear Nuevo Proyecto".
    * **Creación de Nuevo Proyecto:**
        * Un diálogo (`NewProjectDialog`) permite ingresar el nombre y la fecha de inicio.
        * El nuevo proyecto se guarda en Firestore bajo la ruta `artifacts/{APP_ID}/users/{USER_ID}/p6_projects`.
    * **Selección de Proyecto:** Hacer doble clic en un proyecto de la lista (en `HomeView`) emitirá una señal (aún no conectada para cargar detalles completos del proyecto, pero sí para cambiar de vista).
    * Las demás vistas ("Configuración Proyecto", "EDT", "Actividades", etc.) son actualmente `PlaceholderView` que indican que la funcionalidad vendrá próximamente.

3.  **Ejecución:**
    * Guarda el código como un archivo `.py` (por ejemplo, `p6_simulator_qt.py`).
    * Asegúrate de tener PySide6, google-cloud-firestore y requests instalados (`pip install PySide6 google-cloud-firestore requests`).
    * Configura tus credenciales de Firebase/Google Cloud como se mencionó anteriormente.
    * Ejecuta el script: `python p6_simulator_qt.py`.

4.  **Próximos Pasos en el Desarrollo (Iteraciones Futuras):**
    * **Cargar Detalles del Proyecto:** Al seleccionar un proyecto, cargar todos sus datos (WBS, actividades) y mostrarlos en las vistas correspondientes.
    * **Implementar Vistas Detalladas:**
        * `ProjectSetupView`: Editar nombre, fechas del proyecto.
        * `WBSEditorView`: Crear, editar, eliminar elementos WBS (probablemente usando un `QTreeView`).
        * `ActivityEditorView`: Crear, editar, eliminar actividades, incluyendo predecesoras y costos.
        * `SchedulingView`: Implementar la lógica de CPM (Pase Adelante, Pase Atrás) y mostrar los resultados.
        * `CostsView`: Mostrar resúmenes de costos.
    * **Carta Gantt:** Este es el componente más complejo de replicar. En Qt, podrías usar `QGraphicsView` y `QGraphicsScene` para dibujar las barras y la línea de tiempo, o buscar bibliotecas de gráficos de terceros para Python/Qt si existen y son adecuadas.
    * **Mejorar Manejo de Errores y UI:** Añadir más validaciones, mejores notificaciones, iconos, etc.

Esta es una base para comenzar. La conversión completa es un proyecto de desarrollo significativo. Dime si tienes preguntas sobre esta estructura inicial o cómo te gustaría proced
'''