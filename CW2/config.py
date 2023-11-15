import os
# Enable the CSRF protection
WTF_CSRF_ENABLED = True
# Secret key for signing the data
SECRET_KEY='No the secret key is not "password"'
# Get the folder where this database lives
basedir = os.path.abspath(os.path.dirname(__file__))
# Database file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# Turn on the query tracking
SQLALCHEMY_TRACK_MODIFICATIONS =  True