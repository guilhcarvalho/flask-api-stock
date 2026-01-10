from flask import Blueprint, request
from src.models.models import User, Dji_Part, Role, db
from http import HTTPStatus
from flask_jwt_extended import jwt_required

app = Blueprint('Post', __name__, url_prefix='/post_controllers')


@app.route("/create_roles", methods=["POST"])
def _create_role():
    data = request.json
    role = Role(name=data["name"])

    db.session.add(role)
    db.session.commit()

    return {"msg": "Role created!"}, HTTPStatus.CREATED


@app.route("/create_users", methods=["POST"])
def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"]
        )

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created!"}, HTTPStatus.CREATED


@app.route("/register_item", methods=["POST"])
def _register_item():
    data = request.json
    register_item = Dji_Part(
        dji_part_number=data["dji_part_number"],
        name=data["name"],
        quantity=data["quantity"],
        author_id=data["author_id"]
    )

    db.session.add(register_item)
    db.session.commit()

    return {"msg": "Registered item!"}, HTTPStatus.CREATED
