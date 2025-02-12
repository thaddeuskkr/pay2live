from bson import ObjectId
from flask import render_template, request, redirect
from app import app, users, orders


@app.route("/checkout/<id>/complete")
def checkout_complete(id: str):
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    order = orders.find_one({"_id": ObjectId(id)})
    if not order or str(order["user"]) != str(user["_id"]):
        return redirect("/shop")
    if not order["paid"]:
        return redirect("/checkout/" + id)
    return render_template(
        "checkout_complete.html",
        current_page="checkout",
        user=user,
        order_id=str(order["_id"]),
        order_items=order["items"],
        subtotal=order["total"],
    )
