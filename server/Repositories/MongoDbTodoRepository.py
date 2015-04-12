import datetime
from bson import ObjectId
from server.Entities.TodoTask import TodoTask
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
        todos = list(self._todos_db.find())
        todo_tasks = [TodoTask(todo["task_name"], str(todo["_id"])) for todo in todos]
        return todo_tasks

    def add(self, task_name):
        todo = {"task_name": task_name, "date": datetime.datetime.utcnow()}
        self._todos_db.insert(todo)

    def get_by_id(self, todo_id):
        result = self._todos_db.find_one({"_id": ObjectId(todo_id)})
        todo = TodoTask(result["task_name"], str(result["_id"]))
        return Maybe(value=todo)

    def update(self, todo_id, task_name):
        self._todos_db.update({"_id": ObjectId(todo_id)}, {"task_name": task_name})

    def delete(self, todo_id):
        self._todos_db.remove({"_id": ObjectId(todo_id)})