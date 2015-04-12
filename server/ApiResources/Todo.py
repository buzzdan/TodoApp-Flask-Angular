from flask_restful import reqparse, abort, Resource
from server.ApiResources.DTOs.TodoDTO import TodoDTO
from server.Repositories.ITodoRepository import ITodoRepository
from server.Utils.GeneralUtils import *


class Todo(Resource):
    """shows a single todo item and lets you delete a todo item
        use the 'create' class method to instantiate the class
    """
    def __init__(self):

        must_have(self,
                  member="_todo_repository",
                  of_type=ITodoRepository,
                  use_method=Todo.create.__name__)

        self._parser = reqparse.RequestParser()
        self._parser.add_argument('task', type=str)

    @classmethod
    def create(cls, todo_repository):
        """
        :param todo_repository: an instance of ITodoRepository
        :return: class object of Todo Resource
        """
        cls._todo_repository = todo_repository
        return cls

    def abort_doesnt_exist(self, todo_id):
        abort(404, message="Todo {} doesn't exist".format(todo_id))

    def get(self, todo_id):
        maybe = self._todo_repository.get_by_id(todo_id)
        if maybe.exists():
            return TodoDTO(maybe.values()[0]).to_json()
        else:
            self.abort_doesnt_exist(todo_id)

    def delete(self, todo_id):
        try:
            self._todo_repository.delete(todo_id)
            return '', 204
        except KeyError:
            self.abort_doesnt_exist(todo_id)

    def put(self, todo_id):
        args = self._parser.parse_args()
        task_name = args['task']

        try:
            self._todo_repository.update(todo_id, task_name)
            todo = TodoDTO()
            todo.id = todo_id
            todo.task = task_name
            return todo.to_json(), 201

        except KeyError:
            self.abort_doesnt_exist(todo_id)

        except ValueError as error:
            return "Input error: {}".format(error), 422  # HTTP error for Unprocessable Entity


