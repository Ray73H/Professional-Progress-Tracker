from flask import Flask, request, redirect, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Create app
app = Flask(__name__)
app.secret_key = 'Mamamonkey9Jacob#11'  

# Function to access the database
def get_db():
    conn = sqlite3.connect('database.db')
    return conn

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': 
        # On a POST request, process the form submission
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = get_db()

        try:
            # Try to insert user into DB if it's a new user
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            return "Username already exists"
        return redirect('/login')

    # On a GET request, simply show the form
    return render_template('signup.html') 

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        # On a POST request, process the form submission
        username = request.form['username']
        password = request.form['password']

        # Lookup the user
        conn = get_db()
        # Fetchone returns a single row
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        # Ensure password matches user, using hashcode
        if user and check_password_hash(user[2], password):
            # Store the session in a cookie
            session['user_id'] = user[0]
            return redirect('/home')

        # On an invalide password
        return "Invalid login"

    # On a GET request, just show the login form
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
