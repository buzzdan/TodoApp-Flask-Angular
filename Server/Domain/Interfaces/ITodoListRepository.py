from abc import ABCMeta, abstractmethod
from Server.Domain.Entities import TodoList


class ITodoListRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_user_list_metadata(self, user_id):
        pass

    @abstractmethod
    def get_by_id(self, list_id) -> TodoList:
        pass

    @abstractmethod
    def create(self, new_list: TodoList):
        pass

    @abstractmethod
    def update(self, todo_list: TodoList):
        pass

    def delete(self, list_id):
        pass