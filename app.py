import logging

from chalice import Chalice
from binance.client import Client
from chalicelib.secrets import get_binance_secret

app = Chalice(app_name='wp-bot-platform')
app.log.setLevel(logging.DEBUG)

@app.route('/ping')
def index():
    return {'data': 'pong'}

@app.route('/coin/{coin}', methods=['GET'])
def CoinUSDTHandler(coin=None):

    API_KEY, SECRET_KEY = get_binance_secret()
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

@app.route('/whatsapp/ack', methods=['POST'])
def WhatsappAckHandler():
    body = app.current_request.json_body
    logging.info("This is what is comming from twilio - %s", body)
    
    return 