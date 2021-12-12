import logging
from twilio.rest import Client 

from chalice import Chalice
from binance.client import Client
from chalicelib.secrets import get_binance_secret

app = Chalice(app_name='wp-bot-platform')
logging.getLogger().setLevel(logging.INFO)

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

    account_sid = 'ACa7d17651bc98465ae590d0a6e6443a06' 
    auth_token = '4f6fa92850cfffc32d8049df89c32bfb'
    client = Client(account_sid, auth_token) 

    try:
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='que paso pana mio',      
                                    to='whatsapp:+5491122520361' 
                                ) 
    except Exception as e:
        logging.error("Something bad happened calling twilio - %s", e)

    return 
