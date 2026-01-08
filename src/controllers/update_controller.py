from flask import Blueprint, request
from sqlalchemy import inspect
from src.models.models import User, Dji_Part, db

app = Blueprint("Update", __name__, url_prefix="/update_controllers")


@app.route("/update_users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    mapper = inspect(User)
    
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    
    return {
        "id": user.id,
        "username": user.username
    }
