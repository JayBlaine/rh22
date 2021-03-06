from sys import stderr
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user, current_user
from flask_mail import Message
from rh22 import app, bcrypt, db, mail

from rh22.forms import UpdateAccountForm, LoginForm, RegistrationForm, ResetPasswordForm, RequestResetForm, ResetHistoryForm, StartForm
from rh22.models import User
from rh22.utils import MissingEmbeddedVideoException, get_embedded_video_url
from mal import Anime

current_anime_id = 0


@app.route("/")
@app.route("/about")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You\'re now able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form1 = UpdateAccountForm()
    form2 = ResetHistoryForm()
    if form1.validate_on_submit() and form1.submit.data:
        current_user.email = form1.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    if form2.validate_on_submit() and form2.reset.data:
        current_user.history = None
        db.session.commit()
        flash('Your history has been cleared', 'success')
        return redirect(url_for('account'))
    if request.method == 'GET':
        form1.email.data = current_user.email
        history_dirty = current_user.history
        history2 = []
        if isinstance(history_dirty, str):  # tokenize history
            history1 = history_dirty.split(',')
            for i in history1:
                history2.append(i.split('-'))
    return render_template('account.html', title='Account', form1=form1, form2=form2, history=history2)


@app.route("/start", methods=['GET', 'POST'])
def start():
    form = StartForm()
    if current_user.is_authenticated and isinstance(current_user.history, str):
        return redirect(url_for('discover'))
    elif form.validate_on_submit():
        genres = []
        for field in form:
            if field.name == discover:
                break
            if field.data:
                genres.append(field.name)
        print(genres)
        return redirect(url_for('discover'))

    return render_template('start.html', title='Get Started', form=form, methods=['GET', 'POST'])


@app.route("/discover", methods=['GET', 'POST'])
def discover():
    global current_anime_id
    if request.method == 'POST':
        # Add to user history
        user = User.query.filter_by(email=current_user.email).first()
        print(user.get_history())
        previous_rating = request.form['rating']
        user.add_history(current_anime_id, previous_rating)
    while (True):
        # TODO: get next anime ID from the surprise model
        current_anime_id += 1
        try:
            video_url = get_embedded_video_url(current_anime_id)
            break
        except MissingEmbeddedVideoException:
            print(
                f'Could not get embedded video for {current_anime_id}, skipping it', file=stderr)
    anime = Anime(current_anime_id)
    anime_title = anime.title
    anime_synopsis = anime.synopsis
    return render_template('discover.html', title='Discover', methods=['GET', 'POST'], video_url=video_url, anime_title=anime_title, anime_synopsis=anime_synopsis)


@app.route("/discover/<int:mal_id>")
def mal_page(mal_id):
    anime = Anime.query.get_or_404(mal_id)
    return render_template('discover.html', title=anime.title, anime=anime)


def send_reset_email(user: User):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


'''
@app.route("/<int:anime_id>")
def anime(anime_id):
    anime_info = get_anime(anime_id)
    return render_template('anime.html', anime_info=anime_info)

@app.route("/<int:account_id>")
def account(account_id):
    account_info = get_account(account_id)
    return render_template('account.html', account_info=account_info)
'''
