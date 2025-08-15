"""
Módulo de modelos - Capa de datos de la aplicación MVC

Este paquete contiene todas las clases de modelo que representan
las entidades de la base de datos usando SQLAlchemy ORM.
"""

# Importar modelos para facilitar el acceso


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Lista de todos los modelos disponibles
__all__ = ['Task']

from models import db  
