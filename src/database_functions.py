from src.database import db
from src.models.models import Job, Project, Task
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime

def get_job(job_id: int, user_id: int) -> Optional[Job]:
    sql = text("""
        SELECT id, name, description, position, created_at, user_id
        FROM jobs
        WHERE id = :job_id AND user_id = :user_id
    """)
    result = db.session.execute(sql, {"job_id": job_id, "user_id": user_id})
    row = result.fetchone()

    if row:
        return Job(
            id=row[0],
            name=row[1],
            description=row[2],
            position=row[3],
            created_at=row[4],
            user_id=row[5]
        )
    return None

def get_jobs(user_id: int) -> List[Job]:
    sql = text("""
        SELECT id, name, description, position, created_at, user_id
        FROM jobs
        WHERE user_id = :user_id
        ORDER BY created_at DESC
    """)
    result = db.session.execute(sql, {"user_id": user_id})

    return [
        Job(
            id=row[0],
            name=row[1],
            description=row[2],
            position=row[3],
            created_at=row[4],
            user_id=row[5]
        )
        for row in result.fetchall()
    ]

def create_job(name: str, description: str, position: str, user_id: int) -> Job:
    sql = text("""
        INSERT INTO jobs (name, description, position, user_id, created_at)
        VALUES (:name, :description, :position, :user_id, :created_at)
        RETURNING id, name, description, position, user_id, created_at
    """)
    result = db.session.execute(sql, {
        "name": name,
        "description": description,
        "position": position,
        "user_id": user_id,
        "created_at": datetime.utcnow()
    })
    db.session.commit()

    row = result.fetchone()
    return Job(
        id=row[0],
        name=row[1],
        description=row[2],
        position=row[3],
        user_id=row[4],
        created_at=row[5]
    )


def delete_job(job_id: int, user_id: int) -> bool:
    """Delete a job and all its related projects and tasks."""
    # First delete related tasks
    sql_delete_tasks = text("""
        DELETE FROM tasks
        WHERE project_id IN (
            SELECT id FROM projects WHERE job_id = :job_id
        )
    """)
    
    # Then delete related projects
    sql_delete_projects = text("""
        DELETE FROM projects
        WHERE job_id = :job_id
    """)
    
    # Finally delete the job
    sql_delete_job = text("""
        DELETE FROM jobs
        WHERE id = :job_id AND user_id = :user_id
        RETURNING id
    """)
    
    try:
        db.session.execute(sql_delete_tasks, {"job_id": job_id})
        db.session.execute(sql_delete_projects, {"job_id": job_id})
        result = db.session.execute(sql_delete_job, {"job_id": job_id, "user_id": user_id})
        db.session.commit()
        return result.fetchone() is not None
    except:
        db.session.rollback()
        return False

def get_project(project_id: int, user_id: int) -> Optional[Project]:
    sql = text("""
        SELECT p.id, p.name, p.description, p.created_at, p.job_id
        FROM projects p
        JOIN jobs j ON p.job_id = j.id
        WHERE p.id = :project_id AND j.user_id = :user_id
    """)
    result = db.session.execute(sql, {
        "project_id": project_id,
        "user_id": user_id
    })
    row = result.fetchone()

    if row:
        return Project(
            id=row[0],
            name=row[1],
            description=row[2],
            created_at=row[3],
            job_id=row[4]
        )
    return None

def get_projects(job_id: int) -> List[Project]:
    sql = text("""
        SELECT id, name, description, created_at, job_id
        FROM projects
        WHERE job_id = :job_id
        ORDER BY created_at DESC
    """)
    result = db.session.execute(sql, {"job_id": job_id})

    return [
        Project(
            id=row[0],
            name=row[1],
            description=row[2],
            created_at=row[3],
            job_id=row[4]
        )
        for row in result.fetchall()
    ]

def create_project(job_id: int, name: str, description: str) -> Project:
    sql = text("""
        INSERT INTO projects (name, description, job_id, created_at)
        VALUES (:name, :description, :job_id, :created_at)
        RETURNING id, name, description, created_at, job_id
    """)
    result = db.session.execute(sql, {
        "name": name,
        "description": description,
        "job_id": job_id,
        "created_at": datetime.utcnow()
    })
    db.session.commit()
    row = result.fetchone()

    return Project(
        id=row[0],
        name=row[1],
        description=row[2],
        created_at=row[3],
        job_id=row[4]
    )


def delete_project(project_id: int, user_id: int) -> bool:
    # First delete related tasks
    sql_delete_tasks = text("""
        DELETE FROM tasks
        WHERE project_id = :project_id
    """)
    
    # Then delete the project
    sql_delete_project = text("""
        DELETE FROM projects p
        USING jobs j
        WHERE p.id = :project_id 
        AND p.job_id = j.id 
        AND j.user_id = :user_id
        RETURNING p.id
    """)
    
    try:
        db.session.execute(sql_delete_tasks, {"project_id": project_id})
        result = db.session.execute(sql_delete_project, {"project_id": project_id, "user_id": user_id})
        db.session.commit()
        return result.fetchone() is not None
    except:
        db.session.rollback()
        return False

def get_task(task_id: int, user_id: int) -> Optional[Task]:
    sql = text("""
        SELECT t.id, t.name, t.description, t.status, t.due_date, t.created_at, t.project_id
        FROM tasks t
        JOIN projects p ON t.project_id = p.id
        JOIN jobs j ON p.job_id = j.id
        WHERE t.id = :task_id AND j.user_id = :user_id
        LIMIT 1
    """)
    result = db.session.execute(sql, {"task_id": task_id, "user_id": user_id})
    row = result.fetchone()

    if row:
        return Task(
            id=row[0],
            name=row[1],
            description=row[2],
            status=row[3],
            due_date=row[4],
            created_at=row[5],
            project_id=row[6]
        )
    return None

def get_tasks(project_id: int) -> List[Task]:
    sql = text("""
        SELECT id, name, description, status, due_date, created_at, project_id
        FROM tasks
        WHERE project_id = :project_id
        ORDER BY created_at DESC
    """)
    result = db.session.execute(sql, {"project_id": project_id})

    return [
        Task(
            id=row[0],
            name=row[1],
            description=row[2],
            status=row[3],
            due_date=row[4],
            created_at=row[5],
            project_id=row[6]
        )
        for row in result.fetchall()
    ]

def create_task(project_id: int, name: str, description: str) -> Task:
    sql = text("""
        INSERT INTO tasks (name, description, status, due_date, created_at, project_id)
        VALUES (:name, :description, 'pending', NULL, :created_at, :project_id)
        RETURNING id, name, description, status, due_date, created_at, project_id
    """)
    result = db.session.execute(sql, {
        "name": name,
        "description": description,
        "created_at": datetime.utcnow(),
        "project_id": project_id
    })
    db.session.commit()

    row = result.fetchone()
    if row:
        return Task(
            id=row[0],
            name=row[1],
            description=row[2],
            status=row[3],
            due_date=row[4],
            created_at=row[5],
            project_id=row[6]
        )
    return None

def delete_task(task_id: int, user_id: int) -> bool:
    sql = text("""
        DELETE FROM tasks t
        USING projects p, jobs j
        WHERE t.id = :task_id 
        AND t.project_id = p.id 
        AND p.job_id = j.id 
        AND j.user_id = :user_id
        RETURNING t.id
    """)
    
    try:
        result = db.session.execute(sql, {"task_id": task_id, "user_id": user_id})
        db.session.commit()
        return result.fetchone() is not None
    except:
        db.session.rollback()
        return False 