from flask import Blueprint
from src.services.utils import requires_role
from src.models.models import User, Dji_Part, db
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint('Get', __name__, url_prefix='/get_controllers')


@app.route("/list_users")
@jwt_required()
@requires_role("admin")
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    users_json = [{
        "id": user.id,
        "username": user.username,
        "role": {
            "role id": user.role_id,
            "access": user.role.name,
        }
        } for user in users]
    return {"User Identify id": get_jwt_identity(), "users": users_json}


@app.route("/get_user/<int:user_id>")
@jwt_required()
@requires_role("admin")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    user_json = {
        "id": user.id,
        "username": user.username,
        "Role": {
            "role id": user.role_id,
            "access": user.role.name
            }
        }
    return {"User Identify id": get_jwt_identity(), "user": user_json}


@app.route("/list_itens")
@jwt_required()
@requires_role("admin", "client")
def list_itens():
    query = db.select(Dji_Part)
    itens = db.session.execute(query).scalars()
    itens_json = [
        {
            "Item ID": item.id,
            "DJI Part Number": item.dji_part_number,
            "Name": item.name,
            "Quantity": item.quantity,
            "Last update": item.last_update,
            "Author ID": item.author_id,
        }
        for item in itens
    ]
    return {"User Identify id": get_jwt_identity(), "user": itens_json}


@app.route("/get_item/<int:item_id>")
@jwt_required()
@requires_role("admin", "client")
def get_item(item_id):
    item = db.get_or_404(Dji_Part, item_id)
    itens_json = {
            "Item ID": item.id,
            "DJI Part Number": item.dji_part_number,
            "Name": item.name,
            "Quantity": item.quantity,
            "Last update": item.last_update,
            "Author ID": item.author_id,
        }

    return {"User Identify id": get_jwt_identity(), "user": itens_json}
