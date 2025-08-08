"""
Controlador de Tareas - Maneja la lógica de negocio de las tareas

Este archivo contiene todas las rutas y lógica relacionada con las tareas.
Representa la capa "Controlador" en la arquitectura MVC.
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from models.task import Task
from app import db


def register_routes(app):
    """
    Registra todas las rutas del controlador de tareas en la aplicación Flask
    
    Args:
        app (Flask): Instancia de la aplicación Flask
    """
    
    @app.route('/')
    def index():
        """
        Ruta principal - Redirige a la lista de tareas
        
        Returns:
            Response: Redirección a la lista de tareas
        """
        return redirect(url_for('task_list'))
    
    
    @app.route('/tasks')
    def task_list():
        """
        Muestra la lista de todas las tareas
        
        Query Parameters:
            filter (str): Filtro para mostrar tareas ('all', 'pending', 'completed')
            sort (str): Ordenamiento ('date', 'title', 'created')
        
        Returns:
            str: HTML renderizado con la lista de tareas
        """
     
        filter_type = request.args.get('filter', 'all')
        sort_type = request.args.get('sort', 'created')

        query = Task.query

        if filter_type == 'pending':
            query = query.filter_by(completed=False)
        elif filter_type == 'completed':
            query = query.filter_by(completed=True)

       
        if sort_type == 'date':
            query = query.order_by(Task.due_date.asc())
        elif sort_type == 'title':
            query = query.order_by(Task.title.asc())
        else: 
            query = query.order_by(Task.created_at.desc())

        tasks = query.all()
        return render_template('task_list.html', tasks=tasks)

    
    
    @app.route('/tasks/new', methods=['GET', 'POST'])
    def task_create():
        """
        Crea una nueva tarea
        
        GET: Muestra el formulario de creación
        POST: Procesa los datos del formulario y crea la tarea
        
        Returns:
            str: HTML del formulario o redirección tras crear la tarea
        """
        
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            due_date_str = request.form.get('due_date')
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None

            if not title:
                flash('El título es obligatorio.', 'danger')
                return redirect(url_for('task_create'))

            task = Task(
                title=title,
                description=description,
                due_date=due_date,
                completed=False
            )

            db.session.add(task)
            db.session.commit()
            flash('Tarea creada correctamente.', 'success')
            return redirect(url_for('task_list'))

        return render_template('task_form.html', action='Crear', task=None)
           
    @app.route('/tasks/<int:task_id>')
    def task_detail(task_id):
        """
        Muestra los detalles de una tarea específica
        
        Args:
            task_id (int): ID de la tarea a mostrar
        
        Returns:
            str: HTML con los detalles de la tarea
        """
        pass # TODO: implementar el método
    
    
    @app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
    def task_edit(task_id):
        """
        Edita una tarea existente
        
        Args:
            task_id (int): ID de la tarea a editar
        
        GET: Muestra el formulario de edición con datos actuales
        POST: Procesa los cambios y actualiza la tarea
        
        Returns:
            str: HTML del formulario o redirección tras editar
        """
        if request.method == 'POST':
            pass # TODO: implementar para una solicitud POST
        
        # Mostrar el formulario para editar la tarea
        pass # TODO: implementar para una solicitud GET
    
    
    @app.route('/tasks/<int:task_id>/delete', methods=['POST'])
    def task_delete(task_id):
        """
        Elimina una tarea
        
        Args:
            task_id (int): ID de la tarea a eliminar
        
        Returns:
            Response: Redirección a la lista de tareas
        """
        pass # TODO: implementar el método
    
    
    @app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
    def task_toggle(task_id):
        """
        Cambia el estado de completado de una tarea
        
        Args:
            task_id (int): ID de la tarea a cambiar
        
        Returns:
            Response: Redirección a la lista de tareas
        """
        pass # TODO: implementar el método
    
    
    # Rutas adicionales para versiones futuras
    
    @app.route('/api/tasks', methods=['GET'])
    def api_tasks():
        """
        API endpoint para obtener tareas en formato JSON
        (Para versiones futuras con JavaScript)
        
        Returns:
            json: Lista de tareas en formato JSON
        """
        # TODO: para versiones futuras
        return jsonify({
            'tasks': [],
            'message': 'API en desarrollo - Implementar en versiones futuras'
        })
    
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Maneja errores 404 - Página no encontrada"""
        return render_template('404.html'), 404
    
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores 500 - Error interno del servidor"""
        db.session.rollback()
        return render_template('500.html'), 500

