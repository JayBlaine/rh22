from datetime import datetime
from rh22 import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(32), unique=True, nullable=False)
    def __repr__(self):
        return "hello"
        #return f"User('{self.username}', '{self.email}', '{self.image_file}')"

