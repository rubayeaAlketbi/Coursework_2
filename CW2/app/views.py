from app import app, db, login_manager, api
from flask import render_template, flash, redirect, request, jsonify, url_for
from datetime import datetime
from .forms import LoginForm, UserForm, PostForm, UpdateAccountForm, CommentForm, ChangePasswordForm, deleteAccountForm, DeletePostForm, UpdatePostForm, DeletePostForm, DeleteCommentForm
from .models import User, Post, Tag, post_tag, Comment
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid
from sqlalchemy import func
import re


@app.route('/')
def home():
    return render_template("about.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserForm()
    if (register_form.validate_on_submit()):
        fname = register_form.fname.data
        lname = register_form.lname.data
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if (user is not None):
            print("User exists")
            # User exists, redirect to the login page
            return redirect('/login')
        else:
            print("User does not exist")
            # User does not exist, create a new user
            user = User(name=fname + ' ' + lname, email=email,
                        username=username, password=password)
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

    return render_template("register.html", register_form=register_form)


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
        if (user is not None and user.verify_password(password)):
            # Log in the user
            login_user(user)
            if (user.username == 'admin'):
                return redirect('/admin')
            else:
                return redirect('/explore')
        else:
            return redirect('/login')
    return render_template("login.html", login_form=login_form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def userDash():
    user = User.query.filter_by(username=current_user.username).first()
    register_form = UpdateAccountForm()
    password_form = ChangePasswordForm()
    delete_form = deleteAccountForm()
    if 'update' in request.form:
        # Check if username is changed and not unique
        if (register_form.username.data != user.username and
                User.query.filter(User.username == register_form.username.data).first()):
            flash("Username already in use. Please choose another one.", "error")
            return redirect(url_for('userDash'))

        # Check if email is changed and not unique
        if (register_form.email.data != user.email and
                User.query.filter(User.email == register_form.email.data).first()):
            flash("Email already in use. Please choose another one.", "error")
            return redirect(url_for('userDash'))

        # Check if the name is changed
        if register_form.name.data:
            user.name = register_form.name.data

        user.name = register_form.name.data
        user.username = register_form.username.data
        user.email = register_form.email.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('userDash'))

    elif 'delete' in request.form:
        print("Delete")
        if 'delete' in request.form and current_user.username != 'admin':
            if check_password_hash(current_user.passwordHashed, delete_form.confirm_password.data):
                # Delete the comments of the user
                comments = Comment.query.filter_by(
                    author_id=current_user.id).all()
                for comment in comments:
                    db.session.delete(comment)
                    db.session.commit()
                # Delete the posts of the user
                posts = Post.query.filter_by(author_id=current_user.id).all()
                for post in posts:
                    db.session.delete(post)
                    db.session.commit()

                # Delete the user
                db.session.delete(user)
                db.session.commit()
                flash('Your account has been deleted!', 'success')
                return redirect('/login')
            else:
                flash("Password is incorrect.", "error")
                return redirect('/dashboard')
    elif 'change' in request.form:
        # Check if old password is correct
        if not check_password_hash(current_user.passwordHashed, password_form.old_password.data):
            flash('Old password is incorrect.', 'danger')
            return redirect(url_for('userDash'))

        # Ensure new password is different from the old password
        if password_form.old_password.data == password_form.password.data:
            flash('New password must be different from the old password.', 'danger')
            return redirect(url_for('userDash'))

        # Update the user's password
        hashed_password = generate_password_hash(password_form.password.data)
        current_user.passwordHashed = hashed_password  # Use the correct attribute name
        db.session.commit()

        flash('Your password has been updated!', 'success')
        return redirect(url_for('userDash'))

    print(request.form)
    return render_template("user_dash.html", user=user, register_form=register_form, delete_form=delete_form, password_form=password_form)


@app.route('/my_page', methods=['GET', 'POST'])
@login_required
def my_page():
    user = User.query.filter_by(username=current_user.username).first()
    posts = Post.query.filter_by(author_id=current_user.id).all()
    latest_posts = []  # Initialize the variable before the loop
    for _ in posts:
        latest_posts = Post.query.filter_by(author_id=current_user.id).order_by(
            Post.publish_date.desc()).limit(5).all()
    # Return all of the posts of the user except the post with the highest number of comments and the latest posts
    top_three_posts = Post.query \
        .outerjoin(Comment, Post.id == Comment.post_id) \
        .with_entities(Post, func.count(Comment.id).label('comment_count')) \
        .group_by(Post.id) \
        .order_by(func.count(Comment.id).desc()) \
        .limit(3) \
        .all()

    # Display the number of posts and comments of the user
    posts = Post.query.filter_by(author_id=current_user.id).all()
    comments = Comment.query.filter_by(author_id=current_user.id).all()
    post_count = len(posts)
    comment_count = len(comments)

    # Display the number of tags used by the user
    tags = Tag.query.all()
    tag_count = 0
    for tag in tags:
        for post in posts:
            if tag in post.tags:
                tag_count += 1

    return render_template("my_page.html", user=user, posts=posts, latest_posts=latest_posts, remaining_posts=top_three_posts, tag_count=tag_count, post_count=post_count, comment_count=comment_count)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    print("User logged out")
    return redirect('/login')


@app.route('/addPost', methods=['GET', 'POST'])
def add_post():
    post_form = PostForm()
    if (request.method == 'POST'):
        # Get the data from the form
        title = request.form['title']
        # Extract post content and tags from the form
        content = request.form['caption']
        # Check if the title is not duplicate from the same user
        post = Post.query.filter_by(title=title).first()
        if (post is not None):
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
        post = Post(title=title, caption=content, author_id=current_user.id)
        db.session.add(post)

        # Add each tag to the post
        for tag in tag_instances:
            post.tags.append(tag)

        # Commit once to insert everything
        db.session.commit()
        flash('Your post has been created! , Check it out in the explore page ')
    print("Hello")
    return render_template("add_post.html", post_form=post_form)


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    # Store the users in a dictionary for easy lookup
    userCache = {}
    # get the page number from the request
    page = request.args.get('page', 1, type=int)
    # Paginate the posts
    posts = Post.query.order_by(
        Post.publish_date.desc()).paginate(page=page, per_page=4)
    for post in posts.items:
        if post.author_id in userCache:
            authorName = userCache[post.author_id]
        else:
            # Fetch the author from the database
            author = User.query.filter_by(id=post.author_id).first()
            # Add the author to the cache
            userCache[post.author_id] = author.name

    return render_template("explore.html", posts=posts.items, userCache=userCache, paginationPost=posts)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    post_author = User.query.filter_by(id=post.author_id).first()
    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_form = CommentForm()
    delete_post_form = DeletePostForm()
    delete_comment_form = DeleteCommentForm()
    updatePost = UpdatePostForm()
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
            # Redirect after form submission
            return redirect(url_for('post', post_id=post_id))
    current_user_id = current_user.id
    # Regular GET request
    comments_with_authors = db.session.query(Comment, User.name).join(
        User, User.id == Comment.author_id).filter(Comment.post_id == post_id).all()
    return render_template(
        "post_page.html",
        post=post,
        comments=comments,
        comment_form=comment_form,
        userCache=userCache,
        post_author=post_author,
        current_user_id=current_user_id,
        comments_with_authors=comments_with_authors,
        delete_post_form=delete_post_form,
        delete_comment_form=delete_comment_form,
        updatePost=updatePost
    )


@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if (comment.author_id != current_user.id) or (current_user.username == 'admin'):
        flash('You cannot delete this comment.', 'danger')
        return redirect(url_for('explore'))
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Your comment has been deleted!', 'success')
    return redirect(url_for('post', post_id=comment.post_id))


@app.route('/edit_post/<int:post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        flash('You cannot edit this post.', 'danger')
        # Redirect to the homepage or other appropriate page
        return redirect(url_for('index'))

    # Pre-populate the form with the existing post
    post_form = PostForm(obj=post)

    if request.method == "POST":
        # Update the post's title and content
        post.title = post_form.title.data
        post.caption = post_form.caption.data

        # Clear existing tags and add the new ones from the form content
        post.tags.clear()
        tags = set(re.findall(r'#([A-Za-z0-9_]+)', post.caption))
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            post.tags.append(tag)

        # Commit the changes to the database
        db.session.commit()
        flash('Your post has been updated!', 'success')
        # Redirect to the view post page
        return redirect(url_for('post', post_id=post.id))
    return redirect(url_for('post', post_id=post_id))


@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    delete_post_form = DeletePostForm()
    post = Post.query.get_or_404(post_id)
    if (request.method == 'POST' and post.author_id == current_user.id) or (request.method == 'POST' and current_user.username == 'Admin'):
        # Delete all of the comments of the post
        comments = Comment.query.filter_by(post_id=post_id).all()
        for comment in comments:
            db.session.delete(comment)
            db.session.commit()
        # Delete the post
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('my_page'))
    flash('You can only delete your own posts!', 'danger')
    return redirect(url_for('post', post_id=post_id))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.username != "Admin":  # Assuming "admin" is the admin's username
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('explore'))  # Make sure to use return here!

    # The admin views the users and views the number of posts and comments of each user
    users = User.query.filter(User.id != 1).all()
    # Load the delete user form
    delete_user_form = deleteAccountForm()
    # Create dictionaries to hold the post and comment counts for each user
    user_posts_counts = {user.id: Post.query.filter_by(
        author_id=user.id).count() for user in users}
    user_comments_counts = {user.id: Comment.query.filter_by(
        author_id=user.id).count() for user in users}
    return render_template("admin_dash.html", users=users, user_posts_counts=user_posts_counts, user_comments_counts=user_comments_counts, delete_user_form=delete_user_form)


@app.route('/admin/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def deleteUsers(user_id):
    if current_user.id != 1:  # Assuming user with ID 1 is the admin
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('admin'))

    user_to_delete = User.query.get_or_404(user_id)
    # delete all of the posts of the user
    posts = Post.query.filter_by(author_id=user_id).all()
    # Delete all of the comments of the user
    comments = Comment.query.filter_by(author_id=user_id).all()
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    # Delete all of the posts of the user
    posts = Post.query.filter_by(author_id=user_id).all()
    for post in posts:
        db.session.delete(post)
        db.session.commit()
    # Delete the user
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin'))
