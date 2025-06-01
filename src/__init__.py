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

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'devkey123'
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY"),
    )
    
    db.init_app(app)
    
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