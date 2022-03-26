from datetime import datetime
from rh22 import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(32), unique=True, nullable=False)
    email = db.Column(db.VARCHAR(32), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    history = db.Column(db.VARCHAR(1000))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"

