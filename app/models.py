from app import db,login, admin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from time import time
import os
import jwt
from app import app


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),index=True,unique=True)
    password_hash=db.Column(db.String(128))
    admin_role=db.Column(db.Boolean, default=False)
    profile=db.relationship('Profile', backref='user',lazy='dynamic')
    social_links=db.relationship('SocialLinks', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time()+expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id=jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(20),index=True)
    last_name=db.Column(db.String(20))
    img=db.Column(db.String(128))
    about=db.Column(db.Text)
    timestamp=db.Column(db.DateTime, index=True,default=datetime.utcnow)
    temp=db.Column(db.String(20))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Profile {}>'.format(self.first_name)

class PortfolioTemplates(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20), index=True, unique=True)
    thumb=db.Column(db.String(128))

    def __repr__(self):
        return self.name

class SocialLinks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fb=db.Column(db.String(128), index=True)
    insta=db.Column(db.String(128), index=True)
    linkedIn=db.Column(db.String(128), index=True)
    github=db.Column(db.String(128), index=True)
    twitter=db.Column(db.String(128), index=True)
    yt=db.Column(db.String(128), index=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Social Links of id {}>'.format(self.id)

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.username == 'admin':
            return True
        else:
            return False
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


admin.add_views(MyModelView(User, db.session), MyModelView(Profile, db.session),MyModelView(PortfolioTemplates, db.session))
Stpath = os.path.join(os.path.dirname(__file__), 'static')
#PtTemp = os.path.join(os.path.dirname(__file__), 'templates/portfolios')
path=os.path.dirname(__file__)
admin.add_view(FileAdmin(path, '/templates/portfolios', name='Portfolio Templates Files'))
#admin.add_view(FileAdmin(Stpath, '/static/', name='Static Files'))