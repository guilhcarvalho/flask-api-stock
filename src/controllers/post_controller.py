from flask import Flask, Blueprint
from src.models.models import db

app = Blueprint('Post', __name__, url_prefix='/post_controllers')


@app.route("/", methods=["POST"])
def list_product(id, dji_part_number, name, quantity, last_update, author_id):
    return {
        'ID': id,
        'DJI Part Number': dji_part_number,
        'Name': name,
        'Quantity': quantity,
        'Last update': last_update,
        'Author ID': author_id
    }