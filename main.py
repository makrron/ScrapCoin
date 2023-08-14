"""Main file where the application will be started and the initial paths and configurations will be defined."""
import json

from waitress import serve

from api.controllers import routes

with open("instance/config.json", "r") as f:
    config = json.load(f)

app = routes.app

# Start the Flask app using Waitress
serve(app, host=config['HOST'], port=config['PORT'])
