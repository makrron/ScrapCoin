import json
import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api.controllers import db


def create_app(test_config=None):
    # create and configure the app
    application = Flask(__name__, instance_relative_config=True, template_folder='templates')
    application.config.from_mapping(
        DATABASE="instance/database.db",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_file("config.json", load=json.load)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    db.init_app(application)
    application.config['RATELIMIT_HEADERS_ENABLED'] = True  # To allow the header to be sent

    return application


app = create_app()
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "50 per hour"],
    storage_uri="memory://",
)