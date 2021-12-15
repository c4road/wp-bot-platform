import logging
from twilio.rest import Client 

from chalice import Chalice
from binance.client import Client
from chalicelib.secrets import get_binance_secret, get_twilio_secret

app = Chalice(app_name='wp-bot-platform')
logging.basicConfig(level = logging.INFO)
app.log.setLevel(logging.DEBUG)

@app.route('/ping')
def index():
    app.log.info('logging cloudfront using chalice log')
    return {'data': 'pong'}

@app.route('/coin/{coin}', methods=['GET'])
def CoinUSDTHandler(coin=None):

    API_KEY, SECRET_KEY = get_binance_secret()
    client = Client(API_KEY, SECRET_KEY)
    symbol = coin + 'USDT' if coin else 'BTCUSDT'
    app.log.info('Fetching %s price', symbol)
    try:
        avg_price = client.get_avg_price(symbol=symbol)
    except Exception as e:
        app.log.error('Something happened fetching %s symbol from Binance', symbol)
        raise e 
    response = {
        'price': avg_price.get('price')
    }

    return  response

@app.route('/whatsapp/ack', methods=['POST'])
def WhatsappAckHandler():
    try:
        body = app.current_request.json_body
        app.log.info('This is comming from twilio - %s', body)
        account_sid, auth_token = get_twilio_secret()
        # client = Client(account_sid, auth_token) 
        # client.messages.create( 
        #     from_='whatsapp:+14155238886',  
        #     body='que paso pana mio',      
        #     to='whatsapp:+5491122520361' 
        # ) 
    except Exception as e:
        app.log.error('something happened in the ack handler %s', str(e))
        raise
    response = {}
    return response
