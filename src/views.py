from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.database_functions import (
    get_job, get_jobs, create_job, delete_job,
    get_project, get_projects, create_project, delete_project,
    get_task, get_tasks, create_task, delete_task
)

views = Blueprint('views', __name__)

"""
Functions needed:
    get_job
    get_jobs
    create_job
    delete_job

    get_project
    get_projects
    create_project
    delete_project

    get_tasks
    get_task
    create_task
    delete_task
"""

### JOBS
@views.route('/')
@login_required
def dashboard():
    user_jobs = get_jobs(current_user.id)
    return render_template("dashboard.html", jobs=user_jobs)

@views.route('/add_job', methods=['POST'])
@login_required
def add_job():
    name = request.form.get('name')
    description = request.form.get('description', '')
    position = request.form.get('position')

    if not name or not position:
        flash('Project name and position is required.', 'warning')
    else:
        try:
            create_job(name, description, position, current_user.id)
            flash('Job created successfully!', 'success')
        except Exception as e:
            current_app.logger.error(f"Error adding Job: {e}")
            flash('Failed to add job. An unexpected error occurred.', 'danger')
    
    return redirect(url_for('views.dashboard'))

@views.route('/remove_job/<int:job_id>', methods=['GET'])
@login_required
def remove_job(job_id):
    if delete_job(job_id, current_user.id):
        flash("Job deleted successfully.", "success")
    else:
        flash("Job not found or not authorized.", "danger")
    return redirect(url_for('views.dashboard'))

### PROJECTS
@views.route('/job/<int:job_id>')
@login_required
def view_job(job_id):
    job = get_job(job_id, current_user.id)
    if not job:
        flash('Job not found or not authorized.', 'danger')
        return redirect(url_for('views.dashboard'))

    projects = get_projects(job_id)
    return render_template("job.html", job=job, projects=projects)

@views.route('/job/<int:job_id>/add_project', methods=['POST'])
@login_required
def add_project(job_id):
    job = get_job(job_id, current_user.id)
    if not job:
        flash('Job not found or not authorized.', 'danger')
        return redirect(url_for('views.dashboard'))

    name = request.form.get('name')
    description = request.form.get('description', '')

    if not name:
        flash('Project name is required.', 'warning')
    else:
        try:
            create_project(job_id, name, description)
            flash(f'Project "{name}" added successfully to job "{job.name}"!', 'success')
        except Exception as e:
            current_app.logger.error(f"Error adding project to job {job_id}: {e}")
            flash('Failed to add project. An unexpected error occurred.', 'danger')
    
    return redirect(url_for('views.view_job', job_id=job_id))

@views.route('/remove_project/<int:project_id>', methods=['GET'])
@login_required
def remove_project(project_id):
    project = get_project(project_id, current_user.id)
    if not project:
        flash("Project not found or not authorized.", "danger")
        return redirect(request.referrer or url_for('views.dashboard'))

    job_id = project.job_id
    if delete_project(project_id, current_user.id):
        flash("Project deleted successfully.", "success")
    else:
        flash("Failed to delete project. Please try again later.", "danger")

    return redirect(url_for('views.view_job', job_id=job_id))

### TASKS
@views.route('/project/<int:project_id>')
@login_required
def view_project(project_id):
    project = get_project(project_id, current_user.id)
    if not project:
        flash('Project not found or not authorized.', 'danger')
        return redirect(request.referrer or url_for('views.dashboard'))
    
    tasks = get_tasks(project_id)
    return render_template("project.html", project=project, tasks=tasks)

@views.route('/project/<int:project_id>/add_task', methods=['POST'])
@login_required
def add_task(project_id):
    project = get_project(project_id, current_user.id)
    if not project:
        flash('Project not found or not authorized.', 'danger')
        return redirect(request.referrer or url_for('views.dashboard'))

    name = request.form.get('name')
    description = request.form.get('description', '')

    if not name:
        flash('Task Name is required.', 'warning')
        return redirect(url_for('views.view_project', project_id=project_id))

    try:
        create_task(project_id, name, description)
        flash(f'Task "{name}" added successfully.', 'success')
    except Exception as e:
        current_app.logger.error(f"Error adding task to project {project_id}: {e}")
        flash('Failed to add task. An unexpected error occurred.', 'danger')

    return redirect(url_for('views.view_project', project_id=project_id))

@views.route('/remove_task/<int:task_id>', methods=['GET'])
@login_required
def remove_task(task_id):
    task = get_task(task_id, current_user.id)
    if not task:
        flash("Task not found or not authorized.", "danger")
        return redirect(request.referrer or url_for('views.dashboard'))

    project_id = task.project_id
    if delete_task(task_id, current_user.id):
        flash("Task deleted successfully.", "success")
    else:
        flash("Failed to delete task. Please try again later.", "danger")

    return redirect(url_for('views.view_project', project_id=project_id))