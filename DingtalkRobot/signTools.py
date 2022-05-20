import time
import hmac
import hashlib
import base64
import urllib.parse

from typing import Dict


def sing_calculation(secret: str) -> Dict[str, str]:
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    # string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign = ''.join([timestamp, '\n', secret])
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return {'timestamp': timestamp, 'sign': sign}





