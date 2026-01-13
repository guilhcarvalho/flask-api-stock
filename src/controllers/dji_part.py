from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.models import Dji_Part, db
from src.services.utils import (InvalidFieldsError, delete_data, requires_role,
                                save_data, update_fields)

app = Blueprint("dji_part", __name__, url_prefix="/dji_parts")


@app.route("/get_itens/<int:item_id>")
@jwt_required()
@requires_role("admin", "client")
def _get_item(item_id):
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


@app.route("/register_item", methods=["POST"])
@jwt_required()
@requires_role("admin")
def _register_item():
    data = request.json
    register_item = Dji_Part(
        dji_part_number=data["dji_part_number"],
        name=data["name"],
        quantity=data["quantity"],
        author_id=data["author_id"],
    )

    save_data(register_item)

    return {"msg": "Registered item!"}, HTTPStatus.CREATED


@app.route("/list_itens")
@jwt_required()
@requires_role("admin", "client")
def _list_itens():
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


@app.route("/update_itens/<int:item_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
def _update_item(item_id):
    item = db.get_or_404(Dji_Part, item_id)
    data = request.json

    try:
        update_fields(item, data)

    except InvalidFieldsError as e:
        return {
            "error": "Not allowed fields in request",
            "Not allowed fields": list(e.fields),
        }, HTTPStatus.BAD_REQUEST

    return {"message": "Item updated"}, HTTPStatus.OK


@app.route("/delete_itens/<int:item_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def _delete_item(item_id):
    item = db.get_or_404(Dji_Part, item_id)
    delete_data(item)

    return "", HTTPStatus.NO_CONTENT
