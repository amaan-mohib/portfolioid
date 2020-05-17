from flask import Flask, redirect, url_for, flash
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_moment import Moment
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


app = Flask(__name__)

app.config.from_object(Config)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
login=LoginManager(app)
login.login_view='login'
mail=Mail(app)
moment=Moment(app)

class MyIndexView(AdminIndexView):
    def is_accessible(self):
        if  current_user.is_authenticated and current_user.admin_role == True:
            return True
        else:
            return False
    def inaccessible_callback(self,name,**kwargs):
        flash('You can\'t access adminitrative page.')
        return redirect(url_for('login'))

admin=Admin(app, name='Portfolioid', index_view=MyIndexView(), template_mode='bootstrap3')

from app import routes, models, errors

# app.config['MAIL_SERVER']='smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = 'b832d3261c1b64'
# app.config['MAIL_PASSWORD'] = '56442a873595e3'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

# app.config['MAIL_SERVER']='localhost'
# app.config['MAIL_PORT'] = 8025
app.config['TEMP_PER_PAGE']=21
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'amaan.mohib@gmail.com'
app.config['MAIL_PASSWORD'] = '2001Amaan'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth=None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure=None
        if app.config['MAIL_USE_TLS']:
            secure=()
        mail_handler=SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Portdolioid Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/portfolioid.log', maxBytes=10240,
                                            backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Portfolioid startup')