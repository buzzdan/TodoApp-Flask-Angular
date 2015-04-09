from flask_restful import reqparse, Resource
from server.ApiResources.DTOs.TodoDTO import TodoDTO
from server.Repositories.InMemoryTodoRepository import InMemoryTodoRepository


class TodoList(Resource):
    """shows a list of all todos, and lets you POST to add new tasks
    """
    def __init__(self):
        self.todo_repository = InMemoryTodoRepository()
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('task', type=str)

    def get(self):
        todos = self.todo_repository.get_all()
        return self.toJson(todos)

    def post(self):
        args = self._parser.parse_args()
        task_name = args['task']

        try:
            self.todo_repository.add(task_name)
            todos = self.todo_repository.get_all()
            return self.toJson(todos), 201

        except ValueError as error:
            return "Input error: {}".format(error), 422  # HTTP error for Unprocessable Entity

    def toJson(self, todos):
        return [TodoDTO(todo).to_json() for todo in todos]
