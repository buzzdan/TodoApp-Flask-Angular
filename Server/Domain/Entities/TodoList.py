import json
from uuid import uuid1, UUID
from Server.Domain.Core import pre_condition_arg, method_guard
from Server.Domain.Entities import TodoTask, TodoTaskState


class TodoList:
    def __init__(self, name, owner_ids, todos, list_id: str=None):
        pre_condition_arg(self, name, of_type=str)
        self._name = name

        pre_condition_arg(self, todos, list_of_type=TodoTask)
        self._todos = todos

        pre_condition_arg(self, owner_ids, list_of_type=str)
        if len(owner_ids) < 1:
            raise ValueError("Todo list must have at least one owner")

        self._owner_ids = owner_ids

        if list_id:
            if not isinstance(list_id, str):
                raise ValueError("list_id must be a unique identifier string")
            self._list_id = list_id
        else:
            self._list_id = str(uuid1())

    def add_todo_item(self, todo_task):
        method_guard(self.add_todo_item, todo_task, of_type=TodoTask)
        if any(todo for todo in self._todos if todo.get_id() == todo_task.get_id()):
            raise KeyError("its not possible to add the same item to a list")
        self._todos.append(todo_task)

    def delete_task(self, todo_id):
        task = self.get_todo_by_id(todo_id)
        task.delete_task()

    def get_todo_by_id(self, todo_id) -> TodoTask:
        task = next((todo for todo in self._todos if todo.get_id() == todo_id), None)
        if task is None:
            raise KeyError("todo_id '{}' doesnt exist in list '{}' (id '{}')".format(todo_id, self._name, self._list_id))
        return task

    def get_name(self):
        return self._name

    def get_todos(self):
        return self._todos

    def get_owner_ids(self):
        return self._owner_ids

    def get_id(self):
        return self._list_id

    def to_json(self):
        todo_jsons = [todo.to_json() for todo in self._todos]
        todos_json = str.join("\n", todo_jsons)
        owner_ids = json.dumps(self._owner_ids)
        return '"list_id":"{}", "name":"{}", "owner_ids":"{}", "todos":"{}"'.format(self._list_id, self._name, owner_ids, todos_json)