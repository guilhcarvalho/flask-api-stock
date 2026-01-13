import os

import click
from flask import Flask, current_app, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from src.models import db

jwt = JWTManager()
bcrypt = Bcrypt()


@click.command("init-db")
def init_db_command():
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(enviroment=os.environ["ENVIROMENT"]):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{enviroment.title()}Config")

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register cli commands
    app.cli.add_command(init_db_command)

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from src.controllers import auth, dji_part, role, user
    """Importação dentro da função, para evitar importação circular"""
    app.register_blueprint(dji_part.app)
    app.register_blueprint(role.app)
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    
 
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app
