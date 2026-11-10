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

@app.route("/user/<int:user_id>")
@app.route("/user/<int:user_id>/<int:page>")
def show_user(user_id, page=1):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    statistics = users.get_statistics(user_id)
    page_count = get_page_count(statistics["route_count"])

    if page < 1:
        return redirect("/user/" + str(user_id) + "/1")
    if page > page_count:
        return redirect("/user/" + str(user_id) + "/" + str(page_count))

    user_routes = users.get_routes(user_id, page, PAGE_SIZE)
    return render_template("show_user.html", user=user, statistics=statistics,
                           routes=user_routes, page=page, page_count=page_count)

@app.route("/find_route")
def find_route():
    query = request.args.get("query", "")
    if len(query) > 50:
        abort(403)
    page = request.args.get("page", 1, type=int)
    all_classes = routes.get_all_classes()
    classes = read_classes(request.args.getlist("classes"))

    searched = bool(query or classes)
    results = []
    result_count = 0
    page_count = 1
    if searched:
        result_count = routes.get_result_count(query, classes)
        page_count = get_page_count(result_count)
        page = min(max(page, 1), page_count)
        results = routes.find_routes(query, classes, page, PAGE_SIZE)

    selected = [class_title + ":" + class_value for class_title, class_value in classes]
    return render_template("find_route.html", query=query, all_classes=all_classes,
                           selected=selected, searched=searched, results=results,
                           result_count=result_count, page=page, page_count=page_count)

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

@app.route("/remove_route/<int:route_id>", methods=["GET", "POST"])
def remove_route(route_id):
    require_login()
    route = get_own_route(route_id)

    if request.method == "GET":
        return render_template("remove_route.html", route=route)

    check_csrf()
    if "remove" in request.form:
        routes.remove_route(route_id)
        flash("Reitti poistettu")
        return redirect("/")
    return redirect("/route/" + str(route_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    content = request.form["content"]
    if not content.strip() or len(content) > 1000:
        abort(403)
    rating = request.form["rating"]
    if not re.search("^[1-5]$", rating):
        abort(403)
    route_id = request.form["route_id"]
    route = routes.get_route(route_id)
    if not route:
        abort(403)
    user_id = session["user_id"]

    routes.add_comment(route_id, user_id, content, int(rating))
    flash("Kommentti lisätty")
    return redirect("/route/" + str(route_id))

@app.route("/remove_comment", methods=["POST"])
def remove_comment():
    require_login()
    check_csrf()

    comment_id = request.form["comment_id"]
    comment = routes.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    routes.remove_comment(comment_id)
    flash("Kommentti poistettu")
    return redirect("/route/" + str(comment["route_id"]))

@app.route("/images/<int:route_id>")
def edit_images(route_id):
    require_login()
    route = get_own_route(route_id)

    images = routes.get_images(route_id)
    return render_template("images.html", route=route, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    route_id = request.form["route_id"]
    get_own_route(route_id)

    file = request.files["image"]
    if not file.filename.endswith(".png"):
        flash("VIRHE: väärä tiedostomuoto")
        return redirect("/images/" + str(route_id))

    image = file.read()
    if len(image) > 100 * 1024:
        flash("VIRHE: liian suuri kuva")
        return redirect("/images/" + str(route_id))

    routes.add_image(route_id, image)
    flash("Kuva lisätty")
    return redirect("/images/" + str(route_id))

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    route_id = request.form["route_id"]
    get_own_route(route_id)

    for image_id in request.form.getlist("image_id"):
        routes.remove_image(route_id, image_id)

    return redirect("/images/" + str(route_id))

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
