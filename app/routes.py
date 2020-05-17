from flask import render_template,flash,redirect,url_for,request
from werkzeug.urls import url_parse
from app import app,db, admin
from app.forms import LoginForm, RegistrationForm, UserForm, ResetPasswordRequestForm, ResetPasswordForm, ContactForm
from flask_login import current_user,login_user,logout_user,login_required
from flask_admin import Admin, AdminIndexView
from app.models import User, Profile, PortfolioTemplates, SocialLinks
from app.email import send_password_reset_email, send_portfolio_verification, send_message
from datetime import datetime
import PIL

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('dashboard'))
        return redirect(next_page)
    return render_template('login.html',title='Log In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        prof=Profile(user=user)
        social=SocialLinks(user=user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    user= User.query.filter(User.username==current_user.username).first()
    prof=user.profile.filter(Profile.user_id==user.id).first()
    available=Profile.query.filter(Profile.user_id==user.id).first()
    portfolio=PortfolioTemplates.query.filter(PortfolioTemplates.name==Profile.temp).first()
    fn=prof.first_name
    ln=prof.last_name
    img=prof.img
    temp=available.temp
    thumb=portfolio.thumb
    if fn and ln:
        name='{} {}'.format(fn,ln)
    else:
        name=None
    return render_template('dashboard.html', user=user,name=name,img=img,temp=temp,thumb=thumb,title='Dashboard')

@app.route('/profile/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    prof=user.profile.filter(Profile.user_id==user.id).first()
    social=user.social_links.filter(SocialLinks.user_id==user.id).first()
    if prof:
        fn=prof.first_name
        ln=prof.last_name
        img=prof.img
        about=prof.about
        if about:
            about=about.split('\n')
        fb={'Facebook':social.fb, 'Instagram':social.insta, 'LinkedIn':social.linkedIn, 'GitHub':social.github, 'Twitter': social.twitter, 'YouTube':social.yt}
        timestamp=prof.timestamp
        if fn or ln:
            name='{} {}'.format(fn,ln)
        else:
            name=None
        return render_template('user.html', user=user,name=name,img=img,about=about,fb=fb,timestamp=timestamp, title=username)
    return render_template('user.html', user=user,title=username)

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form=UserForm()
    user= User.query.filter(User.username==current_user.username).first()
    prof=user.profile.filter(Profile.user_id==user.id).first()
    social=user.social_links.filter(SocialLinks.user_id==user.id).first()
    
    if form.validate_on_submit():
        available=Profile.query.filter(Profile.user_id==user.id).first()
        social_avail=SocialLinks.query.filter(SocialLinks.user_id==user.id).first()
        if prof and social and available.user_id==user.id:
            available.first_name=form.first_name.data
            available.last_name=form.last_name.data
            available.img=form.img.data
            available.about=form.about.data
            available.timestamp=datetime.utcnow()
            social_avail.fb=form.fb.data
            social_avail.insta=form.insta.data
            social_avail.linkedIn=form.linkedIn.data
            social_avail.github=form.github.data
            social_avail.twitter=form.twitter.data
            social_avail.yt=form.yt.data
            db.session.commit()       
        else:
            profile= Profile(first_name=form.first_name.data, last_name=form.last_name.data, img=form.img.data, about=form.about.data, fb=form.social.data, user=user)
            db.session.add(profile)
            db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('user', username=current_user.username))
    elif request.method=='GET':
        user_id=user.profile.filter(Profile.user_id==current_user.id).first()
        s_user_id=user.social_links.filter(SocialLinks.user_id==current_user.id).first()
        if prof:
            form.first_name.data=user_id.first_name
            form.last_name.data=user_id.last_name
            form.img.data=user_id.img
            form.about.data=user_id.about
            form.fb.data=s_user_id.fb
            form.insta.data=s_user_id.insta
            form.linkedIn.data=s_user_id.linkedIn
            form.github.data=s_user_id.github
            form.yt.data=s_user_id.yt
            form.twitter.data=s_user_id.twitter
    if prof:
        img=prof.img
        return render_template('edit_profile.html', title='Edit Profile',img=img, form=form)
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/delete/<username>')
def delete(username):
    user= User.query.filter(User.username==current_user.username).first()
    available=Profile.query.filter(Profile.user_id==user.id).first()
    social_avail=SocialLinks.query.filter(SocialLinks.user_id==user.id).first()
    db.session.delete(user)
    db.session.delete(available)
    db.session.delete(social_avail)
    db.session.commit()
    flash('Sorry to see you leave :(')
    return redirect(url_for('index'))

@app.route('/template')
def template():
    page = request.args.get('page', 1, type=int)
    list_=PortfolioTemplates.query.paginate(page, 21, False)
    next_url = url_for('template', page=list_.next_num) \
        if list_.has_next else None
    prev_url = url_for('template', page=list_.prev_num) \
        if list_.has_prev else None
    first_url=url_for('template', page=1)
    last_url=url_for('template', page=list_.pages)
    names=[portfolio_templates.name for portfolio_templates in list_.items]
    thumbs=[portfolio_templates.thumb for portfolio_templates in list_.items]
    return render_template('template_browser.html',names=names,thumbs=thumbs,zip=zip,len=len, title='Templates', next_url=next_url, prev_url=prev_url
    ,first_url=first_url, last_url=last_url)

@app.route('/set/<template>/<username>')
def set(template, username):
    if current_user.is_authenticated:
        user= User.query.filter(User.username==username).first()
        available=Profile.query.filter(Profile.user_id==user.id).first()
        available.temp=template
        db.session.commit()
        send_portfolio_verification(user, template)
        flash(template+' has been set as your template!')
        return redirect(url_for('dashboard'))
    else:
        flash('You need to be logged in to set a template.')
        return redirect(url_for('login'))


@app.route('/view/<template>')
def view(template):
    user= User.query.filter(User.username=='view').first()
    user_data=Profile.query.filter(Profile.user_id==user.id).first()
    social=user.social_links.filter(SocialLinks.user_id==user.id).first()
    fb={'Facebook':social.fb, 'Instagram':social.insta, 'LinkedIn':social.linkedIn, 'GitHub':social.github, 'Twitter': social.twitter, 'YouTube':social.yt}
    fn=user_data.first_name
    ln=user_data.last_name
    img=user_data.img
    email=user.email
    about=user_data.about
    if about:
        about=about.split('\n')
    if fn or ln:
        name='{} {}'.format(fn,ln)
        initials=fn[:1]+ln[:1]
    else:
        name=user.username
        initials=name
    return render_template('/portfolios/{}/index.html'.format(template), name=name, title=name, img=img,about=about,fb=fb,email=email, initials=initials)

@app.route('/portfolio/<username>')
def portfolio(username):
    user= User.query.filter_by(username=username).first_or_404()
    user_data=Profile.query.filter(Profile.user_id==user.id).first()
    social=user.social_links.filter(SocialLinks.user_id==user.id).first()
    fb={'Facebook':social.fb, 'Instagram':social.insta, 'LinkedIn':social.linkedIn, 'GitHub':social.github, 'Twitter': social.twitter, 'YouTube':social.yt}
    fn=user_data.first_name
    ln=user_data.last_name
    img=user_data.img
    email=user.email
    template=user_data.temp
    about=user_data.about
    if about:
        about=about.split('\n')
    if fn or ln:
        name='{} {}'.format(fn,ln)
        initials=fn[:1]+ln[:1]
    else:
        name=user.username
        initials=name
    return render_template('/portfolios/{}/index.html'.format(template), name=name, title=name, img=img,about=about,fb=fb,email=email, initials=initials)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form=ContactForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user= User.query.filter(User.username==current_user.username).first()
            send_message(name=user.username, msg=form.message.data, email=user.email)
            flash('Your message has been sent.')
            return redirect(url_for('contact'))
        else:
            send_message(name=form.name.data, msg=form.message.data, email=form.email.data)
            flash('Your message has been sent.')
            return redirect(url_for('contact'))
    elif request.method=='GET':
        if current_user.is_authenticated:
            user= User.query.filter(User.username==current_user.username).first()
            form.name.data=user.username
            form.email.data=user.email

    return render_template('contact.html',title="Contact Us", form=form)

@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user=User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))