from flask import Flask, send_from_directory
from flask_restful import Api, Resource
from server.ApiResources.TodoList import TodoList
from server.ApiResources.Todo import Todo


class AppStarter():

    def __init__(self, config_name):
        self._static_files_root_folder_path = ''  # Default is current folder
        self._app = Flask(__name__)  # , static_folder='client', static_url_path='')
        self._app.config.from_object(config_name)
        self._api = Api(self._app)

    def _register_static_server(self, static_files_root_folder_path):
        self._static_files_root_folder_path = static_files_root_folder_path
        self._app.add_url_rule('/<path:file_relative_path_to_root>', 'serve_page', self._serve_page, methods=['GET'])
        self._app.add_url_rule('/', 'index', self._goto_index, methods=['GET'])

    def register_routes_to_resources(self, static_files_root_folder_path):
        self._register_static_server(static_files_root_folder_path)
        self._api.add_resource(TodoList, '/api/todos')
        self._api.add_resource(Todo, '/api/todos/<todo_id>')

    def _goto_index(self):
        return self._serve_page("index.html")

    def _serve_page(self, file_relative_path_to_root):
        return send_from_directory(self._static_files_root_folder_path, file_relative_path_to_root)

    def run(self):
        self._app.run()

    def get_flask_runner(self):
        return self._app