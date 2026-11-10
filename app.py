import math
import re
import secrets
import sqlite3

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe

import config
import routes
import users

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

PAGE_SIZE = 10

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/register")
def register():
    return render_template("register.html", filled={})

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    filled = {"username": username}

    if not re.search("^[a-zA-Z0-9_]{3,16}$", username):
        flash("VIRHE: tunnuksessa tulee olla 3–16 merkkiä (a–z, 0–9, _)")
        return render_template("register.html", filled=filled)
    if len(password1) < 8 or len(password1) > 100:
        flash("VIRHE: salasanassa tulee olla 8–100 merkkiä")
        return render_template("register.html", filled=filled)
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return render_template("register.html", filled=filled)

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return render_template("register.html", filled=filled)

    flash("Tunnus luotu, voit nyt kirjautua sisään")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if not user_id:
        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/login")

    session["user_id"] = user_id
    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    require_login()
    check_csrf()

    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
    return redirect("/")
