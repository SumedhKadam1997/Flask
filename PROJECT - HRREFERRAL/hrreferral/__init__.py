import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,current_user,logout_user
from flask_admin import Admin


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db, render_as_batch=True)

admin = Admin(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

from hrreferral.users.views import user
from hrreferral.core.views import core
from hrreferral.error_pages.error_handlers import error_pages

app.register_blueprint(user)
app.register_blueprint(core)
app.register_blueprint(error_pages)
