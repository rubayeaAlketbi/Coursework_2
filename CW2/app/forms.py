from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField, FileField, PasswordField, ValidationError
from wtforms.validators import DataRequired,Length,EqualTo
from wtforms.widgets import TextArea

''' Login form which takes in the email and the password of the user '''
class LoginForm(FlaskForm):
    username = StringField('Enter your username', validators=[DataRequired()])
    password = PasswordField('Type in your password', validators=[DataRequired()])
    loginButton = SubmitField('Login')
    
''' Register form which takes in the first name, last name, email, password and confirm password of the user '''   
class UserForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=20)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8,max=20),EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    profilePicture = FileField('Profile picture')
    registerButton = SubmitField('Register')

class Update_AccountForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=20)])
    email = StringField('Email Address', validators=[DataRequired()])
    old_password = PasswordField('Password', validators=[DataRequired(),Length(min=8,max=20),EqualTo('confirm',message='Old Passwords must match')])
    new_password = PasswordField('Password', validators=[DataRequired(),Length(min=8,max=20),EqualTo('confirm',message='New Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    updateButton = SubmitField('Update')
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    caption = StringField('Write your Limbo', validators=[DataRequired()], widget=TextArea())
    author = StringField('Author', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    postButton = SubmitField('Post')