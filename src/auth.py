from flask import Blueprint, request, redirect, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import text
from src.database import db
from src.models.models import User

auth = Blueprint('auth', __name__)

# Signup route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': 
        print("Signup form submitted:", request.form)
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            db.session.execute(
                text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)"),
                {"username": username, "password_hash": password}
            )
            db.session.commit()
            return redirect('/login')
        except Exception as e:
            db.session.rollback()
            print("Signup failed:", str(e))
            return "Error: " + str(e) 
    
    return render_template('signup.html')

# Login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            result = db.session.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username}
            )
            user_row = result.fetchone()
        except Exception as e:
            print("Login failed:", str(e))
            return "Error: " + str(e) 

        if user_row and check_password_hash(user_row.password_hash, password):
            user = db.session.get(User, user_row.id)
            login_user(user)
            return redirect('/')
        else:
            print("Invalid login credentials")
            return render_template('login.html')

    return render_template('login.html')

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')