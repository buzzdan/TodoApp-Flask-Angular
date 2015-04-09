import datetime
from server.Entities import TodoTask
from server.Repositories.ITodoRepository import ITodoRepository
from pymongo import MongoClient
from server.Utils.Maybe import Maybe

# TODO: finish this class - handle if not found with maybe object...


class MongoDbTodoRepository(ITodoRepository):
    def __init__(self, connection_string):
        self._connection_string = connection_string
        self._db_client = MongoClient(connection_string)
        self._db = self._db_client.get_default_database()
        self._todos_db = self._db['todos']

    def get_all(self):
        return self._todos_db

    def add(self, task_name):
        todo = {"task_name": task_name, "date": datetime.datetime.utcnow()}
        self._todos_db.insert_one(todo)

    def get_by_id(self, todo_id):
        result = self._todos_db.find_one({"_id": todo_id})
        todo = TodoTask(todo_name=result.todo_name, todo_id=result.todo_id)
        return Maybe(value=todo)

    def update(self, todo_id, task_name):
        self._todos_db.update_one({"_id": todo_id}, {"task_name": task_name})

    def delete(self, todo_id):
        self._todos_db.remove({"_id": todo_id})