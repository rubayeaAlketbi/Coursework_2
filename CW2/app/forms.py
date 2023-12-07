from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, FileField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets import TextArea

''' Login form which takes in the email and the password of the user '''


class LoginForm(FlaskForm):
    username = StringField('Enter your username', validators=[DataRequired()])
    password = PasswordField('Type in your password',
                             validators=[DataRequired()])
    loginButton = SubmitField('Login')


''' Register form which takes in the first name, last name, email, password and confirm password of the user '''


class UserForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=8, max=20), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    profilePicture = FileField('Profile picture')
    registerButton = SubmitField('Register')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username')
    name = StringField('Name')
    email = StringField('Email Address')
    update = SubmitField('Update')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), Length(
        min=8, max=20), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    change = SubmitField('Change Password')


class deleteAccountForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=8, max=20), EqualTo('confirm', message='Passwords must match')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    delete = SubmitField('Delete Account')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    caption = StringField('Write your Limbo', validators=[
                          DataRequired()], widget=TextArea())
    author = StringField('Author', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    postButton = SubmitField('Post')


class CommentForm(FlaskForm):
    text = StringField('Your Comment', validators=[
                       DataRequired()], widget=TextArea())
    commentButton = SubmitField('Comment')


class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    caption = StringField('Write your thoughts', validators=[
                          DataRequired()], widget=TextArea())
    tags = StringField('Tags')
    update = SubmitField('Update')


class DeletePostForm(FlaskForm):
    delete = SubmitField('Delete')


class DeleteCommentForm(FlaskForm):
    delete = SubmitField('Delete')
