from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.database import db

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
    user_jobs = get_jobs();
    return render_template("dashboard.html", jobs=user_jobs)

@views.route('/add_job')
@login_required
def add_job():
    name = request.form.get('name')
    description = request.form.get('description', '')
    position = request.form.get('position')

    if not name or not position:
        flash('Project name and position is required.', 'warning')
    else:
        try:
            create_job(name, description, position)
            flash(f'Job created"!', 'success')
        except Exception as e:
            current_app.logger.error(f"Error adding Job: {e}")
            flash('Failed to add job. An unexpected error occurred.', 'danger')
    
    return redirect(url_for('views.dashboard'))

@views.route('/remove_job/<int:job_id>', methods=['GET'])
@login_required
def remove_job(job_id):
    job = get_job(job_id, current_user.id)
    if not job:
        flash("Job not found or not authorized.", "danger")
        return redirect(url_for('views.dashboard'))

    try:
        delete_job(job_id)
        flash("Job deleted successfully.", "success")
    except Exception as e:
        current_app.logger.error(f"Error deleting job {job_id}: {e}")
        flash("Failed to delete job. Please try again later.", "danger")

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
            flash(f'Project "{name}" added successfully to job "{job.title}"!', 'success')
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
    try:
        delete_project(project_id)
        flash("Project deleted successfully.", "success")
    except Exception as e:
        current_app.logger.error(f"Error deleting project {project_id}: {e}")
        flash("Failed to delete project. Please try again later.", "danger")

    return redirect(url_for('views.view_job', job_id=job_id) or url_for('views.dashboard'))

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

    title = request.form.get('title')
    description = request.form.get('description', '')

    if not title:
        flash('Task title is required.', 'warning')
        return redirect(request.referrer or url_for('views.view_project', project_id=project_id))

    try:
        create_task(project_id, title, description)
        flash(f'Task "{title}" added successfully.', 'success')
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
    try:
        delete_task(task_id)
        flash("Task deleted successfully.", "success")
    except Exception as e:
        current_app.logger.error(f"Error deleting task {task_id}: {e}")
        flash("Failed to delete task. Please try again later.", "danger")

    return redirect(url_for('views.view_project', project_id=project_id) or url_for('views.dashboard'))