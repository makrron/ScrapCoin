"""Specific driver for the endpoint that returns Bitcoin prices in fiat."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the ScrapCoin API!'})
