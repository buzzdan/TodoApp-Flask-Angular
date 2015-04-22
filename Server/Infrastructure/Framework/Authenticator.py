# from requests.packages.urllib3.exceptions import DecodeError
import os
from urllib.parse import parse_qsl
from datetime import datetime, timedelta
import json
from functools import wraps
import jwt
import requests
from flask import g, request, jsonify, Flask
from jwt import DecodeError, ExpiredSignatureError
# from urlparse import parse_qs, parse_qsl
# from urllib import urlencode
# from requests_oauthlib import OAuth1
from Server.Domain.Core import InvalidInstantiationError

from Server.Infrastructure.Services import EnvironmentSettingsLoader


class SecretAuthKeys:
    def __init__(self):
        configs = self._get_configs()
        self.secret_token = configs['TOKEN_SECRET']
        self.facebook_secret = configs['FACEBOOK_SECRET']

        if self.secret_token is None or str(self.secret_token).strip() == '':
            raise InvalidInstantiationError(type(self).__class__.__name__, "secrets.secret_token")

    def _get_configs(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        root_folder_path = os.path.join(current_folder, '..', '..', '..')
        _configs = EnvironmentSettingsLoader(root_folder_path)
        return _configs

_secrets = SecretAuthKeys()

# Idea taken from https://github.com/sahat/satellizer/tree/master/examples/Server/python
# TODO: Implement user_repository (memory/mongoDB) and import angular package satellizer


def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.now(),
        'exp': datetime.now() + timedelta(days=14)
    }
    token = jwt.encode(payload, _secrets.secret_token)
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, _secrets.secret_token)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignatureError:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

