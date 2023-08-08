"""Main file where the application will be started and the initial paths and configurations will be defined."""

from api.controllers import routes
from waitress import serve

app = routes.app
serve(app, host='0.0.0.0', port=8080)
