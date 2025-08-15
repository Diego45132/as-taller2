"""
Aplicación Flask - Punto de entrada principal
Este archivo configura y ejecuta la aplicación Flask siguiendo el patrón MVC
"""

from flask import Flask
from models import db
from config import config
import os
from controllers.task_controller import task_bp,register_routes
# Crear instancia de SQLAlchemy


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
   
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'clave_secreta'

    # Inicializar extensiones
    db.init_app(app)
    
    # Importar modelos para que SQLAlchemy los reconozca
    from models.task import Task
    
    # Registrar blueprints (controladores)
    from controllers.task_controller import register_routes, task_bp
    register_routes(app)
    print(app.url_map)

    print("\n🔗 RUTAS REGISTRADAS:")
    app.register_blueprint(task_bp, url_prefix='')
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} ({', '.join(rule.methods)})")
    
    

    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
    

    return app


if __name__ == '__main__':
    print("Iniciando aplicación To-Do MVC...")
    app = create_app()
    for rule in app.url_map.iter_rules():
     print(f"Endpoint: {rule.endpoint} → Ruta: {rule.rule} → Métodos: {rule.methods}")

    app.run(debug=True)

    
    print("Accede a: http://127.0.0.1:5000")
    print("Modo debug activado - Los cambios se recargarán automáticamente")
    app.run(host='127.0.0.1', port=5000, debug=True)

