"""Specific driver for the endpoint that returns Bitcoin prices in fiat."""
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db_connection():
    """Connect to the database."""
    conn = sqlite3.connect('api/controllers/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the ScrapCoin API!'})


@app.route('/prices/<pair>', methods=['GET'])
def get_price(pair):
    """
    Returns the current price of a specific trading pair,
    e.g. GET /prices/BTC_USD to get the current price of Bitcoin in US dollars.
    :param pair: The trading pair to be searched.
    :type pair: str
    :return: JSON object with the current price of the given trading pair.
    :rtype: JSON
    """
    conn = get_db_connection()
    if request.method == 'GET':
        cur = conn.execute(f"SELECT * FROM BITCOIN WHERE PAIR LIKE '{pair.upper()}'").fetchall()

        rows = [dict(row) for row in cur]

        if len(rows) == 0:
            return jsonify({'ERROR': 'Invalid pair.'}), 400
        else:
            return jsonify(rows), 200


@app.route('/prices', methods=['GET'])
def get_price_list():
    """
    Allows you to send a list of trading pairs as query parameters to obtain the prices of several pairs in
    a single call, e.g. GET /prices?pairs=BTC_USD,BTC_EUR,ETH_USD
    :return: JSON object with the current prices of the given trading pairs.
    """
    conn = get_db_connection()
    if request.method == 'GET':
        pairs = request.args.get('pairs').split(',')
        pairs = [pair.upper() for pair in pairs]
        pairs = tuple(pairs)
        print(pairs)
        cur = conn.execute(f"SELECT * FROM BITCOIN WHERE PAIR IN {pairs}").fetchall()

        rows = [dict(row) for row in cur]

        if len(rows) == 0:
            return jsonify({'ERROR': 'Invalid pairs.'}), 400
        else:
            return jsonify(rows), 200


@app.route('/exchanges/<exchange_name>/prices', methods=['GET'])
def get_exchange_price_list(exchange_name):
    """
    Returns the prices of all trading pairs available on a specific exchange,
    e.g. GET /exchanges/coinbasepro/prices to get the prices available on Coinbase Pro.
    :param exchange_name: The name of the exchange.
    :return: JSON object with the current prices of the given exchange.
    """
    conn = get_db_connection()
    if request.method == 'GET':
        cur = conn.execute(f"SELECT * FROM BITCOIN WHERE EXCHANGE LIKE '{exchange_name.upper()}'").fetchall()

        rows = [dict(row) for row in cur]

        if len(rows) == 0:
            return jsonify({'ERROR': 'Invalid exchange.'}), 400
        else:
            return jsonify(rows), 200


