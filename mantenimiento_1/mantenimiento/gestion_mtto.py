from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import io
import pandas as pd
from werkzeug.utils import secure_filename

# Definir la ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "maintenance.db")}'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB máximo por archivo

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar la base de datos
db = SQLAlchemy(app)

# Agregar contexto global para templates
@app.context_processor
def inject_year():
    return {'year': datetime.now().year}

# Definir modelos
class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    mantenimientos = db.relationship('Mantenimiento', backref='equipo', lazy=True, cascade="all, delete")

class Mantenimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)

# Función para validar archivos permitidos
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'xls', 'xlsx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    equipos = Equipo.query.all()
    return render_template('index.html', equipos=equipos)

@app.route('/equipos')
def equipos():
    equipos = Equipo.query.all()
    return render_template('equipos.html', equipos=equipos)

@app.route('/agregar_equipo', methods=['POST'])
def agregar_equipo():
    nombre = request.form.get('nombre')
    ubicacion = request.form.get('ubicacion')
    if not nombre or not ubicacion:
        flash('Todos los campos son obligatorios', 'error')
        return redirect(url_for('equipos'))
    equipo = Equipo(nombre=nombre, ubicacion=ubicacion)
    db.session.add(equipo)
    db.session.commit()
    flash('Equipo agregado exitosamente', 'success')
    return redirect(url_for('equipos'))

@app.route('/eliminar_equipo/<int:id>')
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado correctamente', 'success')
    return redirect(url_for('equipos'))

@app.route('/mantenimientos')
def mantenimientos():
    mantenimientos = Mantenimiento.query.all()
    equipos = Equipo.query.all()
    return render_template('mantenimientos.html', mantenimientos=mantenimientos, equipos=equipos)

@app.route('/agregar_mantenimiento', methods=['POST'])
def agregar_mantenimiento():
    try:
        equipo_id = request.form.get('equipo_id')
        fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion', '')
        
        if not equipo_id or not fecha or not tipo:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('mantenimientos'))
        
        mantenimiento = Mantenimiento(equipo_id=equipo_id, fecha=fecha, tipo=tipo, descripcion=descripcion)
        db.session.add(mantenimiento)
        db.session.commit()
        flash('Mantenimiento agregado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al agregar mantenimiento: {str(e)}', 'error')
    return redirect(url_for('mantenimientos'))

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    flash('El archivo no existe', 'danger')
    return redirect(url_for('index'))

@app.route('/export/<int:equipment_id>')
def export_equipment_history(equipment_id):
    try:
        equipment = Equipo.query.get_or_404(equipment_id)
        activities = Mantenimiento.query.filter_by(equipo_id=equipment_id).all()
        
        data = {
            'ID': equipment.id,
            'Nombre del Equipo': equipment.nombre,
            'Ubicación': equipment.ubicacion,
            'Mantenimientos': len(activities)
        }
        
        activities_data = [
            {'Fecha': a.fecha.strftime('%Y-%m-%d'), 'Tipo': a.tipo, 'Descripción': a.descripcion} 
            for a in activities
        ]

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            pd.DataFrame([data]).to_excel(writer, sheet_name='Equipo', index=False)
            if activities_data:
                pd.DataFrame(activities_data).to_excel(writer, sheet_name='Mantenimientos', index=False)
        output.seek(0)
        
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=f'equipo_{equipment.id}_{datetime.now().strftime("%Y%m%d")}.xlsx')
    except Exception as e:
        flash(f'Error al exportar: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)