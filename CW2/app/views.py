from app import app,db
from flask import render_template, flash, redirect
from .forms import LoginForm, RegisterForm
from .models import User, Post, Comment, Tag, post_tag

@app.route('/')
def about():
    return render_template("about.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create the login form object
    login_form = LoginForm()
    email = None
    password = None

    # Validate the login form on submit
    if(login_form.validate_on_submit()):
        # print("Form validated")
        # flash('Login requested for user {}, remember_me={}'.format(login_form.email.data, login_form.password.data))
        # print("Email: " + login_form.email.data)
        # print("Password: " + login_form.password.data)
        #Get the user name email and password from the form
        email = login_form.email.data
        password = login_form.password.data
        # Reterive the user 
        user = User.query.filter_by(email=email).first()
        # Check if the user exists in the database and the hashed password
        if(user and user.verify_password(password)):
            print("User Logged in")
            return redirect('/admin')
            
        else:
            print("User does not exist or the password is wrong")
            # User does not exist, redirect to the login page
            return redirect('/login')
        
    return render_template("login.html",login_form = login_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if(register_form.validate_on_submit()):
        # print("First Name: " + register_form.fname.data)
        # print("Last Name: " + register_form.lname.data)
        # print("Email: " + register_form.email.data)
        # if(register_form.password.data != register_form.confirm.data):
        #     print("Passwords do not match")
        # print("Password: " + register_form.password.data)
        # print("Confirm Password: " + register_form.confirm.data)
        # Get the data from the form and create a new user
        fname = register_form.fname.data
        lname = register_form.lname.data
        email = register_form.email.data
        password = register_form.password.data
        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if(user is not None):
            print("User exists")
            # User exists, redirect to the login page
            return redirect('/login')
        else:
            print("User does not exist")
            # User does not exist, create a new user
            user = User(name=fname +' '+ lname, email=email, password=password)
            # Add the new user to the database
            db.session.add(user)
            db.session.commit()
            # Set the form variables to empty
            register_form.fname.data = ''
            register_form.lname.data = ''
            register_form.email.data = ''
            register_form.password.data = ''
            register_form.confirm.data = ''
            # Redirect to the login page
            return redirect('/login')

    return render_template("register.html",register_form = register_form)

@app.route('/admin')
def admin():
    return render_template("admin_dash.html")