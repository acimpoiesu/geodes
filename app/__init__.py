# Geodes
# Softdev 2025
# p00

from flask import Flask, render_template, request, session

import sqlite3


app = Flask(__name__)
app.secret_key = "secret"
DB_FILE = "blog.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, blog_title TEXT, session_key TEXT, login_token TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS posts (owner TEXT, post_title TEXT, post_text TEXT, timestamp TEXT);")
if not c.execute("SELECT * FROM users WHERE username = 'admin'") #Always returns false ????:
    c.execute("INSERT INTO users VALUES ('admin', 'geodes1234', 'TEST BLOG', 'session_key', 'token')")

db.commit()
c.close()

errormessage = "Query Failed"

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
    username = request.form["username"]
    password = request.form["password"]
    userinfo = c.execute(f"SELECT password FROM users WHERE username = '{username}';")
    for password in userinfo:
        if password == password:
            session["username"] = username
            session["password"] = password
    c.close()
    return render_template('homepage.html')

@app.route("/logout")
def disp_logout():
    username = session['username']
    session.pop('username', None)
    return render_template('logout.html')

@app.route("/createaccount")
def disp_create_account():
        return render_template("createaccount.html")

@app.route("/error")
def disp_error():
    return render_template("error.html")

@app.route("/creating", methods = ["POST"])
def creating():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        if password == request.form["confirm"]:
            if c.execute(f"SELECT * FROM users WHERE username = '{username}';") == None #Always returns false????:
                errormessage = "Username Taken. Please Retry." #not working html doesnt display
                return render_template('error.html')
            else:
                c.execute(f"INSERT INTO users VALUES ('{username}', '{password}', 'BLOG_TITLE', 'SESSION', 'TOKEN');") #Not sure if this actually adds
                db.commit()
                c.close()
                return render_template('login.html')
    return render_template("createaccount.html")

@app.route("/profile")
def disp_profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

db.close()
