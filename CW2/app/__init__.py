from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
admin = Admin(app, name='Admin', template_mode='bootstrap4')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models