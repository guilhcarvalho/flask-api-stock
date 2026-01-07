from flask import Flask, Blueprint, request
from src.models.models import User, Dji_Part, db

app = Blueprint('Get', __name__, url_prefix='/get_controllers')


@app.route("/", methods=["GET"])
def list_product(dji_part_number, name, quantity, last_update, author_id):
    return {
        'DJI Part Number': dji_part_number,
        'Name': name,
        'Quantity': quantity,
        'Last update': last_update,
        'Author ID': author_id
    }