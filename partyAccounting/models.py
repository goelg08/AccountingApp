from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from partyAccounting import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    userparty = db.relationship('UserParty', backref='creator', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class UserParty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partyname = db.Column(db.String(100), nullable=False)
    partymob = db.Column(db.Integer,nullable=False)
    partyadddate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    partydesc = db.Column(db.Text, nullable=False)
    partyaddress = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"UserParty('{self.partyname}', '{self.partyadddate}')"



class UserPartyTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    userparty_id = db.Column(db.Integer, nullable=False)
    debit = db.Column(db.Integer,nullable=False, default=0)
    credit = db.Column(db.Integer,nullable=False, default=0)
    balance = db.Column(db.Integer,nullable=False, default=0)
    transactiondesc = db.Column(db.Text, nullable=False)
    transactiondte = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"UserPartyTransaction('{self.debit}', '{self.credit}')"


