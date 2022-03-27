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
        return f"User('{self.email}', '{self.id}')"

    def get_reset_token(self, time_slice=1800) -> str:
        s = Serializer(app.config['SECRET_KEY'], time_slice)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    def add_history(self, anime_id: int, rating: int) -> None:
        # self.history = '3010-5'
        # db.session.commit()
        if not self.__contains__(anime_id):
            self.history = f'{anime_id:5}-{rating:2},' + self.history
            db.session.commit()
        else:
            raise ValueError(f"{anime_id} is already in User's history")

    def get_history(self) -> list[dict[str: str]]:
        history_list = self.history.split(',')
        history = []
        for history_item in history_list:
            anime_id, rating = history_item.split('-')
            history.append({anime_id: rating})
        return history

    def __contains__(self, item):
        for items in self.get_history():
            if str(item) in items.keys():
                return True
        return False

    @staticmethod
    def verify_reset_token(token: str):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
