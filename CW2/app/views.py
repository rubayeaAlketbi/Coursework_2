from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm, RegisterForm

@app.route('/')
def about():
    return render_template("about.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create the login form object
    login_form = LoginForm()
    # Validate the login form on submit
    if(login_form.validate_on_submit()):
        print("Form validated")
        flash('Login requested for user {}, remember_me={}'.format(login_form.email.data, login_form.password.data))
        print("Email: " + login_form.email.data)
        print("Password: " + login_form.password.data)
    return render_template("login.html",login_form = login_form)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/admin')
def admin():
    return render_template("admin_dash.html")