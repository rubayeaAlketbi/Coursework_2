from app import app,db,login_manager
from flask import render_template, flash, redirect,request
from .forms import LoginForm, UserForm
from .models import User, Post, Comment, Tag, post_tag
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os



@app.route('/')
def home():
    return render_template("about.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserForm()
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
        username = register_form.username.data
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
            user = User(name=fname +' '+ lname, email=email, username = username, password=password)
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


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create the login form object
    login_form = LoginForm()
    if (login_form.validate_on_submit()):
        # Get the data from the form
        username = login_form.username.data
        password = login_form.password.data
        # Using the username and password query the database to see if the user exists
        user = User.query.filter_by(username=username).first()
        if(user is not None and user.verify_password(password)):
            # Log in the user
            login_user(user)
            if(user.username == 'admin'):
                return redirect('/admin')
            else:
                return redirect('/dashboard')
        else:
            return redirect('/login')
    return render_template("login.html",login_form = login_form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def userDash():
    register_form = UserForm()
    user = User.query.filter_by(username=current_user.username).first()
    id = current_user.id
    userToEdit = User.query.get_or_404(id)
    if(request.method == 'POST'):
        userToEdit.name = register_form.fname.data + ' ' + register_form.lname.data
        userToEdit.username = request.form['username']
        userToEdit.email = request.form['email']
        userToEdit.password = request.form['password']
       
        # Grab Image Name 
        profilePicture = secure_filename(userToEdit.avatar.filename)
        # Give each profile picture a unique name
        profileName = str(uuid.uuid1()) + "_" +profilePicture 
        # Save the profile picture in the static folder
        userToEdit.avatar = profileName
        # Check if the username exists in the database
        user = User.query.filter_by(username=userToEdit.username).first()
        email = User.query.filter_by(email=userToEdit.email).first()
        if(user is not None or email is not None):
            # If the user exists, then ask to change username or email
            print("Change username or email")
            return redirect('/dashboard')
        # If the email and username is unique then update the user
        else:
            print("User does not exist")
            #
            user = User(name=register_form.fname.data +' '+ register_form.lname.data, email=register_form.email.data, username = register_form.username.data, password=register_form.password.data)
            # Add the new user to the database
            db.session.add(user)
        
    return render_template("user_dash.html", user=user, register_form=register_form)

@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def editUser():
    id = current_user.id
    register_form = UserForm()
    userToEdit = User.query.get_or_404(id)
    if(register_form.validate_on_submit()):
        userToEdit.name = register_form.fname.data + ' ' + register_form.lname.data
        userToEdit.username = register_form.username.data
        userToEdit.email = register_form.email.data
        userToEdit.password = register_form.password.data
        # Check if the username exists in the database
        user = User.query.filter_by(username=userToEdit.username).first()
        email = User.query.filter_by(email=userToEdit.email).first()
        if(user is not None or email is not None):
            print("Change username or email")
            # User exists, redirect to the login page
            return redirect('/edit/user/<int:id>')
        else:
            print("User does not exist")
            # User does not exist, create a new user
            user = User(name=register_form.fname.data +' '+ register_form.lname.data, email=register_form.email.data, username = register_form.username.data, password=register_form.password.data)
            # Add the new user to the database
            db.session.add(user)
        db.session.commit()
        return redirect('/dashboard')
    return render_template("edit_user.html", user=user, register_form=register_form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    print("User logged out")
    return redirect('/login')