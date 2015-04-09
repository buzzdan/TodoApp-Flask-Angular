from server.Entities.TodoTask import TodoTask
from server.Utils.Maybe import Maybe


class TodoRepository:

    _todos = [TodoTask('build an API'), TodoTask('shop soy milk'), TodoTask('study python')]


    #_todo_db = {todo.get_id(): todo for todo in _todos}
    # _todo_db = {
    #     'todo1': {'task': 'build an API'},
    #     'todo2': {'task': '?????'},
    #     'todo3': {'task': 'profit!'},
    # }

    def __init__(self):
        self._todo_db = TodoRepository._todos

    def get_all(self):
        return self._todo_db

    def get_by_id(self, todo_id):
        todo = next((task for task in self._todo_db if task.get_id() == todo_id), None)
        task_doesnt_exist = todo is None
        if task_doesnt_exist:
            return Maybe(None)
        else:
            return Maybe(value=todo)

    def delete(self, todo_id):
        maybe = self.get_by_id(todo_id)
        if maybe.exists():
            todo = maybe.values()[0]
            self._todo_db.remove(todo)
        else:
            self.raise_key_error(todo_id)

    def update(self, todo_id, task_name):
        maybe = self.get_by_id(todo_id)
        if maybe.exists():
            todo = maybe.values()[0]
            todo.update_task(task_name)
        else:
            self.raise_key_error(todo_id)

    def add(self, task_name):
        t = TodoTask(task_name)
        self._todo_db.append(t)

    def raise_key_error(self, todo_id):
        raise KeyError("{} doesnt exist in todos".format(todo_id))
