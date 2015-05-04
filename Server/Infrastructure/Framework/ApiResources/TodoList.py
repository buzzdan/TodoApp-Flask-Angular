import json
from flask import g
from flask_restful import reqparse, Resource
from Server.Application.ListManagementService import ListManagementService
from Server.Domain.Entities import TodoTask
from Server.Infrastructure.Framework.Authenticator import login_required
from Server.Infrastructure.Framework.DTOs import TodoDTO, TodoListDTO
from Server.Domain.Core import must_have


class TodoList(Resource):
    """shows a list of all todos, and lets you POST to add new tasks
    """
    def __init__(self):

        must_have(self,
                  member="_list_management_service",
                  of_type=ListManagementService,
                  use_method=TodoList.create.__name__)

        self._parser = reqparse.RequestParser()
        self._parser.add_argument('task', type=str)

    @classmethod
    def create(cls, list_management_service: ListManagementService):
        """
        :param list_management_service: an instance of ListManagementService
        :return: class object of TodoList Resource
        """
        cls._list_management_service = list_management_service
        return cls

    @login_required
    def get(self, list_id):
        """
        :param list_id: specific list to get
        :return: list by id.
        """
        my_list = self._list_management_service.get_list(list_id)
        return TodoListDTO(my_list).to_json()

    @login_required
    def post(self, list_id):
        """
        Creates a new todo task in a specific list
        :return: creation approval
        """
        try:
            args = self._parser.parse_args()
            task_name = args['task']
            self._list_management_service.add_task_to_list(list_id, task_name)
            up_to_dated_list = self._list_management_service.get_list(list_id)
            return TodoListDTO(up_to_dated_list).to_json(), 201

        except Exception as ex:
            return "Input error: {}".format(ex), 500  # General Error

        except ValueError as e:
            return "Input error: {}".format(e), 422  # HTTP error for Unprocessable Entity

    # def toJson(self, todos):
    #     return [TodoDTO(todo).to_json() for todo in todos]

