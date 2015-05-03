from Server.Domain.Core import pre_condition_arg
from Server.Domain.Entities import TodoTask, TodoList
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
        todo_list = self._todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise KeyError("list id '{}' doesnt exist".format(list_id))
        return todo_list

    def add_task_to_list(self, list_id, task_name):
        todo_list = self._todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise KeyError("list id '{}' doesnt exist".format(list_id))

        task = TodoTask(task_name)
        todo_list.add_todo_item(task)

        self._todo_list_repository.update(todo_list)

    def update_todo(self, list_id, todo_id, task_name):
        todo_list = self.get_list(list_id)
        todo = todo_list.get_todo_by_id(todo_id)
        todo.update_task(task_name)
        self._todo_list_repository.update(todo_list)

    def get_todo_from_list(self, list_id, todo_id):
        todo_list = self.get_list(list_id)
        todo = todo_list.get_todo_by_id(todo_id)
        return todo

    def delete_task_from_list(self, list_id, task_id):
        todo_list = self._todo_list_repository.get_by_id(list_id)
        if not todo_list:
            raise KeyError("list id '{}' doesnt exist".format(list_id))

        todo_list.delete_task(task_id)
        self._todo_list_repository.update(todo_list)

    def create_new_list(self, list_name, user_id):
        new_list = TodoList(list_name, [user_id])
        self._todo_list_repository.create(new_list)
