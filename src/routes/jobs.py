from flask import Blueprint, jsonify, request
from src.database import db
from src.models.models import Job
from flask_login import login_required, current_user

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/api/jobs', methods=['GET'])
@login_required
def get_jobs():
    """Get all jobs for the current user"""
    try:
        jobs = Job.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': job.id,
            'name': job.name,
            'description': job.description,
            'position': job.position,
            'created_at': job.created_at.isoformat()
        } for job in jobs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# This is an example of one endpoint. Try implementing the POST endpoint yourself!
# Here's the structure you should follow:

@jobs_bp.route('/api/jobs', methods=['POST'])
@login_required
def create_job():
    """Create a new job"""
    # 1. Get data from request
    # 2. Validate the data
    # 3. Create new job
    # 4. Add to database
    # 5. Return response
    data = request.get_json()
    
    if not data.get('name') or not data.get('position'):
        return jsonify({'error': 'Name and position are required'}), 400
    
    new_job = Job(
        name=data['name'],
        description=data.get('description', ''),
        position=data['position'],
        user_id=current_user.id
    )
    
    db.session.add(new_job)
    db.session.commit()
    
    return jsonify({
        'id': new_job.id,
        'name': new_job.name,
        'description': new_job.description,
        'position': new_job.position,
        'created_at': new_job.created_at.isoformat()
    }), 201

@jobs_bp.route('/api/jobs/<int:job_id>', methods=['PUT'])
@login_required
def update_job(job_id):
    """Update an existing job"""
    try:
        job = Job.query.filter_by(id=job_id, user_id=current_user.id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404

        data = request.get_json()
        
        # Update fields if they're provided
        if 'name' in data:
            job.name = data['name']
        if 'description' in data:
            job.description = data['description']
        if 'position' in data:
            job.position = data['position']
        
        db.session.commit()
        
        return jsonify({
            'id': job.id,
            'name': job.name,
            'description': job.description,
            'position': job.position,
            'created_at': job.created_at.isoformat()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/api/jobs/<int:job_id>', methods=['DELETE'])
@login_required
def delete_job(job_id):
    """Delete a job"""
    try:
        job = Job.query.filter_by(id=job_id, user_id=current_user.id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
            
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
