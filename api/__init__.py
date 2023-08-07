from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.config['RATELIMIT_HEADERS_ENABLED'] = True  # To allow the header to be sent
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "50 per hour"],
    storage_uri="memory://",
)

