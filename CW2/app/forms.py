from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired,Length,EqualTo

''' Login form which takes in the email and the password of the user '''
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(),Length(min=8,max=20)])
    loginButton = SubmitField('Login')
    
''' Register form which takes in the first name, last name, email, password and confirm password of the user '''   
class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8,max=20),EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    registerButton = SubmitField('Register')