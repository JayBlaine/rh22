from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
#from rh22.forms import RegistrationForm, LoginForm, UpdateAccountForm
from rh22 import app, db, bcrypt


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template("login.html")

