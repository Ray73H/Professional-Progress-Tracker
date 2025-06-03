from src.database import db
from src.models.models import User, Job, Project
from werkzeug.security import generate_password_hash

def seed_example_data():
    if User.query.first():
        return

    user = User(username="demo", password_hash=generate_password_hash("password"))
    db.session.add(user)
    db.session.commit()

    job = Job(title="Demo Job", user_id=user.id)
    db.session.add(job)
    db.session.commit()

    project = Project(name="Demo Project", description="Seeded data", job_id=job.id)
    db.session.add(project)
    db.session.commit()

    print("✅ Seed data loaded")
