import json
from flask import g
from flask_restful import reqparse, Resource
from Server.Application.ListManagementService import ListManagementService
from Server.Domain.Entities import TodoTask
from Server.Infrastructure.Framework.Authenticator import login_required
from Server.Infrastructure.Framework.DTOs import TodoDTO, TodoListDTO
from Server.Domain.Core import must_have


class TodoLists(Resource):
    """shows a list of all todos, and lets you POST to add new tasks
    """
    def __init__(self):

        must_have(self,
                  member="_list_management_service",
                  of_type=ListManagementService,
                  use_method=TodoLists.create.__name__)

        self._parser = reqparse.RequestParser()
        self._parser.add_argument('listName', type=str)

    @classmethod
    def create(cls, list_management_service: ListManagementService):
        """
        :param list_management_service: an instance of ListManagementService
        :return: class object of TodoList Resource
        """
        cls._list_management_service = list_management_service
        return cls

    @login_required
    def get(self):
        """
        :return: all lists Metadata
        """
        my_lists = self._list_management_service.get_my_lists_metadata(g.user_id)
        return self.toJson(my_lists)

    @login_required
    def post(self):
        """
        Creates a new list with authorized user as the owner
        :return: creation approval
        """
        args = self._parser.parse_args()
        list_name = args['listName']

        try:
            self._list_management_service.create_new_list(list_name, g.user_id)
            return "New list created", 201

        except Exception as ex:
            return "Input error: {}".format(ex), 500  # General Error

        except ValueError as e:
            return "Input error: {}".format(e), 422  # HTTP error for Unprocessable Entity

    def toJson(self, lists):
        return [TodoListDTO(todo_list).to_json() for todo_list in lists]
