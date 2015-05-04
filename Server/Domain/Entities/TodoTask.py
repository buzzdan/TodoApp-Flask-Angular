from enum import Enum
import json
from uuid import uuid1


class TodoTaskState(Enum):
    Unchanged = 1
    Added = 2
    Modified = 3
    Deleted = 4


class TodoTask:
    _id_counter = 1

    def __init__(self, task_name, todo_id=None):
        self.validate(task_name)
        self._task_name = task_name
        self._state = TodoTaskState.Unchanged

        if todo_id is None:
            self._id = str(uuid1())
            self._state = TodoTaskState.Added
        else:
            self._id = todo_id

    def get_state(self):
        return self._state

    def get_id(self):
        return self._id

    def get_task_name(self):
        return self._task_name

    def update_task(self, task_name):
        self.validate(task_name)
        self._task_name = task_name
        self._state = TodoTaskState.Modified

    def delete_task(self):
        self._state = TodoTaskState.Deleted

    def validate(self, task_name):
        if task_name is None or task_name.strip() == '':
            raise ValueError("task name cannot be empty")

    def to_dict(self):
        self_dict = {"task_id": self._id, "task_name": self._task_name}
        return self_dict

    def to_json(self):
        real_json = json.dumps(self.to_dict())
        return real_json
