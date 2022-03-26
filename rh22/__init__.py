from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

PASSWORD = 'password123'
PUBLIC_IP_ADDRESS = '34.121.3.128'
DBNAME = 'rh22'
PROJECT_ID = 'rh22-345316'
INSTANCE_NAME = 'rh22-345316:us-central1:animerh22'

rh22 = Flask(__name__)
rh22.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
rh22.config['SQLALCHEMY_DATABASE_URI'] = f"mysql + mysqldb://animerh22:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
db = SQLAlchemy(rh22)
bcrypt = Bcrypt(rh22)
login_manager = LoginManager(rh22)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#from rh22 import routes
