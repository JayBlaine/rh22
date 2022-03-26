from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

rh22 = Flask(__name__)
rh22.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
rh22.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(rh22)
bcrypt = Bcrypt(rh22)
login_manager = LoginManager(rh22)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#from rh22 import routes
