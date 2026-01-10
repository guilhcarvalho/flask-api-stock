from flask import Blueprint
from src.models.models import User, Dji_Part, db
from http import HTTPStatus
from flask_jwt_extended import jwt_required

app = Blueprint("Delete", __name__, url_prefix="/delete_controllers")


@app.route("/delete_users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT


@app.route("/delete_itens/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = db.get_or_404(Dji_Part, item_id)
    db.session.delete(item)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
