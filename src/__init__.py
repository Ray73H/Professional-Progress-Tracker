import psycopg2
import os
from flask import Flask
from src.routes.jobs import jobs_bp
from src.routes.projects import projects_bp
from src.routes.tasks import tasks_bp
from src.models.models import User
from flask_login import LoginManager
from views import views
from auth import auth
from database import get_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "devkey123")
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
                    user_record = cur.fetchone()
                    if user_record:
                        uid, uname = user_record
                        return User(id=uid, username=uname)
        except Exception as e:
            print(f"User load error: {e}")
    
    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    
    return app