from Server.Domain.Core import pre_condition_arg
from Server.Domain.Entities import TodoTask
from Server.Domain.Interfaces import ITodoListRepository


class ListManagementService:
    def __init__(self, todolist_repository):
        """
        @type todolist_repository: ITodoListRepository
        """
        pre_condition_arg(self, todolist_repository, of_type=ITodoListRepository)
        self._todo_list_repository = todolist_repository

    def get_my_lists_metadata(self, user_id):
        return self._todo_list_repository.get_user_list_metadata(user_id)

    def get_list(self, list_id):
        return self._todo_list_repository.get_by_id(list_id)

    def add_task_to_list(self, list_id, task_name):
        todo_list = self._todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise KeyError("list id '{}' doesnt exist".format(list_id))

        task = TodoTask(task_name)
        todo_list.add_todo_item(task)

        self._todo_list_repository.update(todo_list)

    def delete_task_from_list(self, list_id, task_id):
        todo_list = self._todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise KeyError("list id '{}' doesnt exist".format(list_id))

        todo_list.delete_task(task_id)
        self._todo_list_repository.update(todo_list)
