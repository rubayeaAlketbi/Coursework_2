from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField
from wtforms.validators import DataRequired,Length

''' Login form which takes in the email and the password of the user '''
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired(),Length(min=8,max=20)])
    loginButton = SubmitField('Login')