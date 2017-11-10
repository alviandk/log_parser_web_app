import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instantiate the db
db = SQLAlchemy()
# instantiate flask migrate
migrate = Migrate()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.log_parser.views import log_parser_blueprint
    app.register_blueprint(log_parser_blueprint)

    return app
