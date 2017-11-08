import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# instantiate the db
db = SQLAlchemy()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from app.user_interface.views import user_interface_blueprint
    app.register_blueprint(user_interface_blueprint)

    return app