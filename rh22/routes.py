import sqlite3
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user, current_user

from rh22 import app, bcrypt, db
from werkzeug.exceptions import abort

from rh22.forms import UpdateAccountForm, LoginForm, RegistrationForm
from rh22.models import User


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_account(account_id):
    print('test')
    # conn = get_db_connection()
    # post = conn.execute('SELECT * FROM posts WHERE id = ?',
    #                     (post_id,)).fetchone()
    # account=
    # conn.close()
    # if post is None:
    #     abort(404)
    # return post

def get_anime(anime_id):
    print('test')


@app.route("/")
@app.route("/home")
def home():
    # conn = get_db_connection()
    # posts = conn.execute("SELECT * FROM posts").fetchall()
    # global_recommendations =
    #
    # conn.close()
    return render_template('home.html')#, global_recommendations=global_recommendations)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
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
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
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
