import logging
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioException

from chalice import Chalice, Response
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

@app.route('/whatsapp/ack', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def WhatsappAckHandler():
    request = app.current_request.to_dict()
    body = app.current_request.json_body
    raw_body = app.current_request.raw_body

    app.log.info('This is comming from twilio request=%s', request)
    app.log.info('Body of the requests - body=%s, raw_body=%s', body, raw_body)
    account_sid, auth_token = get_twilio_secret()
    try:
        twilio = TwilioClient(account_sid, auth_token) 
        message = twilio.messages.create( 
            from_='whatsapp:+14155238886',
            body='que paso pana mio',      
            to='whatsapp:+5491122520361' 
        ) 
    except TwilioException as e:
        error = {
            'name': str(e),
            'uri': e.uri,
            'status': e.status,
            'message': e.msg,
            'code': e.code,
            'method': e.method,
            'details': e.exception,
        }
        app.log.error('Twilio error: %s', error)
        return Response(body=error,
                        status_code=500,
                        headers={'Content-Type': 'application/json'})
    except Exception as e:
        error = {'error': str(e)}
        app.log.error('Unknown Exception - %s', error)
        return Response(body=error,
                        status_code=500,
                        headers={'Content-Type': 'application/json'})
    else:
        app.log.info('Message created: message_id=%s', message)
        return Response(body={},
                        status_code=204,
                        headers={'Content-Type': 'application/json'})
