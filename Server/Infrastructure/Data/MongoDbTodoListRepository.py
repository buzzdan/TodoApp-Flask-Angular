from pymongo import MongoClient
from Server.Domain.Core import method_guard, pre_condition_arg
from Server.Domain.Entities import TodoList, TodoTaskState, TodoTask
from Server.Domain.Interfaces import ITodoListRepository


class MongoDbTodoListRepository(ITodoListRepository):
    def __init__(self, connection_string: str):
        pre_condition_arg(self, connection_string, of_type=str)
        self._db_client = MongoClient(connection_string, _connect=False)
        self._todolist_db = None

    def _get_todos_collection(self):
        if not self._todolist_db:
            db = self._db_client.get_default_database()
            self._todolist_db = db['todos_lists']
        return self._todolist_db

    def get_by_id(self, list_id) -> TodoList:
        todo_collection = self._get_todos_collection()
        result = todo_collection.find_one({"list_id": list_id})
        if result is None:
            return None

        tasks = []
        for t in result["todos"]:
            tasks.append(TodoTask(t["task_name"], t["task_id"]))

        fetched_list = TodoList(result["name"], result["owner_ids"], tasks, result["list_id"])

        self._db_client.close()
        return fetched_list

    def get_user_list_metadata(self, user_id):
        todo_collection = self._get_todos_collection()
        owners_lists = list(todo_collection.find({"owner_ids": user_id}))
        if len(owners_lists) == 0:
            return []
        fetched_list = [TodoList(todo["name"], todo["owner_ids"], [], todo["list_id"]) for todo in owners_lists]
        self._db_client.close()
        return fetched_list

    def create(self, new_list: TodoList):
        method_guard(self.create, new_list, of_type=TodoList)
        list_json = new_list.to_json()
        todo_collection = self._get_todos_collection()
        todo_collection.insert(list_json)

    def update(self, todo_list: TodoList):
        method_guard(self.update, todo_list, of_type=TodoList)
        todo_collection = self._get_todos_collection()
        bulk = todo_collection.initialize_ordered_bulk_op()
        for todo in todo_list.get_todos():
            if todo.get_state() == TodoTaskState.Added:
                bulk.insert(todo.to_json())
            if todo.get_state() == TodoTaskState.Modified:
                bulk.find({"todo_id": todo.get_id()}).update(todo.to_json())
            if todo.get_state() == TodoTaskState.Deleted:
                bulk.find({"todo_id": todo.get_id()}).remove()
        bulk.execute()
