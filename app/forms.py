from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Please enter at least an 8-digit password')])
    password2=PasswordField('Repeat Password',validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Register')

    def validate_usesrname(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UserForm(FlaskForm):
    first_name=StringField('First Name *', validators=[DataRequired()])
    last_name=StringField('Last Name')
    img=StringField('Profile picture URL')
    about=TextAreaField('About')
    fb=StringField('Facebook')
    insta=StringField('Instagram')
    linkedIn=StringField('LinkedIn')
    github=StringField('GitHub')
    twitter=StringField('Twitter')
    yt=StringField('YouTube')
    submit=SubmitField('Save')

class ContactForm(FlaskForm):
    name=StringField('Name *', validators=[DataRequired()])
    email=StringField('Email *', validators=[DataRequired(), Email()])
    message=TextAreaField('Message')
    submit=SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(), Email()])
    submit=SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Please enter at least an 8-digit password')])
    password2=PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Reset Password')