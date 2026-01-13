from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.app import bcrypt
from src.models import User, db
from src.services.utils import (InvalidFieldsError, delete_data, requires_role,
                                save_data, update_fields)

app = Blueprint("user", __name__, url_prefix="/users")


@app.route("/first_user", methods=["POST"])
def _first_user():
    data = request.json
    user = User(username=data["username"], password=bcrypt.generate_password_hash(data["password"]), role_id=data["role_id"])
    validation = db.session.query(db.session.query(User).exists()).scalar()
    
    if validation == True:
        return {"msg": "The first role already exists."}, HTTPStatus.FORBIDDEN
    
    save_data(user)

    return {"msg": "User created!"}, HTTPStatus.CREATED


@app.route("/get_users/<int:user_id>")
@jwt_required()
@requires_role("admin")
def _get_user(user_id):
    user = db.get_or_404(User, user_id)
    user_json = {
        "id": user.id,
        "username": user.username,
        "Role": {"role id": user.role_id, "access": user.role.name},
    }
    return {"User Identify id": get_jwt_identity(), "user": user_json}


@app.route("/list_users")
@jwt_required()
@requires_role("admin")
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    users_json = [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "role id": user.role_id,
                "access": user.role.name,
            },
        }
        for user in users
    ]
    return {"User Identify id": get_jwt_identity(), "users": users_json}


@app.route("/create_users", methods=["POST"])
@jwt_required()
@requires_role("admin")
def _create_user():
    data = request.json
    user = User(username=data["username"], password=bcrypt.generate_password_hash(data["password"]), role_id=data["role_id"])

    save_data(user)

    return {"msg": "User created!"}, HTTPStatus.CREATED


@app.route("/update_users/<int:user_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
def _update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    try:
        update_fields(user, data)

    except InvalidFieldsError as e:
        return {
            "error": "Not allowed fields in request",
            "Not allowed fields": list(e.fields),
        }, HTTPStatus.BAD_REQUEST

    return {"msg": "User updated"}, HTTPStatus.OK


@app.route("/delete_users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def _delete_user(user_id):
    user = db.get_or_404(User, user_id)
    delete_data(user)

    return "", HTTPStatus.NO_CONTENT
