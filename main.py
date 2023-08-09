"""Main file where the application will be started and the initial paths and configurations will be defined."""

from waitress import serve

from api.controllers import routes

app = routes.app

# Start the Flask app using Waitress
serve(app, host='0.0.0.0', port=8080)
