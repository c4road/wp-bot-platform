import logging

from chalice import Chalice
from binance.client import Client
from chalicelib.secrets import get_binance_secret

app = Chalice(app_name='wp-bot-platform')
API_KEY, SECRET_KEY = get_binance_secret()

@app.route('/ping')
def index():
    return {'data': 'pong'}

@app.route('/coin/{coin}', methods=['GET'])
def CoinUSDTHandler(coin=None):

    client = Client(API_KEY, SECRET_KEY)
    symbol = coin + 'USDT' if coin else 'BTCUSDT'

    try:
        avg_price = client.get_avg_price(symbol=symbol)
    except Exception as e:
        raise e 
    response = {
        'price': avg_price.get('price')
    }

    return  response
