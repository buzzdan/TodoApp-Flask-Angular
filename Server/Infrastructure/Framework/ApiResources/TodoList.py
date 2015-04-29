import json
from flask import g
from flask_restful import reqparse, Resource
from Server.Application.ListManagementService import ListManagementService
from Server.Domain.Entities import TodoTask
from Server.Infrastructure.Framework.Authenticator import login_required
from Server.Infrastructure.Framework.DTOs import TodoDTO
from Server.Domain.Interfaces import ITodoRepository, ITodoListRepository
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
        :param todo_repository: an instance of ITodoRepository
        :return: class object of Todo Resource
        """
        cls._list_management_service = list_management_service
        return cls

    @login_required
    def get(self):
        my_lists = self._list_management_service.get_my_lists_metadata(g.user_id)
        default_list = next(iter(my_lists), None)
        if not default_list:
            return json.dumps(dict())
        else:
            todos = self._list_management_service.get_list(default_list.get_id()).get_todos()
            return self.toJson(todos)

    def post(self):
        args = self._parser.parse_args()
        task_name = args['task']

        try:
            task = TodoTask(task_name)
            self._todo_repository.add(task)
            todos = self._todo_repository.get_all()
            return self.toJson(todos), 201
        except Exception as ex:
            return "Input error: {}".format(ex), 500  # General Error

        except ValueError as e:
            return "Input error: {}".format(e), 422  # HTTP error for Unprocessable Entity

    def toJson(self, todos):
        return [TodoDTO(todo).to_json() for todo in todos]
