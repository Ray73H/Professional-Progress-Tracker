import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import create_app
from src.database import db

def reset_database():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables with the new schema
        db.create_all()
        print("Database has been reset successfully!")

if __name__ == "__main__":
    reset_database() 