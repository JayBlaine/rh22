from datetime import datetime
from rh22 import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR(32), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    history = db.Column(db.VARCHAR(1000))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"

    def get_reset_token(self, time_slice=1800) -> str:
        s = Serializer(app.config['SECRET_KEY'], time_slice)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token: str):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Anime(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(300), nullable=False)
    score = db.Column(db.Float(precision=3.2))
    genre = db.Column(db.VARCHAR(300), nullable=False)
    synopsis = db.Column(db.VARCHAR(1500), nullable=False)

    def __repr__(self) -> str:
        return f"Anime({self.mal_id}, '{self.title}', {self.score}, '{self.genre}', '{self.synopsis}')"
