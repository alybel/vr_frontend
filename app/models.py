from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


class GeneralSettings(db.Model):
    __tablename__ = 'GeneralSettings'
    email = db.Column(db.String(64), primary_key = True)
    consumer_key = db.Column(db.String(64), unique=False, index = False)
    consumer_secret = db.Column(db.String(64), unique=False, index=False)
    access_token = db.Column(db.String(64), unique=False, index=False)
    access_token_secret = db.Column(db.String(64), unique=False, index=False)
    own_twittername = db.Column(db.String(64), unique=True, index=False)
    max_updates_per_day = db.Column(db.Integer, unique = False, index = False, default = 5)
    status_update_score = db.Column(db.Integer, unique = False, index = False, default = 12)
    follow_score = db.Column(db.Integer, unique = False, index = False, default = 10)
    retweet_score = db.Column(db.Integer, unique = False, index = False, default = 14)
    favorite_score = db.Column(db.Integer, unique = False, index = False, default = 14)
    number_active_favorites = db.Column(db.Integer, unique = False, index = False, default = 384)
    number_active_retweets = db.Column(db.Integer, unique = False, index = False, default = 482)
    number_active_follows = db.Column(db.Integer, unique = False, index = False, default = 1982)
    only_with_url = db.Column(db.Integer, unique = False, index = False, default = 1)
    activated = db.Column(db.Integer, unique = False, index = False, default = 1)


class WhiteList(db.Model):
    __tablename__ = 'WhitelistKeywords'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=False, index = False)
    keyword = db.Column(db.String(64), unique=False, index = False)
    weight = db.Column(db.Integer, unique=False, index = False)

class BlackList(db.Model):
    __tablename__ = 'BlacklistKeywords'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=False, index = False)
    keyword = db.Column(db.String(64), unique=False, index = False)
    weight = db.Column(db.Integer, unique=False, index = False)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
