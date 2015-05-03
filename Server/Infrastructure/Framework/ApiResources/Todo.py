from flask_restful import reqparse, abort, Resource
from Server.Application import ListManagementService
from Server.Infrastructure.Framework.DTOs import TodoDTO
from Server.Domain.Core.GeneralUtils import *


class Todo(Resource):
    """shows a single todo item and lets you delete a todo item
        use the 'create' class method to instantiate the class
    """
    def __init__(self):

        must_have(self,
                  member="_list_management_service",
                  of_type=ListManagementService,
                  use_method=Todo.create.__name__)

        self._parser = reqparse.RequestParser()
        self._parser.add_argument('task', type=str)

    @classmethod
    def create(cls, list_management_service):
        """
        @type list_management_service: ListManagementService
        :return: class object of Todo Resource
        """
        cls._list_management_service = list_management_service
        return cls

    def abort_doesnt_exist(self, message):
        abort(404, message=message)

    def get(self, list_id, todo_id):
        try:
            todo = self._list_management_service.get_todo_from_list(list_id, todo_id)
            return TodoDTO(todo).to_json()

        except KeyError as ex:
            self.abort_doesnt_exist("{}".format(ex))

        except Exception as e:
            abort(500, message="{}".format(e))

    def delete(self, list_id, todo_id):
        try:
            self._list_management_service.delete_task_from_list(list_id, todo_id)
            return '', 204
        except KeyError as ex:
            self.abort_doesnt_exist("{}".format(ex))
        except Exception as e:
            abort(500, message="{}".format(e))

    def put(self, list_id, todo_id):
        args = self._parser.parse_args()
        task_name = args['task']

        try:
            self._list_management_service.update_todo(list_id, todo_id, task_name)
            todo = TodoDTO()
            todo.id = todo_id
            todo.task = task_name
            return todo.to_json(), 201

        except KeyError as ex:
            self.abort_doesnt_exist("{}".format(ex))

        except ValueError as error:
            return "Input error: {}".format(error), 422  # HTTP error for Unprocessable Entity

        except Exception as e:
            abort(500, message="{}".format(e))


