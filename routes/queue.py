from flask import render_template, request
from app import app, users, queue
from config import abbreviations, services
import math
import pymongo


@app.route("/queue")
def queue_route():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    columns_current = 3
    columns_missed = 5

    current_numbers = list(
        queue.find({"status": "current"}, sort=[("_id", pymongo.DESCENDING)])
    )

    waiting_numbers = list(
        queue.find({"status": "waiting"}, sort=[("_id", pymongo.DESCENDING)])
    )

    missed_numbers = list(
        queue.find({"status": "missed"}, sort=[("_id", pymongo.DESCENDING)])
    )

    current_rows = math.ceil(len(current_numbers) / columns_current)
    missed_rows = math.ceil(len(missed_numbers) / columns_missed)
    current_queue_numbers = [
        current_numbers[i * columns_current : (i + 1) * columns_current]
        for i in range(current_rows)
    ]
    missed_queue_numbers = [
        missed_numbers[i * columns_missed : (i + 1) * columns_missed]
        for i in range(missed_rows)
    ]

    services_list: list[dict[str, str]] = []
    for service in services.keys():
        services_list.append({"id": service, "name": services[service]})

    return render_template(
        "queue.html",
        current_page="queue",
        user=user,
        current_queue_numbers=current_queue_numbers[:3],
        missed_queue_numbers=missed_queue_numbers,
        abbreviations=abbreviations,
        services=services_list,
        waiting=(len(waiting_numbers or [])),
    )
