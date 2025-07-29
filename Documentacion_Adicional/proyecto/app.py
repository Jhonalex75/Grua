from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from celery import Celery
from dotenv import load_dotenv
import os
import uuid
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import json
from functools import wraps
from pathlib import Path
import io
import secrets
import logging
from PIL import Image
from sqlalchemy import event
import mimetypes
import redis
from rq import Queue
import boto3
from botocore.exceptions import ClientError

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración base
BASE_DIR = Path(__file__).resolve().parent
ALLOWED_EXTENSIONS = {
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}
MAX_FILE_SIZES = {
    'pdf': 10 * 1024 * 1024,  # 10MB
    'doc': 5 * 1024 * 1024,   # 5MB
    'docx': 5 * 1024 * 1024,  # 5MB
    'jpg': 2 * 1024 * 1024,   # 2MB
    'jpeg': 2 * 1024 * 1024,  # 2MB
    'png': 2 * 1024 * 1024,   # 2MB
    'xls': 5 * 1024 * 1024,   # 5MB
    'xlsx': 5 * 1024 * 1024   # 5MB
}

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', secrets.token_hex(32)),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///maintenance.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    UPLOAD_FOLDER=os.path.join(BASE_DIR, 'uploads'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID'),
    AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY'),
    AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME'),
    REDIS_URL=os.getenv('REDIS_URL', 'redis://localhost:6379'),
    CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

# Asegurar que la carpeta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Configurar Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Configuración de Redis y RQ
redis_conn = redis.from_url(app.config['REDIS_URL'])
task_queue = Queue(connection=redis_conn)

# Configuración de S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
) if app.config['AWS_ACCESS_KEY_ID'] else None

# Modelos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
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
    next_maintenance_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='active')
    documents = db.relationship('Document', backref='equipment', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime)
    deleted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    activities = db.relationship('Activity', backref='equipment', lazy=True)
    created_by = db.relationship('User', foreign_keys=[created_by_id])
    updated_by = db.relationship('User', foreign_keys=[updated_by_id])
    deleted_by = db.relationship('User', foreign_keys=[deleted_by_id])

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.equipment_name,
            'model': self.model_type,
            'serial_number': self.serial_number,
            'manufacturer': self.manufacturer,
            'location': self.location,
            'department': self.department,
            'status': self.status,
            'maintenance_frequency': self.maintenance_frequency,
            'next_maintenance_date': self.next_maintenance_date.isoformat() if self.next_maintenance_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    activity_type = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    technician = db.Column(db.String(100))
    parts_replaced = db.Column(db.Text)
    cost = db.Column(db.Float)
    status = db.Column(db.String(50))
    observations = db.Column(db.Text)
    documents = db.relationship('Document', backref='activity', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime)
    deleted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_by = db.relationship('User', foreign_keys=[created_by_id])
    updated_by = db.relationship('User', foreign_keys=[updated_by_id])
    deleted_by = db.relationship('User', foreign_keys=[deleted_by_id])

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'equipment_id': self.equipment_id,
            'date': self.date.isoformat(),
            'activity_type': self.activity_type,
            'description': self.description,
            'technician': self.technician,
            'status': self.status,
            'cost': self.cost,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    storage_path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deleted_at = db.Column(db.DateTime)
    deleted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_by = db.relationship('User', foreign_keys=[created_by_id])
    deleted_by = db.relationship('User', foreign_keys=[deleted_by_id])

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat()
        }

# Tareas Celery
@celery.task
def check_maintenance_schedule():
    """Verifica equipos que necesitan mantenimiento y envía notificaciones"""
    equipments = Equipment.query.all()
    for equipment in equipments:
        next_maintenance = equipment.next_maintenance_date
        if next_maintenance and next_maintenance <= datetime.now() + timedelta(days=7):
            # Aquí implementar el envío de notificaciones
            pass

# Decoradores y funciones auxiliares
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('No tienes permiso para acceder a esta página', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_safe_filename(filename):
    """Genera un nombre de archivo seguro y único"""
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"

def upload_file_to_s3(file, filename):
    """Sube un archivo a S3"""
    try:
        s3_client.upload_fileobj(
            file,
            app.config['AWS_BUCKET_NAME'],
            filename,
            ExtraArgs={'ACL': 'private'}
        )
        return f"s3://{app.config['AWS_BUCKET_NAME']}/{filename}"
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise

def process_image(file_path, max_size=(800, 800)):
    """Procesa y optimiza imágenes"""
    try:
        with Image.open(file_path) as img:
            img.thumbnail(max_size)
            img.save(file_path, optimize=True, quality=85)
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise

def export_to_excel(data, filename):
    """Exporta datos a Excel"""
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

# Rutas de autenticación
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']) and user.active:
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rutas principales
@app.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Equipment.query.filter(Equipment.deleted_at.is_(None))
    
    if search:
        query = query.filter(
            db.or_(
                Equipment.equipment_name.ilike(f'%{search}%'),
                Equipment.serial_number.ilike(f'%{search}%'),
                Equipment.model_type.ilike(f'%{search}%')
            )
        )
    
    equipments = query.order_by(Equipment.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('index.html', equipments=equipments, search=search)

# ... (resto de las rutas)

# Manejo de errores
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Crear la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)