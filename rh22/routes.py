import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route("/")
def home():
    # conn = get_db_connection()
    # posts = conn.execute("SELECT * FROM posts").fetchall()
    # global_recommendations =
    # conn.close()
    return render_template('home.html', global_recommendations=global_recommendations)

@app.route("/<int:account_id>")
def account(account_id):
    account_info = get_account(account_id)
    return render_template('account.html', account_info=account_info)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login")
def
