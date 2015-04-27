from flask_restful import Resource
from Server.Domain.Core import must_have
from Server.Domain.Interfaces import IUserRepository
from flask_restful import reqparse, abort, Resource
from flask import Flask, request, jsonify, g
from Server.Infrastructure.Framework.Authenticator import login_required
from Server.Infrastructure.Framework.DTOs import UserDTO


class Profile(Resource):
    """User Profile
    """
    def __init__(self):

        must_have(self,
                  member="_user_repository",
                  of_type=IUserRepository,
                  use_method=Profile.create.__name__)

        # self._parser = reqparse.RequestParser()
        # self._parser.add_argument('task', type=str)

    @classmethod
    def create(cls, user_repository):
        """
        :param user_repository: an instance of IUserRepository
        :return: class object of Profile Resource
        """
        cls._user_repository = user_repository
        return cls

    def abort_doesnt_exist(self, user_id):
        abort(404, message="user {} doesn't exist".format(user_id))

    # @app.route('/api/me')
    @login_required
    def get(self):
        maybe_user = self._user_repository.get_by_id(g.user_id)
        if maybe_user.exists():
            user = maybe_user.values()[0]
            return UserDTO(user).to_json()
        else:
            self.abort_doesnt_exist(g.user_id)

    @login_required
    def put(self):
        maybe_user = self._user_repository.get_by_id(g.user_id)
        if maybe_user.exists():
            user = maybe_user.values()[0]
            user.display_name = request.json['displayName']
            user.email = request.json['email']
            self._user_repository.update(g.user_id, user)
        else:
            self.abort_doesnt_exist(g.user_id)