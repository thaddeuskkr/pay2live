from flask import render_template
from app import app


@app.route("/")
def index():
    return render_template("index.html", current_page="home")


@app.route("/about")
def about():
    return render_template("about.html", current_page="about")


@app.route("/shop")
def shop():
    return render_template("shop.html", current_page="shop")
