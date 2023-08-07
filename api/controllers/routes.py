"""Specific driver for the endpoint that returns Bitcoin prices in fiat."""
import os
import sqlite3

from flask import jsonify, request, render_template, send_from_directory, redirect

from api import app, limiter


def get_db_connection():
    """Connect to the database."""
    try:
        conn = sqlite3.connect('api/controllers/database.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(e)
        return None


@app.route('/', methods=['GET'])
@limiter.exempt
def home():
    """
    Returns index.html.
    :return: index.html
    """
    return render_template('index.html')


@app.route('/api', methods=['GET'])
@limiter.exempt
def api():
    """
    Returns redirect to api documentation.
    :return: Response object with redirect to api documentation.
    """
    return redirect('https://scrapcoinpro.gitbook.io/scrapcoin/')


@app.route('/api/prices', methods=['GET'])
@limiter.limit('10 per minute')
def get_price_list():
    """
    Allows you to send a list of trading pairs as query parameters to obtain the prices of several pairs in
    a single call, e.g. GET /prices?pairs=BTC_USD,BTC_EUR,ETH_USD
    :return: JSON object with the current prices of the given trading pairs.
    """
    conn = get_db_connection()
    if request.method == 'GET':
        try:
            pairs = request.args.get('pairs').split(',')
            pairs = [pair.upper() for pair in pairs]
            pairs = tuple(pairs)
        except Exception as e:
            print(e)
            return jsonify({'ERROR': 'Invalid pairs.'}), 400

        try:
            cur = conn.execute(f"SELECT * FROM BITCOIN WHERE PAIR IN {pairs}").fetchall()

            rows = [dict(row) for row in cur]

            if len(rows) == 0:
                return jsonify({'ERROR': 'Invalid pairs.'}), 400
            else:
                return jsonify(rows), 200
        except Exception as e:
            print(e)
            return jsonify({'ERROR': 'Invalid pairs.'}), 400


@app.route('/api/prices/<pair>', methods=['GET'])
@limiter.limit('10 per minute')
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
        try:
            cur = conn.execute(f"SELECT * FROM BITCOIN WHERE PAIR LIKE '{pair.upper()}'").fetchall()

            rows = [dict(row) for row in cur]

            if len(rows) == 0:
                return jsonify({'ERROR': 'Invalid pair.'}), 400
            else:
                return jsonify(rows), 200
        except Exception as e:
            print(e)
            return jsonify({'ERROR': 'Invalid pair.'}), 400


@app.route('/api/exchanges/<exchange_name>/prices', methods=['GET'])
@limiter.limit('10 per minute')
def get_exchange_price_list(exchange_name):
    """
    Returns the prices of all trading pairs available on a specific exchange,
    e.g. GET /exchanges/coinbasepro/prices to get the prices available on Coinbase Pro.
    :param exchange_name: The name of the exchange.
    :return: JSON object with the current prices of the given exchange.
    """
    conn = get_db_connection()
    if request.method == 'GET':
        try:
            cur = conn.execute(f"SELECT * FROM BITCOIN WHERE EXCHANGE LIKE '{exchange_name.upper()}'").fetchall()

            rows = [dict(row) for row in cur]

            if len(rows) == 0:
                return jsonify({'ERROR': 'Invalid exchange.'}), 400
            else:
                return jsonify(rows), 200
        except Exception as e:
            print(e)
            return jsonify({'ERROR': 'Invalid exchange.'}), 400


@app.route('/api/exchanges', methods=['GET'])
@limiter.limit('10 per minute')
def get_exchange_list():
    """
    Returns the list of exchanges available.
    :return: JSON object with the list of exchanges available.
    """

    conn = get_db_connection()
    if request.method == 'GET':
        try:
            cur = conn.execute(f"SELECT DISTINCT EXCHANGE FROM BITCOIN").fetchall()

            rows = [dict(row) for row in cur]

            if len(rows) == 0:
                return jsonify({'ERROR': 'Invalid exchange.'}), 400
            else:
                return jsonify(rows), 200
        except Exception as e:
            print(e)
            return jsonify({'ERROR': 'Invalid exchange.'}), 400


@app.route('/api/exchanges/<exchange_name>/pairs', methods=['GET'])
@limiter.limit('10 per minute')
def get_exchange_pair_list(exchange_name):
    """
    Returns the list of trading pairs available on a specific exchange,
    e.g. GET /exchanges/CoinBasePro/pairs to get the trading pairs available on Coinbase Pro.
    :param exchange_name: The name of the exchange.
    :return: JSON object with the list of trading pairs available on the given exchange.
    """

    conn = get_db_connection()
    if request.method == 'GET':
        try:
            cur = conn.execute(
                f"SELECT DISTINCT PAIR FROM BITCOIN WHERE EXCHANGE LIKE '{exchange_name.upper()}'").fetchall()

            rows = [dict(row) for row in cur]

            if len(rows) == 0:
                return jsonify({'ERROR': 'Invalid exchange.'}), 400
            else:
                return jsonify(rows), 200
        except Exception as e:
            print(e)
            return jsonify({'ERROR': 'Invalid exchange.'}), 400


@app.route('/api/exchanges/<exchange_name>/pairs/<pair>', methods=['GET'])
@limiter.limit('10 per minute')
def get_exchange_pair_price(exchange_name, pair):
    """
    Returns the price of a specific trading pair on a specific exchange,
    e.g. GET /exchanges/CoinBasePro/pairs/BTC_USD to get the price of Bitcoin in US dollars on Coinbase Pro.
    :param exchange_name: The name of the exchange.
    :param pair: The trading pair to be searched.
    :return: JSON object with the price of the given trading pair on the given exchange.
    """

    conn = get_db_connection()
    if request.method == 'GET':
        try:
            cur = conn.execute(
                f"SELECT * FROM BITCOIN WHERE EXCHANGE LIKE '{exchange_name.upper()}' "
                f"AND PAIR LIKE '{pair.upper()}'").fetchall()

            rows = [dict(row) for row in cur]

            if len(rows) == 0:
                return jsonify({'ERROR': 'Invalid exchange or pair.'}), 400
            else:
                return jsonify(rows), 200
        except Exception as e:
            print(e)
            return jsonify({'ERROR': 'Invalid exchange or pair.'}), 400


@app.route('/favicon.ico')
def favicon():
    """
    Returns the favicon.
    :return: The favicon.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
