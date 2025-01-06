from flask import render_template
from app import app


@app.route("/shop")
def shop():
    return render_template("shop.html", current_page="shop")
