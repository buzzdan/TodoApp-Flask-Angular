# from requests.packages.urllib3.exceptions import DecodeError
from urllib.parse import parse_qsl
from server.Entities.User import User
from server.Repositories.IUserRepository import IUserRepository
from server.Utils.Exceptions import InvalidInstantiationError
from server.Utils.GeneralUtils import pre_condition_arg
from datetime import datetime, timedelta
import jwt
import json
import requests
from functools import wraps
from flask import g, request, jsonify
from jwt import DecodeError, ExpiredSignatureError

# from urlparse import parse_qs, parse_qsl
# from urllib import urlencode
# from requests_oauthlib import OAuth1


class SecretAuthKeys:
    def __init__(self, user_token, facebook_secret):
        pre_condition_arg(self, user_token, of_type=str)
        self.secret_token = user_token
        self.facebook_secret = facebook_secret

# Idea taken from https://github.com/sahat/satellizer/tree/master/examples/server/python
# TODO: Implement user_repository (memory/mongoDB) and import angular package satellizer


class Authenticator:
    def __init__(self, user_repository, flask_app, secrets):

        pre_condition_arg(self, user_repository, of_type=IUserRepository)
        self._user_repository = user_repository

        if flask_app is None:
            raise InvalidInstantiationError(type(self).__class__.__name__, "flask_app")
        self._flask_app = flask_app

        pre_condition_arg(self, secrets, of_type=SecretAuthKeys)
        self._secrets = secrets

        if secrets.secret_token is None:
            raise InvalidInstantiationError(type(self).__class__.__name__, "secrets.secret_token")

        self.register_routes()

    def create_token(self, user):
        payload = {
            'sub': user.id,
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(days=14)
        }
        token = jwt.encode(payload, self._secrets.secret_token)
        return token.decode('unicode_escape')

    def parse_token(self, req):
        token = req.headers.get('Authorization').split()[1]
        return jwt.decode(token, self._secret_token)

    def login_required(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.headers.get('Authorization'):
                response = jsonify(message='Missing authorization header')
                response.status_code = 401
                return response

            try:
                payload = self.parse_token(request)
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


    # Routes
    # TODO: register api routes
    def register_routes(self):
        self._flask_app.add_url_rule('/api/me', 'me', self.me, methods=['GET'])
        self._flask_app.add_url_rule('/auth/login', 'login', self.login, methods=['POST'])
        self._flask_app.add_url_rule('/auth/signup', 'signup', self.login, methods=['POST'])
        self._flask_app.add_url_rule('/auth/facebook', 'facebook', self.login, methods=['POST'])

    # @app.route('/api/me')
    @login_required
    def me(self):
        user = self._user_repository.get_by_id(g.user_id)
        return jsonify(user.to_json())

    # @app.route('/auth/login', methods=['POST'])
    def login(self):
        user = self._user_repository.get_by_email(email=request.json['email'])
        if not user or not user.check_password(request.json['password']):
            response = jsonify(message='Wrong Email or Password')
            response.status_code = 401
            return response
        token = self.create_token(user)
        return jsonify(token=token)

    # @app.route('/auth/signup', methods=['POST'])
    def signup(self):
        user = User(email=request.json['email'], password=request.json['password'])
        self._user_repository.add(user)
        token = self.create_token(user)
        return jsonify(token=token)

    # @app.route('/auth/facebook', methods=['POST'])
    def facebook(self):
        if self._secrets.facebook_secret is None:
            raise ValueError("facebook_secret")

        access_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token'
        graph_api_url = 'https://graph.facebook.com/v2.3/me'

        params = {
            'client_id': request.json['clientId'],
            'redirect_uri': request.json['redirectUri'],
            'client_secret': self._secrets.facebook_secret,
            'code': request.json['code']
        }

        # Step 1. Exchange authorization code for access token.
        r = requests.get(access_token_url, params=params)
        access_token = dict(parse_qsl(r.text))

        # Step 2. Retrieve information about the current user.
        r = requests.get(graph_api_url, params=access_token)
        profile = json.loads(r.text)

        # Step 3. (optional) Link accounts.
        if request.headers.get('Authorization'):
            user = self._user_repository.get_by_facebook_id(facebook=profile['id'])
            if user:
                response = jsonify(message='There is already a Facebook account that belongs to you')
                response.status_code = 409
                return response

            payload = self.parse_token(request)

            user = self._user_repository.get_by_id(id=payload['sub'])
            if not user:
                response = jsonify(message='User not found')
                response.status_code = 400
                return response

            u = User(facebook=profile['id'], display_name=profile['name'])
            self._user_repository.add(u)
            token = self.create_token(u)
            return jsonify(token=token)

        # Step 4. Create a new account or return an existing one.
        user = self._user_repository.get_by_facebook_id(facebook=profile['id'])
        if user:
            token = self.create_token(user)
            return jsonify(token=token)

        u = User(facebook=profile['id'], display_name=profile['name'])
        self._user_repository.add(u)
        token = self.create_token(u)
        return jsonify(token=token)

#
# @app.route('/auth/github', methods=['POST'])
# def github():
#     access_token_url = 'https://github.com/login/oauth/access_token'
#     users_api_url = 'https://api.github.com/user'
#
#     params = {
#         'client_id': request.json['clientId'],
#         'redirect_uri': request.json['redirectUri'],
#         'client_secret': app.config['GITHUB_SECRET'],
#         'code': request.json['code']
#     }
#
#     # Step 1. Exchange authorization code for access token.
#     r = requests.get(access_token_url, params=params)
#     access_token = dict(parse_qsl(r.text))
#     headers = {'User-Agent': 'Satellizer'}
#
#     # Step 2. Retrieve information about the current user.
#     r = requests.get(users_api_url, params=access_token, headers=headers)
#     profile = json.loads(r.text)
#
#     # Step 3. (optional) Link accounts.
#     if request.headers.get('Authorization'):
#         user = User.query.filter_by(github=profile['id']).first()
#         if user:
#             response = jsonify(message='There is already a GitHub account that belongs to you')
#             response.status_code = 409
#             return response
#
#         payload = parse_token(request)
#
#         user = User.query.filter_by(id=payload['sub']).first()
#         if not user:
#             response = jsonify(message='User not found')
#             response.status_code = 400
#             return response
#
#         u = User(github=profile['id'], display_name=profile['name'])
#         db.session.add(u)
#         db.session.commit()
#         token = create_token(u)
#         return jsonify(token=token)
#
#     # Step 4. Create a new account or return an existing one.
#     user = User.query.filter_by(github=profile['id']).first()
#     if user:
#         token = create_token(user)
#         return jsonify(token=token)
#
#     u = User(github=profile['id'], display_name=profile['name'])
#     db.session.add(u)
#     db.session.commit()
#     token = create_token(u)
#     return jsonify(token=token)
#
#
# @app.route('/auth/google', methods=['POST'])
# def google():
#     access_token_url = 'https://accounts.google.com/o/oauth2/token'
#     people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'
#
#     payload = dict(client_id=request.json['clientId'],
#                    redirect_uri=request.json['redirectUri'],
#                    client_secret=app.config['GOOGLE_SECRET'],
#                    code=request.json['code'],
#                    grant_type='authorization_code')
#
#     # Step 1. Exchange authorization code for access token.
#     r = requests.post(access_token_url, data=payload)
#     token = json.loads(r.text)
#     headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
#
#     # Step 2. Retrieve information about the current user.
#     r = requests.get(people_api_url, headers=headers)
#     profile = json.loads(r.text)
#
#     user = User.query.filter_by(google=profile['sub']).first()
#     if user:
#         token = create_token(user)
#         return jsonify(token=token)
#     u = User(google=profile['sub'],
#              display_name=profile['name'])
#     db.session.add(u)
#     db.session.commit()
#     token = create_token(u)
#     return jsonify(token=token)
#
#
# @app.route('/auth/linkedin', methods=['POST'])
# def linkedin():
#     access_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
#     people_api_url = 'https://api.linkedin.com/v1/people/~:(id,first-name,last-name,email-address)'
#
#     payload = dict(client_id=request.json['clientId'],
#                    redirect_uri=request.json['redirectUri'],
#                    client_secret=app.config['LINKEDIN_SECRET'],
#                    code=request.json['code'],
#                    grant_type='authorization_code')
#
#     # Step 1. Exchange authorization code for access token.
#     r = requests.post(access_token_url, data=payload)
#     access_token = json.loads(r.text)
#     params = dict(oauth2_access_token=access_token['access_token'],
#                   format='json')
#
#     # Step 2. Retrieve information about the current user.
#     r = requests.get(people_api_url, params=params)
#     profile = json.loads(r.text)
#
#     user = User.query.filter_by(linkedin=profile['id']).first()
#     if user:
#         token = create_token(user)
#         return jsonify(token=token)
#     u = User(linkedin=profile['id'],
#              display_name=profile['firstName'] + ' ' + profile['lastName'])
#     db.session.add(u)
#     db.session.commit()
#     token = create_token(u)
#     return jsonify(token=token)
#
#
# @app.route('/auth/twitter')
# def twitter():
#     request_token_url = 'https://api.twitter.com/oauth/request_token'
#     access_token_url = 'https://api.twitter.com/oauth/access_token'
#     authenticate_url = 'https://api.twitter.com/oauth/authenticate'
#
#     if request.args.get('oauth_token') and request.args.get('oauth_verifier'):
#         auth = OAuth1(app.config['TWITTER_CONSUMER_KEY'],
#                       client_secret=app.config['TWITTER_CONSUMER_SECRET'],
#                       resource_owner_key=request.args.get('oauth_token'),
#                       verifier=request.args.get('oauth_verifier'))
#         r = requests.post(access_token_url, auth=auth)
#         profile = dict(parse_qsl(r.text))
#
#         user = User.query.filter_by(twitter=profile['user_id']).first()
#         if user:
#             token = create_token(user)
#             return jsonify(token=token)
#         u = User(twitter=profile['user_id'],
#                  display_name=profile['screen_name'])
#         db.session.add(u)
#         db.session.commit()
#         token = create_token(u)
#         return jsonify(token=token)
#     else:
#         oauth = OAuth1(app.config['TWITTER_CONSUMER_KEY'],
#                        client_secret=app.config['TWITTER_CONSUMER_SECRET'],
#                        callback_uri=app.config['TWITTER_CALLBACK_URL'])
#         r = requests.post(request_token_url, auth=oauth)
#         oauth_token = dict(parse_qsl(r.text))
#         qs = urlencode(dict(oauth_token=oauth_token['oauth_token']))
#         return redirect(authenticate_url + '?' + qs)
