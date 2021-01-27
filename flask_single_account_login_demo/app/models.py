from flask_login import UserMixin
from app.extensions import db, login_manager
import random


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    single_account_login_token = db.Column(db.String(64), index=True, default='%064x' % random.getrandbits(255),
                                           comment='用于和session中的token对比')

    def get_id(self):
        return self.single_account_login_token

    @login_manager.user_loader
    def load_user(token):
        return User.query.filter_by(single_account_login_token=token).first()
