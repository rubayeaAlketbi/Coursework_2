from app import db 
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from flask_login import UserMixin


''' User class which has the following important details
    id - unique id for each user
    name - name of the user
    email - email of the user
    passwordHashed - hashed password of the user
    username - username of the user
    biography - biography of the user
    avatar - avatar of the user
    posts - posts of the user
    The user relation has one to many relationship with post relation.
    User can have one or many post but the post can have only one user.
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passwordHashed = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    biography = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(), nullable=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    
    # Prevent password from being accessed
    @property
    def password(self):
        raise AttributeError('password: write-only field , not readable')
    # Generate password hash
    @password.setter
    def password(self, password):
        self.passwordHashed = generate_password_hash(password)
    # Verify password hash
    def verify_password(self, password):
        return check_password_hash(self.passwordHashed, password)

''' Post class for database model which post has id, title, caption, publish_date, author_id. The
    post relation has one to many relationship with comment relation. Post can have one or many
    comments. The comment can have only one post. The post relation has one to many relationship
    with user relation. Post can have one or many users. The user can have only one post.
'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    tags = db.relationship('Tag', secondary='post_tag', backref=db.backref('posts', lazy='dynamic'))
    
''' Tag class which uses tags to categorise posts.'''
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

''' Association table for many to many relationship between post and tag relation.'''
post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

''' Comment class for database model which comment has id, content, timestamp, author_id, post_id.'''
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
