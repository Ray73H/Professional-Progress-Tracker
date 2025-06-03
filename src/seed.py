from src.database import db
from sqlalchemy import text
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed_example_data():
    db.drop_all()
    db.create_all()

    # --- Insert Users ---
    db.session.execute(text("""
        INSERT INTO users (username, password_hash, created_at)
        VALUES 
        (:u1, :pw1, :now),
        (:u2, :pw2, :now)
    """), {
        "u1": "demo",
        "pw1": generate_password_hash("password"),
        "u2": "alice",
        "pw2": generate_password_hash("alicepass"),
        "now": datetime.utcnow()
    })

    # Get user IDs
    users = db.session.execute(text("SELECT id, username FROM users")).fetchall()
    user_map = {user.username: user.id for user in users}

    # --- Insert Jobs ---
    db.session.execute(text("""
        INSERT INTO jobs (name, position, description, created_at, user_id)
        VALUES
        ('Full Stack Developer Intern', 'Intern', 'Track your internship work here.', :now, :uid1),
        ('Product Manager', 'PM', 'Oversee sprint progress.', :now, :uid2)
    """), {
        "now": datetime.utcnow(),
        "uid1": user_map["demo"],
        "uid2": user_map["alice"]
    })

    # Get job IDs
    jobs = db.session.execute(text("SELECT id, name FROM jobs")).fetchall()
    job_map = {job.name: job.id for job in jobs}

    # --- Insert Projects ---
    db.session.execute(text("""
        INSERT INTO projects (name, description, created_at, job_id)
        VALUES
        ('Build Authentication System', 'Implement Flask-based login system.', :now, :jid1),
        ('API Redesign', 'Refactor REST endpoints for clarity.', :now, :jid1),
        ('Customer Feedback Portal', 'Build form to collect feedback.', :now, :jid2)
    """), {
        "now": datetime.utcnow(),
        "jid1": job_map["Full Stack Developer Intern"],
        "jid2": job_map["Product Manager"]
    })

    # Get project IDs
    projects = db.session.execute(text("SELECT id, name FROM projects")).fetchall()
    project_map = {project.name: project.id for project in projects}

    # --- Insert Tasks ---
    db.session.execute(text("""
        INSERT INTO tasks (name, description, status, due_date, created_at, project_id)
        VALUES
        ('Design Login UI', 'Use Bootstrap 5 to build login page.', 'completed', :due1, :now, :pid1),
        ('Integrate OAuth', 'Add Google login support.', 'in_progress', :due2, :now, :pid1),
        ('Refactor Routes', 'Split API routes by module.', 'pending', :due3, :now, :pid2),
        ('Write Feedback Docs', 'Draft how-to guide for the portal.', 'pending', :due4, :now, :pid3)
    """), {
        "now": datetime.utcnow(),
        "due1": datetime.utcnow() + timedelta(days=3),
        "due2": datetime.utcnow() + timedelta(days=7),
        "due3": datetime.utcnow() + timedelta(days=5),
        "due4": datetime.utcnow() + timedelta(days=10),
        "pid1": project_map["Build Authentication System"],
        "pid2": project_map["API Redesign"],
        "pid3": project_map["Customer Feedback Portal"]
    })

    db.session.commit()
    print("Seed data loaded successfully.")

