from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import click
import os


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


@click.command('init-db')
def init_db_command():
    global db
    with current_app.app_context():
        db.create_all()
    click.echo('Initialized the database.')


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.path.join('sqlite:///dji_parts_stock.sqlite')
    )

    # Load the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(init_db_command)
    db.init_app(app)

    @app.route("/product/<id>/<dji_part_number>/<name>/<compatibility>/<quantity>", methods=["GET"])
    def list_product(id, dji_part_number, name, compatibility, quantity):
        return {
            'ID': id,
            'DJI Part Number': dji_part_number,
            'Name': name,
            'Compatibility': compatibility,
            'Quantity': quantity
        }

    @app.route("/create_product/<dji_part_number>/<name>/<compatibility>/<quantity>", methods=['GET', 'POST'])
    def create_product(dji_part_number, name, compatibility, quantity):
        return {
            'DJI Part Number': dji_part_number,
            'Name': name,
            'Compatibility': compatibility,
            'Quantity': quantity
        }

    return app
