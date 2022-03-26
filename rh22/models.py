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
    image_file = db.Column(db.VARCHAR(100), nullable=False, default='default.jpg')
    history = db.Column(db.VARCHAR(1000))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"

class Anime(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(300), nullable=False)
    score = db.Column(db.Float(precision=3.2))
    genre = db.Column(db.VARCHAR(300), nullable=False)
    synopsis = db.Column(db.VARCHAR(1500), nullable=False)

    def __repr__(self) -> str:
        return f"Anime({self.mal_id}, '{self.title}', {self.score}, '{self.genre}', '{self.synopsis}')"