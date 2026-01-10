from flask import Blueprint, request
from src.models.models import User, Dji_Part, db
from http import HTTPStatus
from flask_jwt_extended import jwt_required

app = Blueprint("Update", __name__, url_prefix="/update_controllers")


@app.route("/update_users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    ALLOWED_FIELDS = {"username"}

    NOT_ALLOWED_FIELDS = set(data.keys()) - ALLOWED_FIELDS

    if NOT_ALLOWED_FIELDS:
        return {
            "error": "Not allowed fields in request",
            "Not allowed fields": list(NOT_ALLOWED_FIELDS)
            }, HTTPStatus.BAD_REQUEST

    for field in ALLOWED_FIELDS:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()

    return {"message": "User updated"}, HTTPStatus.OK


@app.route("/update_itens/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = db.get_or_404(Dji_Part, item_id)
    data = request.json

    ALLOWED_FIELDS = {'dji_part_number', 'quantity', 'author_id', 'name'}

    NOT_ALLOWED_FIELDS = set(data.keys()) - ALLOWED_FIELDS

    if NOT_ALLOWED_FIELDS:
        return {
            "error": "Not allowed fields in request",
            "Not allowed fields": list(NOT_ALLOWED_FIELDS)
        }, HTTPStatus.BAD_REQUEST

    for field in ALLOWED_FIELDS:
        if field in data:
            setattr(item, field, data[field])
    db.session.commit()

    return {"message": "Item updated"}, HTTPStatus.OK
