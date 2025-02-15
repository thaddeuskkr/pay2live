from datetime import datetime
from bson import ObjectId
from flask import render_template, redirect, request
import pymongo
from app import app, users, appointments, queue, shop, carts, orders, tickets

tab_map = {
    "users": "User Management",
    "appointments": "Appointment Management",
    "queue": "Queue Management",
    "shop": "Shop Management",
    "carts": "Cart Management",
    "orders": "Order Management",
    "tickets": "Support Tickets",
}


@app.route("/admin")
def admin():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    if not user["admin"]:
        return redirect("/")

    tab = request.args.get("tab", "users")

    a_users = users.find(sort=[("_id", pymongo.DESCENDING)])
    a_appointments = appointments.find(sort=[("_id", pymongo.DESCENDING)])
    a_queue = queue.find(sort=[("_id", pymongo.DESCENDING)])
    a_shop = shop.find(sort=[("_id", pymongo.DESCENDING)])
    a_carts = carts.find(sort=[("_id", pymongo.DESCENDING)])
    a_orders = orders.find(sort=[("_id", pymongo.DESCENDING)])
    a_tickets = tickets.find(sort=[("_id", pymongo.DESCENDING)])

    return render_template(
        "admin.html",
        current_page="admin",
        tab=tab,
        tab_name=tab_map.get(tab),
        user=user,
        a_users=a_users,
        a_appointments=a_appointments,
        a_queue=a_queue,
        a_shop=a_shop,
        a_carts=a_carts,
        a_orders=a_orders,
        a_tickets=a_tickets,
    )


@app.template_filter("date_from_object_id")
def date_from_object_id_filter(oid_str: ObjectId | str):
    oid_str = str(oid_str)
    # Parse the first 8 hex characters
    timestamp = int(oid_str[:8], 16)
    # Convert the Unix timestamp (seconds) to a datetime object (UTC)
    return datetime.fromtimestamp(timestamp)
