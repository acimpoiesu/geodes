# Geodes
# Softdev 2025
# p00

from flask import Flask, render_template, request

import sqlite3


app = Flask(__name__)
DB_FILE = "blog.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()


initusertable = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, blog_title TEXT, session_key TEXT, login_token TEXT);"
c.execute(initusertable)
initposttable = "CREATE TABLE IF NOT EXISTS posts (owner TEXT, post_title TEXT, post_text TEXT, timestamp TEXT);"
c.execute(initposttable)
c.execute("INSERT INTO users VALUES ('hi', 'hello', 'wowie', 'salkdgs', 'askjhgdafhg');")

db.commit()

@app.route("/")
def disp_homepage():
    return render_template('homepage.html')

@app.route("/login")
def disp_login():
    return render_template('login.html')

@app.route("/setuser", methods = ["POST"])
def set_user():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    testing = c.execute("SELECT * FROM users WHERE username = 'hi';")
    for row in testing:
        print("WOOHOO")
        break
    return render_template('homepage.html')

@app.route("/logout")
def disp_logout():
    return render_template('logout.html')

@app.route("/profile")
def disp_profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

db.close()
