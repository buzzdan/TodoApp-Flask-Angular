from flask import Flask, send_from_directory
from flask_restful import Api
from Server.Infrastructure.Data import InMemoryTodoRepository
from Server.Infrastructure.Data.InMemoryUserRepository import InMemoryUserRepository
from Server.Infrastructure.Framework.ApiResources import TodoList
from Server.Infrastructure.Framework.ApiResources import Todo
from Server.Infrastructure.Framework.ApiResources import Profile
from Server.Infrastructure.Services import EnvironmentSettingsLoader
from .FlaskAuthenticationRouter import FlaskAuthenticationRouter
from Server.Domain.Core import pre_condition_arg


class AppStarter():

    def __init__(self, environment_settings_loader):

        pre_condition_arg(self, environment_settings_loader, EnvironmentSettingsLoader)
        self._environment_settings_loader = environment_settings_loader

        self._static_files_root_folder_path = ''  # Default is current folder

        self._app = Flask(__name__)  # , static_folder='Client', static_url_path='')
        self._api = Api(self._app)

    def _register_static_server(self, static_files_root_folder_path):
        self._static_files_root_folder_path = static_files_root_folder_path + '/js/satellizer'
        self._app.add_url_rule('/<path:file_relative_path_to_root>', 'serve_page', self._serve_page, methods=['GET'])
        self._app.add_url_rule('/', 'index', self._goto_index, methods=['GET'])

    def register_routes_to_resources(self, static_files_root_folder_path):
        self._register_static_server(static_files_root_folder_path)

        userRepo = InMemoryUserRepository()
        self.authenticator = FlaskAuthenticationRouter(userRepo, self._app)
        self.authenticator.register_routes()

        db_url = self._environment_settings_loader['MONGOLAB_URI']
        print(db_url)

        # todo_repo = MongoDbTodoRepository(db_url)
        todo_repo = InMemoryTodoRepository()
        todo = Todo.create(todo_repo)
        todo_list = TodoList.create(todo_repo)
        profile = Profile.create(userRepo)

        self._api.add_resource(profile, '/api/me')
        self._api.add_resource(todo, '/api/todos/<todo_id>')
        self._api.add_resource(todo_list, '/api/todos')

    def _goto_index(self):
        return self._serve_page("index.html")

    def _serve_page(self, file_relative_path_to_root):
        print("sending '{}/{}'".format(self._static_files_root_folder_path, file_relative_path_to_root))
        return send_from_directory(self._static_files_root_folder_path, file_relative_path_to_root)

    def run(self):
        debug = bool(self._environment_settings_loader['DEBUG'])
        if debug:
            self._app.run(debug=debug, host='fuf.me', port=5000)
        else:
            self._app.run()

    def get_flask_runner(self):
        return self._app