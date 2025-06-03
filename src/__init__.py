import os
from flask import Flask
from src.database import db
from src.routes.jobs import jobs_bp
from src.routes.projects import projects_bp
from src.routes.tasks import tasks_bp
from src.models.models import User
from flask_login import LoginManager
from .views import views
from .auth import auth
from src.seed import seed_example_data

def create_app():
    app = Flask(__name__)

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'devkey123'
    
    db.init_app(app)

    with app.app_context():
        seed_example_data()
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    
    return app