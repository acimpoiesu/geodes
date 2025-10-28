# Geodes
# Softdev 2025
# p00

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def disp_homepage():
    return render_template('homepage.html')

@app.route("/login")
def disp_login():
    return render_template('login.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
