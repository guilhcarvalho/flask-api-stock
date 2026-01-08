from flask import Blueprint, request
from src.models.models import User, Dji_Part, db
from http import HTTPStatus

app = Blueprint('Post', __name__, url_prefix='/post_controllers')


@app.route("/create_users", methods=["POST"])
def _create_user():
    data = request.json
    user = User(username=data["username"])
    if request.method == "POST":
        with db.session.begin():
            db.session.add(user)
            db.session.commit()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return []


@app.route("/register_item", methods=["POST"])
def _register_item():
    data = request.json
    register_item = Dji_Part(
        dji_part_number=data["dji_part_number"],
        name=data["name"],
        quantity=data["quantity"],
        author_id=data["author_id"]
    )
    if request.method == "POST":
        with db.session.begin():
            db.session.add(register_item)
            db.session.commit()
        return {"message": "Registered item!"}, HTTPStatus.CREATED
    else:
        return []
