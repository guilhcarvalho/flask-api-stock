from flask import Blueprint
from src.models.models import User, Dji_Part, db
from flask_jwt_extended import jwt_required

app = Blueprint('Get', __name__, url_prefix='/get_controllers')


@app.route("/list_users")
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [{"id": user.id, "username": user.username} for user in users]


@app.route("/get_user/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username
    }


@app.route("/list_itens")
def list_itens():
    query = db.select(Dji_Part)
    itens = db.session.execute(query).scalars()
    return [
        {
            "Item ID": item.id,
            "DJI Part Number": item.dji_part_number,
            "Quantity": item.quantity,
            "Last update": item.last_update,
            "Author ID": item.author_id,
        }
        for item in itens
    ]


@app.route("/get_item/<int:item_id>")
def get_item(item_id):
    item = db.get_or_404(Dji_Part, item_id)
    return {
        "Item ID": item.id,
        "DJI Part Number": item.dji_part_number,
        "Quantity": item.quantity,
        "Last update": item.last_update,
        "Author ID": item.author_id
    }
