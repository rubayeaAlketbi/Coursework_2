from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models