from Server.Domain.Core import Jsonable
from Server.Infrastructure.Framework.DTOs import TodoDTO


class TodoListDTO(Jsonable):
    def __init__(self, todo_list=None):
        self.id = 0
        self.name = ''
        self.owner_ids = []
        self.todos = []
        if todo_list is not None:
            self.id = todo_list.get_id()
            self.name = todo_list.get_name()
            self.owner_ids = todo_list.get_owner_ids()
            self.todos = [TodoDTO(todo) for todo in todo_list.get_todos()]
