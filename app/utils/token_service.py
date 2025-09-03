# token_service.py
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import os
import requests
import time
import uuid
from urllib import parse


def _encode_text(text: str) -> str:
    """Encode text for AliCloud API signature."""
    encoded_text = parse.quote_plus(text)
    return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')


def _encode_dict(dic: dict) -> str:
    """Encode dict parameters into AliCloud required format."""
    keys = dic.keys()
    dic_sorted = [(key, dic[key]) for key in sorted(keys)]
    encoded_text = parse.urlencode(dic_sorted)
    return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')


def get_alicloud_token(access_key_id: str, access_key_secret: str):
    """
    Generate an AliCloud token.

    :param access_key_id: AliCloud access key ID
    :param access_key_secret: AliCloud access key secret
    :return: (token, expire_time) or (None, None) if failed
    """
    parameters = {
        'AccessKeyId': access_key_id,
        'Action': 'CreateToken',
        'Format': 'JSON',
        'RegionId': 'ap-southeast-1',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'SignatureVersion': '1.0',
        'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        'Version': '2019-07-17'
    }

    # Build canonical query string
    query_string = _encode_dict(parameters)

    # Build string to sign
    string_to_sign = 'GET' + '&' + _encode_text('/') + '&' + _encode_text(query_string)

    # Calculate signature
    secreted_string = hmac.new(
        bytes(access_key_secret + '&', encoding='utf-8'),
        bytes(string_to_sign, encoding='utf-8'),
        hashlib.sha1
    ).digest()
    signature = base64.b64encode(secreted_string)

    # URL encode signature
    signature = _encode_text(signature)

    # Request token
    full_url = f'http://nlsmeta.ap-southeast-1.aliyuncs.com/?Signature={signature}&{query_string}'
    response = requests.get(full_url)

    if response.ok:
        root_obj = response.json()
        key = 'Token'
        if key in root_obj:
            token = root_obj[key]['Id']
            expire_time = root_obj[key]['ExpireTime']
            return token, expire_time

    return None, None