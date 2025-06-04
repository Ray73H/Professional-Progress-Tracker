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
        "u2": "demo2",
        "pw2": generate_password_hash("1234"),
        "now": datetime.utcnow()
    })

    users = db.session.execute(text("SELECT id, username FROM users")).fetchall()
    user_map = {user.username: user.id for user in users}

    # --- Insert Jobs ---
    db.session.execute(text("""
        INSERT INTO jobs (name, position, description, created_at, user_id)
        VALUES
        ('Full Stack Developer Intern', 'Intern', 'Track your internship work here.', :now, :uid1),
        ('Backend Developer', 'Intern', 'Focus on server-side features.', :now, :uid1),
        ('Product Manager', 'PM', 'Oversee sprint progress.', :now, :uid2),
        ('UX Research Assistant', 'Intern', 'Support user research initiatives.', :now, :uid2)
    """), {
        "now": datetime.utcnow(),
        "uid1": user_map["demo"],
        "uid2": user_map["demo2"]
    })

    jobs = db.session.execute(text("SELECT id, name FROM jobs")).fetchall()
    job_map = {job.name: job.id for job in jobs}

    # --- Insert Projects ---
    db.session.execute(text("""
        INSERT INTO projects (name, description, created_at, job_id)
        VALUES
        -- demo user
        ('Build Authentication System', 'Implement Flask-based login system.', :now, :jid1),
        ('API Redesign', 'Refactor REST endpoints for clarity.', :now, :jid1),
        ('Database Optimization', 'Improve query performance.', :now, :jid2),
        -- demo2 user
        ('Customer Feedback Portal', 'Build form to collect feedback.', :now, :jid3),
        ('Sprint Planning Dashboard', 'Create tools for PM tracking.', :now, :jid3),
        ('User Interviews', 'Set up interviews with power users.', :now, :jid4)
    """), {
        "now": datetime.utcnow(),
        "jid1": job_map["Full Stack Developer Intern"],
        "jid2": job_map["Backend Developer"],
        "jid3": job_map["Product Manager"],
        "jid4": job_map["UX Research Assistant"]
    })

    projects = db.session.execute(text("SELECT id, name FROM projects")).fetchall()
    project_map = {project.name: project.id for project in projects}

    # --- Insert Tasks ---
    db.session.execute(text("""
        INSERT INTO tasks (name, description, status, due_date, created_at, project_id)
        VALUES
        -- Tasks for demo user
        ('Design Login UI', 'Use Bootstrap 5 to build login page.', 'completed', :due1, :now, :pid1),
        ('Integrate OAuth', 'Add Google login support.', 'in_progress', :due2, :now, :pid1),
        ('Refactor Routes', 'Split API routes by module.', 'pending', :due3, :now, :pid2),
        ('Index Key Tables', 'Add indexes to user/task tables.', 'pending', :due4, :now, :pid3),

        -- Tasks for demo2 user
        ('Write Feedback Docs', 'Draft how-to guide for the portal.', 'pending', :due5, :now, :pid4),
        ('Build Kanban Board', 'Visualize task flow for PMs.', 'in_progress', :due6, :now, :pid5),
        ('Schedule Interviews', 'Coordinate with beta users.', 'completed', :due7, :now, :pid6),
        ('Synthesize Findings', 'Write report on research results.', 'pending', :due8, :now, :pid6)
    """), {
        "now": datetime.utcnow(),
        "due1": datetime.utcnow() + timedelta(days=3),
        "due2": datetime.utcnow() + timedelta(days=7),
        "due3": datetime.utcnow() + timedelta(days=5),
        "due4": datetime.utcnow() + timedelta(days=10),
        "due5": datetime.utcnow() + timedelta(days=4),
        "due6": datetime.utcnow() + timedelta(days=6),
        "due7": datetime.utcnow() + timedelta(days=2),
        "due8": datetime.utcnow() + timedelta(days=9),
        "pid1": project_map["Build Authentication System"],
        "pid2": project_map["API Redesign"],
        "pid3": project_map["Database Optimization"],
        "pid4": project_map["Customer Feedback Portal"],
        "pid5": project_map["Sprint Planning Dashboard"],
        "pid6": project_map["User Interviews"]
    })

    db.session.commit()
    print("Seed data loaded successfully.")
