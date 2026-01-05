from flask import Flask
import os


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dji_parts_stock.sqlite')
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