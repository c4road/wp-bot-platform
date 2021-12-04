import boto3
import json
import logging

from botocore.exceptions import ClientError


def get_binance_secret():

    secret_name = "wp-bot/BinanceSecrets"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logging.error('[get_binance_secret] Something happening retrieving the secrets %s', repr(e))
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret_string = get_secret_value_response['SecretString']
        else:
            logging.error('[get_binance_secret] No secrets string in aws response')
            return None, None
    
    secret = json.loads(secret_string)
    api_key = secret.get('BinanceApiKey')
    secret_key = secret.get('BinanceSecretKey')
    
    if not api_key or not secret_key:
        logging.error('[get_binance_secret] Impossibility to retrieve the secrets: %s', get_secret_value_response)

    return api_key, secret_key
