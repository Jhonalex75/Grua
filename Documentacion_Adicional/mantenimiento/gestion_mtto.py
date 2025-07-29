from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from pathlib import Path
import pandas as pd
import io
from werkzeug.utils import secure_filename

# Definir la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

# Clave secreta para mensajes flash y sesiones
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maintenance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de subida de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Hacer que `now` esté disponible en todas las plantillas Jinja2
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Modelo para el Equipo
class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(100), nullable=False)
    model_type = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    purchase_date = db.Column(db.DateTime)
    installation_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    department = db.Column(db.String(100))
    technical_specifications = db.Column(db.Text)
    maintenance_frequency = db.Column(db.Integer)
    documents = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con las actividades
    activities = db.relationship('Activity', backref='equipment', lazy=True)

# Modelo para las Actividades
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    activity_type = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    technician = db.Column(db.String(100))
    parts_replaced = db.Column(db.Text)
    cost = db.Column(db.Float)
    status = db.Column(db.String(50))
    observations = db.Column(db.Text)
    documents = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'xls', 'xlsx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    try:
        equipments = Equipment.query.all()
        return render_template('index.html', equipments=equipments)
    except Exception as e:
        flash(f'Error al cargar equipos: {str(e)}')
        return redirect(url_for('index'))

@app.route('/equipment/new', methods=['GET', 'POST'])
def new_equipment():
    if request.method == 'POST':
        try:
            equipment = Equipment(
                equipment_name=request.form['equipment_name'],
                model_type=request.form['model_type'],
                serial_number=request.form['serial_number'],
                manufacturer=request.form['manufacturer'],
                purchase_date=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d'),
                installation_date=datetime.strptime(request.form['installation_date'], '%Y-%m-%d'),
                location=request.form['location'],
                department=request.form['department'],
                technical_specifications=request.form['technical_specifications'],
                maintenance_frequency=int(request.form['maintenance_frequency'])
            )

            # Manejo de archivos adjuntos
            if 'documents' in request.files:
                files = request.files.getlist('documents')
                doc_names = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        doc_names.append(filename)

                if doc_names:
                    equipment.documents = ','.join(doc_names)

            db.session.add(equipment)
            db.session.commit()
            flash('Equipo registrado exitosamente')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar equipo: {str(e)}')

    return render_template('new_equipment.html')

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            flash('El archivo no existe')
            return redirect(url_for('index'))
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f'Error al descargar el archivo: {str(e)}')
        return redirect(url_for('index'))

@app.route('/export/<int:equipment_id>')
def export_equipment_history(equipment_id):
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        activities = Activity.query.filter_by(equipment_id=equipment_id).all()

        # Datos del equipo
        equipment_data = [{
            'ID': equipment.id,
            'Nombre del Equipo': equipment.equipment_name,
            'Modelo': equipment.model_type,
            'Número de Serie': equipment.serial_number,
            'Fabricante': equipment.manufacturer,
            'Fecha de Compra': equipment.purchase_date.strftime('%Y-%m-%d') if equipment.purchase_date else '',
            'Fecha de Instalación': equipment.installation_date.strftime('%Y-%m-%d') if equipment.installation_date else '',
            'Ubicación': equipment.location,
            'Departamento': equipment.department,
            'Especificaciones Técnicas': equipment.technical_specifications,
            'Frecuencia de Mantenimiento (días)': equipment.maintenance_frequency,
            'Documentos': equipment.documents
        }]

        # Datos de actividades
        activities_data = [
            {
                'Fecha': activity.date.strftime('%Y-%m-%d'),
                'Tipo de Actividad': activity.activity_type,
                'Descripción': activity.description,
                'Técnico': activity.technician,
                'Repuestos': activity.parts_replaced,
                'Costo': activity.cost,
                'Estado': activity.status,
                'Observaciones': activity.observations,
                'Documentos': activity.documents
            }
            for activity in activities
        ]

        # Crear Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            pd.DataFrame(equipment_data).to_excel(writer, sheet_name='Equipo', index=False)
            pd.DataFrame(activities_data).to_excel(writer, sheet_name='Actividades', index=False) if activities_data else None
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'equipo_{equipment.id}_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )

    except Exception as e:
        flash(f'Error al exportar: {str(e)}')
        return redirect(url_for('index'))

# Crear la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
