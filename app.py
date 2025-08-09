"""
Aplicación Flask - Punto de entrada principal
Este archivo configura y ejecuta la aplicación Flask siguiendo el patrón MVC
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

# Crear instancia de SQLAlchemy
db = SQLAlchemy()
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    fecha_vencimiento = db.Column(db.Date, nullable=False)

def create_app(config_name=None):
    """
    Factory function para crear y configurar la aplicación Flask
    
    Args:
        config_name (str): Nombre de la configuración a usar ('development', 'production', etc.)
    
    Returns:
        Flask: Instancia configurada de la aplicación
    """
    app = Flask(__name__)
    
    # Determinar configuración a usar
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Aplicar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Importar modelos para que SQLAlchemy los reconozca
    from models.task import Task
    
    # Registrar blueprints (controladores)
    from controllers.task_controller import register_routes
    register_routes(app)
    
    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    print("Iniciando aplicación To-Do MVC...")
    app = create_app()
    
    print("Accede a: http://127.0.0.1:5000")
    print("Modo debug activado - Los cambios se recargarán automáticamente")
    app.run(host='127.0.0.1', port=5000, debug=True)

