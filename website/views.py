from flask import Blueprint,render_template,flash,redirect,url_for,session
from flask_login import login_required, logout_user

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/signup')
def signup():
    return render_template('signup.html')

@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/admin-login')
def admin_login():
    return render_template('Alogin.html')

@views.route('/admin-dashboard')
def admin_dashboard():
    return render_template('Admin_Dashboard.html')

@views.route('/homa-page')
def home_page():
    return render_template('homepage.html')

@views.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('email',None)
    session.pop('user',None)
    flash(f'Logged-Out Successfully', category='Success')
    return redirect(url_for('views.index'))

