from flask import Flask
from src.database import db
from src.routes.jobs import jobs_bp
from src.routes.projects import projects_bp
from src.routes.tasks import tasks_bp
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    
    # Load config from .env file
    app.config.from_object('config')
    
    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(jobs_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    
    return app