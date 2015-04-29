from flask import Flask, send_from_directory
from flask_restful import Api
from Server.Application.ListManagementService import ListManagementService
from Server.Infrastructure.Data import InMemoryTodoRepository, MongoDbTodoRepository, MongoDbTodoListRepository
from Server.Infrastructure.Data.InMemoryUserRepository import InMemoryUserRepository
from Server.Infrastructure.Data.MongoDbUserRepository import MongoDbUserRepository
from Server.Infrastructure.Framework.ApiResources import TodoList
from Server.Infrastructure.Framework.ApiResources import Todo
from Server.Infrastructure.Framework.ApiResources import Profile
from Server.Infrastructure.Services import EnvironmentSettingsLoader, WerkzeugPasswordHasher, ConfigurationError
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
        self._static_files_root_folder_path = static_files_root_folder_path  # + '/js/satellizer'  # <-- Use this to run sattilizer
        self._app.add_url_rule('/<path:file_relative_path_to_root>', 'serve_page', self._serve_page, methods=['GET'])
        self._app.add_url_rule('/', 'index', self._goto_index, methods=['GET'])

    def register_routes_to_resources(self, static_files_root_folder_path):
        self._register_static_server(static_files_root_folder_path)

        db_url = self._environment_settings_loader['MONGOLAB_URI']
        print(db_url)

        userRepo = MongoDbUserRepository(db_url)
        hasher = WerkzeugPasswordHasher()
        self.authenticator = FlaskAuthenticationRouter(userRepo, hasher, self._app)
        self.authenticator.register_routes()

        todo_list_repo = MongoDbTodoListRepository(db_url)
        list_service = ListManagementService(todo_list_repo)
        todo_list = TodoList.create(list_service)

        # todo_repo = InMemoryTodoRepository()
        todo_repo = MongoDbTodoRepository(db_url)
        todo = Todo.create(todo_repo)
        profile = Profile.create(userRepo)

        self._api.add_resource(profile, '/api/me')
        self._api.add_resource(todo, '/api/todos/<todo_id>')
        self._api.add_resource(todo_list, '/api/todos')

    def _goto_index(self):
        return self._serve_page("index.html")

    def _serve_page(self, file_relative_path_to_root):

        if file_relative_path_to_root == 'appConfigs.js':
            return self._server_configs()

        print("sending '{}/{}'".format(self._static_files_root_folder_path, file_relative_path_to_root))
        return send_from_directory(self._static_files_root_folder_path, file_relative_path_to_root)

    def _server_configs(self):
        env = EnvironmentChecker(self._environment_settings_loader['APP_SETTINGS'])
        if env.is_production():
            return send_from_directory(self._static_files_root_folder_path, 'configs/production.js')
        elif env.is_development():
            return send_from_directory(self._static_files_root_folder_path, 'configs/development.js')
        else:
            raise ConfigurationError("cannot retrieve app configs. make sure environment is configured")

    def run(self):
        debug = bool(self._environment_settings_loader['DEBUG'])
        if debug:
            self._app.run(debug=debug, host='fuf.me', port=5000)
        else:
            self._app.run()

    def get_flask_runner(self):
        return self._app


class EnvironmentChecker:
    def __init__(self, config_name):
        self.config_name = config_name

    def is_production(self):
        return self.config_name == 'ProductionConfig'

    def is_development(self):
        return self.config_name == 'DevelopmentConfig'