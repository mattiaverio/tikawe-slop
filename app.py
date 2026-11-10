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

def get_page_count(item_count):
    return max(math.ceil(item_count / PAGE_SIZE), 1)

def read_classes(entries):
    all_classes = routes.get_all_classes()

    classes = []
    for entry in entries:
        if entry:
            if ":" not in entry:
                abort(403)
            class_title, class_value = entry.split(":", 1)
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    return classes

def read_route_form():
    title = request.form["title"]
    if not title.strip() or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description.strip() or len(description) > 2000:
        abort(403)
    length_km = request.form["length_km"]
    if not re.search("^[1-9][0-9]{0,2}$", length_km):
        abort(403)
    classes = read_classes(request.form.getlist("classes"))

    return title, description, int(length_km), classes

def get_own_route(route_id):
    route = routes.get_route(route_id)
    if not route:
        abort(404)
    if route["user_id"] != session["user_id"]:
        abort(403)
    return route

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_count = get_page_count(routes.get_route_count())

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    page_routes = routes.get_routes(page, PAGE_SIZE)
    return render_template("index.html", routes=page_routes,
                           page=page, page_count=page_count)

@app.route("/route/<int:route_id>")
def show_route(route_id):
    route = routes.get_route(route_id)
    if not route:
        abort(404)
    classes = routes.get_classes(route_id)
    comments = routes.get_comments(route_id)
    average_rating = routes.get_average_rating(route_id)
    images = routes.get_images(route_id)
    return render_template("show_route.html", route=route, classes=classes,
                           comments=comments, average_rating=average_rating,
                           images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = routes.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/new_route")
def new_route():
    require_login()
    classes = routes.get_all_classes()
    return render_template("new_route.html", classes=classes)

@app.route("/create_route", methods=["POST"])
def create_route():
    require_login()
    check_csrf()

    title, description, length_km, classes = read_route_form()
    user_id = session["user_id"]

    route_id = routes.add_route(title, description, length_km, user_id, classes)
    flash("Reitti lisätty")
    return redirect("/route/" + str(route_id))

@app.route("/edit_route/<int:route_id>")
def edit_route(route_id):
    require_login()
    route = get_own_route(route_id)

    all_classes = routes.get_all_classes()
    classes = {}
    for class_title in all_classes:
        classes[class_title] = ""
    for entry in routes.get_classes(route_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_route.html", route=route, classes=classes,
                           all_classes=all_classes)

@app.route("/update_route", methods=["POST"])
def update_route():
    require_login()
    check_csrf()

    route_id = request.form["route_id"]
    get_own_route(route_id)

    title, description, length_km, classes = read_route_form()

    routes.update_route(route_id, title, description, length_km, classes)
    flash("Muutokset tallennettu")
    return redirect("/route/" + str(route_id))

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
