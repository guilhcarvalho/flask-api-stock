from flask import Flask, Blueprint, request
from src.models.models import User, Dji_Part, db
from http import HTTPStatus

app = Blueprint('Post', __name__, url_prefix='/post_controllers')


def _create_user():
    data = request.json
    user = User(username=data["username"])
    with db.session.begin():
        db.session.add(user)
        db.session.commit()


def _register_item():
    data = request.json
    register_item = Dji_Part(
        dji_part_number=data["dji_part_number"],
        name=data["name"],
        quantity=data["quantity"],
        author_id=data["author_id"]
    )
    with db.session.begin():
        db.session.add(register_item)
        db.session.commit()


@app.route("/create_users", methods=["POST"])
def handle_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED


@app.route("/register_item", methods=["POST"])
def register_item():
    if request.method == "POST":
        _register_item()
        return {"message": "Registered item!"}, HTTPStatus.CREATED