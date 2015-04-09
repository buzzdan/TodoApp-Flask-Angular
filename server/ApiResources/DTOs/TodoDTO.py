from server.Utils.Jsonable import Jsonable


class TodoDTO(Jsonable):
    def __init__(self, todo_task=None):
        self.id = 0
        self.task = ''
        if todo_task is not None:
            self.id = todo_task.get_id()
            self.task = todo_task.get_task_name()
