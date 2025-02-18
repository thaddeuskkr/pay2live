from bson import ObjectId
from flask import render_template, request, redirect
from app import app, users, orders


@app.route("/checkout/<id>")
def checkout_route(id: str):
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    if not user["registered"]:
        return redirect("/register")
    order = orders.find_one({"_id": ObjectId(id)})
    if not order or str(order["user"]) != str(user["_id"]) or order["paid"]:
        return redirect("/shop")
    return render_template(
        "checkout.html",
        current_page="checkout",
        user=user,
        order_id=str(order["_id"]),
        order_items=order["items"],
        subtotal=order["total"],
    )
