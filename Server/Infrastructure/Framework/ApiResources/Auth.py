from flask_restful import Resource
from Server.Domain.Core import must_have
from Server.Domain.Interfaces import IUserRepository
from flask_restful import reqparse, abort, Resource


class Auth(Resource):
    """shows a single todo item and lets you delete a todo item
        use the 'create' class method to instantiate the class
    """
    def __init__(self):

        must_have(self,
                  member="_todo_repository",
                  of_type=IUserRepository,
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
