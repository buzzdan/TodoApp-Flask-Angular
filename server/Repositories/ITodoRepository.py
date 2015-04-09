from abc import ABCMeta, abstractmethod


class ITodoRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, todo_id):
        pass

    @abstractmethod
    def delete(self, todo_id):
        pass

    @abstractmethod
    def update(self, todo_id, task_name):
        pass

    @abstractmethod
    def add(self, task_name):
        pass