import datetime
from urllib.parse import urlsplit
from bson import ObjectId
from server.Entities.TodoTask import TodoTask
from server.Repositories.ITodoRepository import ITodoRepository
from pymongo import MongoClient, Connection
from server.Utils.GeneralUtils import pre_condition_arg
from server.Utils.Maybe import Maybe

# TODO: finish this class - handle if not found with maybe object...


class DBConnectionDetails:
    def __init__(self, connection_string):
        self.db_url = connection_string
        self.parsed_url = urlsplit(connection_string)
        self.db_name = self.parsed_url.path[1:]
        self.user = ''
        self.password = ''

        # Authenticate
        if '@' in self.db_url:
            self.user, self.password = self.parsed_url.netloc.split('@')[0].split(':')


class MongoDbTodoRepository(ITodoRepository):

    def __init__(self, connection_string):

        pre_condition_arg(self, connection_string, of_type=str)

        self._connection_details = DBConnectionDetails(connection_string)
        self._db_client = MongoClient(connection_string, _connect=False)
        self._todos_db = None

        # db = self.connect_to_db(connection_string)
        # self._db_client = MongoClient(connection_string)
        # self._db = self._db_client.get_default_database()
        # self._todos_db = db['todos']

    def _get_todos_collection(self):
        if not self._todos_db:
            db = self._db_client.get_default_database()
            self._db_client.au
            self._todos_db = db['todos']
        return self._todos_db

        # db_url = self._db_url
        # parsed_url = urlsplit(db_url)
        # db_name = parsed_url.path[1:]
        # # Get your DB
        # # Authenticate
        # if '@' in db_url:
        #     user, password = parsed_url.netloc.split('@')[0].split(':')
        #     # db.authenticate(user, password)
        #
        # db = Connection(db_url)[db_name]
        # return db

    def get_all(self):
        todo_collection = self._get_todos_collection()
        todos_list = list(todo_collection.find())
        todo_tasks = [TodoTask(todo["task_name"], str(todo["_id"])) for todo in todos_list]
        self._db_client.close()
        return todo_tasks

    def add(self, task_name):
        todo = {"task_name": task_name, "date": datetime.datetime.utcnow()}
        todo_collection = self._get_todos_collection()
        todo_collection.insert(todo)
        self._db_client.close()

    def get_by_id(self, todo_id):
        todo_collection = self._get_todos_collection()
        result = todo_collection.find_one({"_id": ObjectId(todo_id)})
        todo = TodoTask(result["task_name"], str(result["_id"]))
        self._db_client.close()
        return Maybe(value=todo)

    def update(self, todo_id, task_name):
        todo_collection = self._get_todos_collection()
        todo_collection.update({"_id": ObjectId(todo_id)}, {"task_name": task_name})
        self._db_client.close()

    def delete(self, todo_id):
        todo_collection = self._get_todos_collection()
        todo_collection.remove({"_id": ObjectId(todo_id)})
        self._db_client.close()