from typing import Any
from flask import render_template, request, redirect
from app import app, users, shop, carts


@app.route("/checkout")
def checkout():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    items = list(shop.find())
    cart = carts.find_one({"user": user["_id"]}) if user else None
    cart_items: list[dict[str, Any]] = []
    if cart:
        for item in cart["items"]:
            item_data = shop.find_one({"_id": item["id"]})
            cart_items.append(
                {
                    "info": item_data,
                    "quantity": item["quantity"],
                }
            )
    subtotal = 0.00
    for item in cart_items:
        subtotal += item["info"]["price"] * item["quantity"]
    return render_template(
        "checkout.html",
        current_page="checkout",
        user=user,
        shop_items=items,
        cart_items=cart_items,
        subtotal=subtotal,
    )
