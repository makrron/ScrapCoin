"""Main file where the application will be started and the initial paths and configurations will be defined."""

from api.controllers import routes
from api.utils import web_scraper  # Import the web_scraper script
from waitress import serve

app = routes.app

# Run the web scraper script here
web_scraper.main()  # Run the web scraper script

# Start the Flask app using Waitress
serve(app, host='0.0.0.0', port=8080)
