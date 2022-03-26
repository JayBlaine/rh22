import sqlite3
from flask import Flask, render_template
from rh22 import app
from werkzeug.exceptions import abort

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
def home():
    # conn = get_db_connection()
    # posts = conn.execute("SELECT * FROM posts").fetchall()
    # global_recommendations =
    #
    # conn.close()
    return render_template('home.html')#, global_recommendations=global_recommendations)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/<int:anime_id>")
def anime(anime_id):
    anime_info = get_anime(anime_id)
    return render_template('anime.html', anime_info=anime_info)

@app.route("/<int:account_id>")
def account(account_id):
    account_info = get_account(account_id)
    return render_template('account.html', account_info=account_info)