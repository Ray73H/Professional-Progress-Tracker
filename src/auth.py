from flask import Blueprint, request, redirect, render_template, session
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.models import User
from database import get_db
import psycopg2

auth = Blueprint('auth', __name__)

# Signup route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                        (username, password)
                    )
                conn.commit()
            return redirect('/login')
        except psycopg2.IntegrityError:
            return "Username already exists"
        except psycopg2.Error as e:
            print(f"Database error during signup: {e}")
            return "Signup failed due to a database issue. Please try again later."
        except Exception as e:
            print(f"Unexpected error during signup: {e}")
            return "An unexpected error occurred during signup. Please try again later."

    return render_template('signup.html')

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_record = None

        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
                    user_record = cur.fetchone()
        except Exception as e:
            print(f"Login DB error: {e}")
            return "Login failed"

        if user_record:
            user_id, uname, stored_hash = user_record
            if check_password_hash(stored_hash, password):
                user = User(id=user_id, username=uname)
                login_user(user)
                return redirect('/')

        return "Invalid credentials"

    return render_template('login.html')

# Logout route
@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')