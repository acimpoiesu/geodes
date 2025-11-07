# Geodes
# Softdev 2025
# p00

from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB_FILE = "blog.db"

#made into function for readability
def setup_database():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            password TEXT, 
            blog_title TEXT, 
            session_key TEXT, 
            login_token TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT, 
            post_title TEXT, 
            post_text TEXT, 
            timestamp TEXT
        );
    """)
    
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone(): 
        c.execute("INSERT INTO users (username, password, blog_title) VALUES (?, ?, ?)", #put secure placeholder so no injection
                  ('admin', 'geodes1234', 'Admin Blog'))
    
    db.commit()
    db.close()
setup_database()


@app.route("/")
def disp_homepage():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    posts = c.execute("SELECT * FROM posts ORDER BY timestamp DESC LIMIT 5").fetchall()
    #limiting to 5 posts so no clutter
    db.close()
    return render_template('homepage.html', posts=posts)

@app.route("/login", methods=["GET", "POST"])
def disp_login():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        username = request.form["username"]
        password_form = request.form["password"]
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()
        db.close()
        if user_data:
            passworddb = user_data[0]
            if password_form == passworddb:
                session["username"] = username
                return redirect(url_for('disp_homepage'))
            else:
                flash("Incorrect password. Try again.")
        else:
            flash("Username incorrect or not found. Try again.")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/createaccount", methods = ['GET', "POST"])
def set_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_exists = c.fetchone()
        if user_exists:
            db.close()
            flash("Username already taken!")
            return redirect(url_for('create_account'))
        c.execute("INSERT INTO users (username, password, blog_title) VALUES (?, ?, ?)",
        (username, password, f"{username}'s Blog"))
        session['username'] = username
        return redirect(url_for('disp_homepage'))
    return render_template('createaccount.html')
    

    for password in userinfo:
        if password == password:
            session["username"] = username
            session["password"] = password
    c.close()
    return render_template('homepage.html')

@app.route("/logout")
def disp_logout():
    session.pop('username', None)
    return render_template('logout.html')

@app.route("/createpost", methods = ["'GET',POST"])
def creating():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        owner = session['username']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("INSERT INTO posts (owner, post_title, post_text, timestamp) VALUES (?, ?, ?, ?)",(owner, title, content, timestamp))
        db.commit()
        db.close()
        return redirect(url_for('blog'))
    return render_template('createpost.html')

@app.route("/profile")
def disp_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    posts = c.execute("SELECT * FROM posts WHERE owner = ? ORDER BY timestamp DESC", (username,)).fetchall()
    db.close()
    return render_template('profile.html', username=username, posts=posts)

if __name__ == "__main__":
    app.debug = True
    app.run()