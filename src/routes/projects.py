from flask import Blueprint, jsonify, request
from src.database import db
from src.models.models import Project, Job
from flask_login import login_required, current_user

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/api/jobs/<int:job_id>/projects', methods=['GET'])
@login_required
def get_projects(job_id):
    """Get all projects for a specific job"""
    try:
        # Verify the job belongs to the current user
        job = Job.query.filter_by(id=job_id, user_id=current_user.id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404

        projects = Project.query.filter_by(job_id=job_id).all()
        return jsonify([{
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
            'job_id': project.job_id
        } for project in projects]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/api/jobs/<int:job_id>/projects', methods=['POST'])
@login_required
def create_project(job_id):
    """Create a new project"""
    try:
        # Verify the job belongs to the current user
        job = Job.query.filter_by(id=job_id, user_id=current_user.id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404

        data = request.get_json()
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400

        new_project = Project(
            name=data['name'],
            description=data.get('description', ''),
            job_id=job_id
        )

        db.session.add(new_project)
        db.session.commit()

        return jsonify({
            'id': new_project.id,
            'name': new_project.name,
            'description': new_project.description,
            'created_at': new_project.created_at.isoformat(),
            'job_id': new_project.job_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/api/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    """Update an existing project"""
    try:
        # Verify the project belongs to the current user's job
        project = Project.query.join(Job).filter(
            Project.id == project_id,
            Job.user_id == current_user.id
        ).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        data = request.get_json()
        
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']

        db.session.commit()

        return jsonify({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created_at': project.created_at.isoformat(),
            'job_id': project.job_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/api/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    """Delete a project"""
    try:
        # Verify the project belongs to the current user's job
        project = Project.query.join(Job).filter(
            Project.id == project_id,
            Job.user_id == current_user.id
        ).first()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        db.session.delete(project)
        db.session.commit()

        return jsonify({'message': 'Project deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 