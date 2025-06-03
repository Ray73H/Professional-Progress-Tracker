from src.database import db
from src.models.models import Job, Project, Task
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

def get_job(job_id: int, user_id: int) -> Optional[Job]:
    """Get a specific job for a user."""
    return Job.query.filter_by(id=job_id, user_id=user_id).first()

def get_jobs(user_id: int) -> List[Job]:
    """Get all jobs for a user."""
    return Job.query.filter_by(user_id=user_id).all()

def create_job(name: str, description: str, position: str, user_id: int) -> Job:
    """Create a new job."""
    job = Job(
        name=name,
        description=description,
        position=position,
        user_id=user_id
    )
    db.session.add(job)
    db.session.commit()
    return job

def delete_job(job_id: int, user_id: int) -> bool:
    """Delete a job and all its related projects and tasks."""
    job = get_job(job_id, user_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        return True
    return False

def get_project(project_id: int, user_id: int) -> Optional[Project]:
    """Get a specific project."""
    return Project.query.join(Job).filter(
        Project.id == project_id,
        Job.user_id == user_id
    ).first()

def get_projects(job_id: int) -> List[Project]:
    """Get all projects for a job."""
    return Project.query.filter_by(job_id=job_id).all()

def create_project(job_id: int, name: str, description: str) -> Project:
    """Create a new project."""
    project = Project(
        name=name,
        description=description,
        job_id=job_id
    )
    db.session.add(project)
    db.session.commit()
    return project

def delete_project(project_id: int, user_id: int) -> bool:
    """Delete a project and all its tasks."""
    project = get_project(project_id, user_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return True
    return False

def get_task(task_id: int, user_id: int) -> Optional[Task]:
    """Get a specific task."""
    return Task.query.join(Project).join(Job).filter(
        Task.id == task_id,
        Job.user_id == user_id
    ).first()

def get_tasks(project_id: int) -> List[Task]:
    """Get all tasks for a project."""
    return Task.query.filter_by(project_id=project_id).all()

def create_task(project_id: int, name: str, description: str) -> Task:
    """Create a new task."""
    task = Task(
        name=name,
        description=description,
        project_id=project_id
    )
    db.session.add(task)
    db.session.commit()
    return task

def delete_task(task_id: int, user_id: int) -> bool:
    """Delete a task."""
    task = get_task(task_id, user_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return True
    return False 