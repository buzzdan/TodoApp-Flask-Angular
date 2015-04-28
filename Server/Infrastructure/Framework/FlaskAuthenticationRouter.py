from Server.Domain.Core import pre_condition_arg
from Server.Domain.Entities import User
from Server.Domain.Interfaces import IUserRepository, IPasswordHasher
from Server.Infrastructure.Framework.Authenticator import SecretAuthKeys, parse_token, create_token
import json
import requests
from flask import Flask, request, jsonify


class FlaskAuthenticationRouter:
    def __init__(self, user_repository, password_hasher, flask_app):

        pre_condition_arg(self, user_repository, of_type=IUserRepository)
        self._user_repository = user_repository

        pre_condition_arg(self, password_hasher, of_type=IPasswordHasher)
        self._password_hasher = password_hasher

        pre_condition_arg(self, flask_app, of_type=Flask)
        self._flask_app = flask_app

        self._secrets = SecretAuthKeys()

    # Routes
    def register_routes(self):
        # self._flask_app.add_url_rule('/api/me', 'me', self.me, methods=['GET'])
        self._flask_app.add_url_rule('/auth/login', 'login', self.login, methods=['POST'])
        self._flask_app.add_url_rule('/auth/signup', 'signup', self.signup, methods=['POST'])
        self._flask_app.add_url_rule('/auth/facebook', 'facebook', self.facebook, methods=['POST'])

    # @app.route('/auth/login', methods=['POST'])
    def login(self):
        maybe_user = self._user_repository.get_by_email(email=request.json['email'])
        if maybe_user.exists():
            user = maybe_user.values()[0]
        if not maybe_user.exists() or not self._password_hasher.verify(request.json['password'], user.hashed_password):
            response = jsonify(message='Wrong Email or Password')
            response.status_code = 401
            return response
        token = create_token(user)
        return jsonify(token=token)

    # @app.route('/auth/signup', methods=['POST'])
    def signup(self):
        hashed_password = self._password_hasher.encode(request.json['password'])
        user = User(email=request.json['email'], hashed_password=hashed_password, display_name=request.json['displayName'])
        self._user_repository.add(user)
        token = create_token(user)
        return jsonify(token=token)

    def _create_facebook_pic_link(self, facebook_id):
        return 'http://graph.facebook.com/{facebook_id}/picture?type=large'.format(facebook_id=facebook_id)

    # @app.route('/auth/facebook', methods=['POST'])
    def facebook(self):
        if self._secrets.facebook_secret is None or str(self._secrets.facebook_secret).strip() == '':
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
        access_token = json.loads(r.text)

        # Step 2. Retrieve information about the current user.
        r = requests.get(graph_api_url, params=access_token)
        profile = json.loads(r.text)

        # Step 3. (optional) Link accounts.
        if request.headers.get('Authorization'):
            maybe_user = self._user_repository.get_by_facebook_id(facebook_id=profile['id'])
            if maybe_user.exists():
                response = jsonify(message='There is already a Facebook account that belongs to you')
                response.status_code = 409
                return response

            payload = parse_token(request)

            maybe_user = self._user_repository.get_by_id(user_id=payload['sub'])
            if not maybe_user.exists():
                response = jsonify(message='User not found')
                response.status_code = 400
                return response

            # u = User(facebook=profile['id'], display_name=profile['name'])
            # self._user_repository.add(u)
            # token = create_token(u)
            # return jsonify(token=token)
            user = maybe_user.values()[0]
            user.facebook = profile['id']
            user.display_name = profile['name']
            if user.email is None:
                user.email = profile['email']
            if user.pic_link is None:
                user.pic_link = self._create_facebook_pic_link(user.facebook)

            self._user_repository.update(user.id, user)
            token = create_token(user)
            return jsonify(token=token)

        # Step 4. Create a new account or return an existing one.
        maybe_user = self._user_repository.get_by_facebook_id(facebook_id=profile['id'])
        if maybe_user.exists():
            user = maybe_user.values()[0]
            token = create_token(user)
            return jsonify(token=token)

        maybe_user_with_same_email = self._user_repository.get_by_email(email=profile['email'])  # Link accounts
        if maybe_user_with_same_email.exists():
            user = maybe_user_with_same_email.values()[0].copy_user()
            user.facebook = profile['id']
            if user.display_name is None:
                user.display_name = profile['name']
            if user.pic_link is None:
                user.pic_link = self._create_facebook_pic_link(user.facebook)
            self._user_repository.update(user.id, user)
            token = create_token(user)
            return jsonify(token=token)

        pic_link = self._create_facebook_pic_link(profile['id'])
        u = User(facebook=profile['id'], display_name=profile['name'], email=profile['email'], pic_link=pic_link)
        self._user_repository.add(u)

        token = create_token(u)
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

