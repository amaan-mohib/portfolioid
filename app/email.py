from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg=Message(subject, sender=sender, recipients=recipients)
    msg.body=text_body
    msg.html=html_body
    Thread(target=send_async_mail, args=(app, msg)).start()

def send_password_reset_email(user):
    token=user.get_reset_password_token()
    send_email('[Portfolioid] Reset Password',sender=('Portfolioid',app.config['ADMINS'][0]),recipients=[user.email],text_body=render_template('email/reset_password.txt',user=user, token=token),html_body=render_template('email/reset_password.html',user=user,token=token))

def send_portfolio_verification(user, template):
    send_email('[Portfolioid] Template Verfication',sender=('Portfolioid',app.config['ADMINS'][0]), recipients=[user.email], text_body=render_template('email/verification.txt', user=user, template=template), html_body=render_template('email/verification.html', user=user, template=template))

def send_message(name, msg, email):
    send_email('[Portfolioid] Contact', sender=('Portfolioid',app.config['ADMINS'][0]), recipients=['amaan.mohib@gmail.com'],
    text_body=render_template('email/message.txt', name=name, email=email,msg=msg), html_body=render_template('email/message.html', name=name, email=email,msg=msg))