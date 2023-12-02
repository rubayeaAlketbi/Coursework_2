from app import app,db,login_manager,api
from flask import render_template, flash, redirect,request,jsonify,url_for
from datetime import datetime
from .forms import LoginForm, UserForm, PostForm,UpdateAccountForm,CommentForm
from .models import User, Post, Tag, post_tag, Comment
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource, reqparse, fields, marshal_with
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid
import os
import re



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


@app.route('/register/validate-username', methods=['POST'])
def validate_username():
    data = request.get_json()  # Use this instead of request.form
    username = data['username']
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Username already exists'})
    
    

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
                return redirect('/explore')
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
       
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename:
                # Secure the filename
                profilePicture = secure_filename(file.filename)
                # Generate a unique name for the profile picture
                profileName = str(uuid.uuid1()) + "_" + profilePicture
                # Save the file in the desired folder
                file.save(os.path.join('path_to_save', profileName))
                # Update the user's avatar field with the new file name
                userToEdit.avatar = profileName
            else:
                # Handle case for no file uploaded
                print("No file uploaded")
        else:
            print("No file part in request")
        user = User.query.filter_by(username=userToEdit.username).first()
        email = User.query.filter_by(email=userToEdit.email).first()
        if(user is not None or email is not None):
            # If the user exists, then ask to change username or email
            print("Change username or email")
            return redirect('/explore')
        # If the email and username is unique then update the user
        else:
            print("User does not exist")
            #
            user = User(name=register_form.fname.data +' '+ register_form.lname.data, email=register_form.email.data, username = register_form.username.data, password=register_form.password.data)
            # Add the new user to the database
            db.session.add(user)
        
    return render_template("user_dash.html", user=user, register_form=register_form)

@app.route("/edit_account", methods=['GET', 'POST'])
@login_required
def edit_account():
    
    update_form = UpdateAccountForm()
    current_user_data = User.query.get(current_user.id)
  
    if request.method == 'POST':
        # Check if username or email fields have been filled and are unique
        if update_form.username.data and User.query.filter(User.username == update_form.username.data, User.id != current_user.id).first():
            flash("Username already in use. Please choose another one.", "error")
            return redirect('/edit_account')
        if update_form.email.data and User.query.filter(User.email == update_form.email.data, User.id != current_user.id).first():
            flash("Email already in use. Please choose another one.", "error")
            return redirect('/edit_account')
        print("146")
        # Update username and email if provided
        if update_form.username.data:
            current_user_data.username = update_form.username.data
        if update_form.email.data:
            current_user_data.email = update_form.email.data

        # Update password if old password is correct and new password is provided
        if update_form.old_password.data and update_form.password.data:
            if check_password_hash(current_user_data.password, update_form.old_password.data):
                current_user_data.password = generate_password_hash(update_form.password.data)
            else:
                flash("Old password is incorrect.", "error")
                return redirect('/edit_account')

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect('/dashboard')

    # Pre-populate the form with current user data
    update_form.username.data = current_user_data.username
    update_form.email.data = current_user_data.email
    # Password fields are typically not pre-populated for security reasons

    return render_template("edit_account.html", update_form=update_form, user=current_user_data)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    print("User logged out")
    return redirect('/login')


@app.route('/addPost', methods=['GET', 'POST'])
def add_post():
    post_form = PostForm()
    if(request.method == 'POST'):
        # Get the data from the form
        title = request.form['title']
        # Extract post content and tags from the form
        content = request.form['caption']
        # Check if the title is not duplicate from the same user
        post = Post.query.filter_by(title=title).first()
        if(post is not None):
            print("Post exists, change the title")
            # Post exists, redirect to the login page
            return redirect('/addPost')
        # Find all tags - words that follow a '#'
        tags = set(re.findall(r'#([A-Za-z0-9_]+)', content))
        # Create or find Tag instances for each tag
        tag_instances = []
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            # No need to commit yet, it will happen after adding to post
            tag_instances.append(tag)
    
        # Now, create a new Post instance
        post = Post(title = title,caption=content, author_id=current_user.id)
        db.session.add(post)
    
        # Add each tag to the post
        for tag in tag_instances:
            post.tags.append(tag)
    
        # Commit once to insert everything
        db.session.commit()
        flash('Your post has been created! , Check it out in the explore page')
    print ("Hello")
    return render_template("add_post.html",post_form = post_form)



@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    posts = Post.query.all()
    # Store the users in a dictionary for easy lookup
    userCache = {}
    for post in posts:
        if post.author_id in userCache:
            authorName = userCache[post.author_id]
        else:
            #Fetch the author from the database
            author = User.query.filter_by(id=post.author_id).first()
            # Add the author to the cache
            userCache[post.author_id] = author.name

    return render_template("explore.html", posts = posts, userCache = userCache)



@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    post_author = User.query.filter_by(id=post.author_id).first()
    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_form = CommentForm()
    userCache = {user.id: user.name for user in User.query.all()}

    if request.method == 'POST':
        if request.is_json:  # This checks if it's an AJAX request
            data = request.get_json()
            comment_text = data.get('comment')

            if comment_text:
                new_comment = Comment(
                    text=comment_text,
                    post_id=post_id,
                    author_id=current_user.id,
                    publish_date=datetime.utcnow()
                )
                db.session.add(new_comment)
                db.session.commit()

                response_data = {
                    'text': new_comment.text,
                    'author_name': current_user.name,
                    'publish_date': new_comment.publish_date.isoformat()
                }

                return jsonify(response_data), 201  # Return JSON for AJAX
            else:
                return jsonify({'error': 'Comment text is required'}), 400

        # If not AJAX, it's a regular form submission, handle accordingly
        if comment_form.validate_on_submit():
            new_comment = Comment(
                text=comment_form.text.data,
                post_id=post_id,
                author_id=current_user.id,
                publish_date=datetime.utcnow()
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('post', post_id=post_id))  # Redirect after form submission

    # Regular GET request
    comments_with_authors = db.session.query(Comment, User.name).join(User, User.id == Comment.author_id).filter(Comment.post_id == post_id).all()
    return render_template(
        "post_page.html",
        post=post,
        comments=comments,
        comment_form=comment_form,
        userCache=userCache,
        post_author=post_author,
        comments_with_authors=comments_with_authors
    )
