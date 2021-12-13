import logging
from twilio.rest import Client 

from chalice import Chalice
from binance.client import Client
from chalicelib.secrets import get_binance_secret, get_twilio_secret

app = Chalice(app_name='wp-bot-platform', configure_logs=False)
logging.basicConfig(level = logging.INFO)
LOGGER = logging.getLogger()

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
def WhatsappAckHandler(log=LOGGER):
    body = app.current_request._json_body
    log.info("[plain logging] This is what is comming from twilio - %s", body)

    account_sid, auth_token = get_twilio_secret()
    client = Client(account_sid, auth_token) 
    client.messages.create( 
        from_='whatsapp:+14155238886',  
        body='que paso pana mio',      
        to='whatsapp:+5491122520361' 
    ) 

    return None
