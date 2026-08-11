from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
# Secret key is used by Flask to keep session data safe
app.secret_key = 'opes-edge-eec2026-logic-legends-secret'

# Path to the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def get_db():
    """Opens a new database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


# ============================
# PUBLIC ROUTES
# ============================

@app.route('/')
def index():
    """Home page — the premium landing page."""
    return render_template('index.html')


@app.route('/agriculture')
def agriculture():
    """Agriculture module placeholder."""
    return render_template('agriculture.html')


@app.route('/education')
def education():
    """Education module placeholder."""
    return render_template('education.html')


@app.route('/healthcare')
def healthcare():
    """Healthcare module placeholder."""
    return render_template('healthcare.html')


@app.route('/community')
def community():
    """Community Services module placeholder."""
    return render_template('community.html')


@app.route('/energy')
def energy():
    """Energy Management module placeholder."""
    return render_template('energy.html')


@app.route('/water')
def water():
    """Water Management module placeholder."""
    return render_template('water.html')


@app.route('/about')
def about():
    """About page — scrolls to about section on home for now."""
    return render_template('index.html', scroll_to='about')


# ============================
# AUTHENTICATION ROUTES
# ============================

@app.route('/login')
def login():
    """Login page placeholder."""
    return render_template('login.html')


@app.route('/register')
def register():
    """Registration page placeholder."""
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard placeholder."""
    return render_template('dashboard.html')


# ============================
# ERROR HANDLERS
# ============================

@app.errorhandler(404)
def page_not_found(e):
    """Shows a friendly message if a page doesn't exist."""
    return render_template('index.html', scroll_to='home'), 404


# ============================
# RUN THE APP
# ============================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)