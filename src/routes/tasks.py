from flask import Blueprint, jsonify, request
from src.database import db
from src.models.models import Task, Project, Job
from flask_login import login_required, current_user
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get tasks with optional filtering"""
    try:
        # Get query parameters
        job_id = request.args.get('job_id', type=int)
        project_id = request.args.get('project_id', type=int)
        
        # Base query joining with Job to check user ownership
        query = Task.query.join(Job, (Job.id == Task.job_id) | 
                               (Job.id == Project.job_id) & (Project.id == Task.project_id))\
                         .filter(Job.user_id == current_user.id)

        # Apply filters if provided
        if job_id:
            query = query.filter(Task.job_id == job_id)
        if project_id:
            query = query.filter(Task.project_id == project_id)

        tasks = query.all()
        return jsonify([{
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'created_at': task.created_at.isoformat(),
            'job_id': task.job_id,
            'project_id': task.project_id
        } for task in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        # Verify ownership of job or project
        job_id = data.get('job_id')
        project_id = data.get('project_id')
        
        if not job_id and not project_id:
            return jsonify({'error': 'Either job_id or project_id is required'}), 400

        if job_id:
            job = Job.query.filter_by(id=job_id, user_id=current_user.id).first()
            if not job:
                return jsonify({'error': 'Job not found'}), 404
        
        if project_id:
            project = Project.query.join(Job).filter(
                Project.id == project_id,
                Job.user_id == current_user.id
            ).first()
            if not project:
                return jsonify({'error': 'Project not found'}), 404

        # Parse due_date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return jsonify({'error': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

        new_task = Task(
            name=data['name'],
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            due_date=due_date,
            job_id=job_id,
            project_id=project_id
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'id': new_task.id,
            'name': new_task.name,
            'description': new_task.description,
            'status': new_task.status,
            'due_date': new_task.due_date.isoformat() if new_task.due_date else None,
            'created_at': new_task.created_at.isoformat(),
            'job_id': new_task.job_id,
            'project_id': new_task.project_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update an existing task"""
    try:
        # Verify the task belongs to the current user's job/project
        task = Task.query.join(Job, (Job.id == Task.job_id) | 
                             (Job.id == Project.job_id) & (Project.id == Task.project_id))\
                        .filter(Task.id == task_id, Job.user_id == current_user.id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        data = request.get_json()
        
        if 'name' in data:
            task.name = data['name']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'due_date' in data:
            try:
                task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
            except ValueError:
                return jsonify({'error': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

        db.session.commit()

        return jsonify({
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'created_at': task.created_at.isoformat(),
            'job_id': task.job_id,
            'project_id': task.project_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    try:
        # Verify the task belongs to the current user's job/project
        task = Task.query.join(Job, (Job.id == Task.job_id) | 
                             (Job.id == Project.job_id) & (Project.id == Task.project_id))\
                        .filter(Task.id == task_id, Job.user_id == current_user.id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 