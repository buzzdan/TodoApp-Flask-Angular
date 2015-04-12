from flask import Flask, send_from_directory
from flask_restful import Api
from server.ApiResources.TodoList import TodoList
from server.ApiResources.Todo import Todo
from server.Repositories.MongoDbTodoRepository import MongoDbTodoRepository
from server.Utils.EnvironmentSettingsLoader import EnvironmentSettingsLoader
from server.Utils.GeneralUtils import pre_condition_arg


class AppStarter():

    def __init__(self, environment_settings_loader):
        pre_condition_arg(self, environment_settings_loader, EnvironmentSettingsLoader)
        self._environment_settings_loader = environment_settings_loader
        self._static_files_root_folder_path = ''  # Default is current folder
        self._app = Flask(__name__)  # , static_folder='client', static_url_path='')
        self._api = Api(self._app)
        # self._app.config.from_object(config_name)

    def _register_static_server(self, static_files_root_folder_path):
        self._static_files_root_folder_path = static_files_root_folder_path
        self._app.add_url_rule('/<path:file_relative_path_to_root>', 'serve_page', self._serve_page, methods=['GET'])
        self._app.add_url_rule('/', 'index', self._goto_index, methods=['GET'])

    def register_routes_to_resources(self, static_files_root_folder_path):
        self._register_static_server(static_files_root_folder_path)

        db_url = self._environment_settings_loader['DB_CONNECTION_STRING']
        todo_repo = MongoDbTodoRepository(db_url)
        todo = Todo.create(todo_repo)
        todo_list = TodoList.create(todo_repo)

        self._api.add_resource(todo, '/api/todos/<todo_id>')
        self._api.add_resource(todo_list, '/api/todos')

    def _goto_index(self):
        return self._serve_page("index.html")

    def _serve_page(self, file_relative_path_to_root):
        return send_from_directory(self._static_files_root_folder_path, file_relative_path_to_root)

    def run(self):
        self._app.run()

    def get_flask_runner(self):
        return self._app